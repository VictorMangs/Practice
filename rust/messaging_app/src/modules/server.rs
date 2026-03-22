use std::sync::Arc;
use tokio::sync::{mpsc, Mutex};
use tokio::net::{TcpListener, TcpStream, UdpSocket};
use tokio::io::{AsyncBufReadExt, AsyncWriteExt, BufReader};

use anyhow::Result;
use serde_json::Result as JsonResult;

use messaging_app::log_event::{log, init_logger};
use messaging_app::message::Message;

type Clients = Arc<Mutex<Vec<(String, mpsc::UnboundedSender<String>)>>>;

const TCP_PORT: u16 = 8080;
const DISCOVERY_PORT: u16 = 8888;

#[tokio::main]
async fn main() -> Result<()> {
    // Initialize logger
    init_logger().await;

    // Start UDP discovery
    tokio::spawn(run_discovery());

    // Start TCP server
    let listener = TcpListener::bind(("0.0.0.0", TCP_PORT)).await?;
    log(&format!("Server running on 0.0.0.0:{}", TCP_PORT)).await;

    let clients: Clients = Arc::new(Mutex::new(Vec::new()));

    loop {
        let (stream, addr) = listener.accept().await?;
        let clients = Arc::clone(&clients);

        log(&format!("Client connected: {}", addr)).await;

        tokio::spawn(async move {
            if let Err(err) = handle_client(stream, clients).await {
                log(&format!("Client error: {:?}", err)).await;
            }
        });
    }
}

// --- UDP Discovery ---
async fn run_discovery() -> Result<()> {
    let socket = UdpSocket::bind(("0.0.0.0", DISCOVERY_PORT)).await?;
    log(&format!("Discovery listening on UDP {}", DISCOVERY_PORT)).await;

    let mut buf = [0u8; 1024];
    loop {
        let (len, addr) = socket.recv_from(&mut buf).await?;
        let msg = String::from_utf8_lossy(&buf[..len]);

        if msg.trim() == "DISCOVER_CHAT_SERVER" {
            let reply = format!("CHAT_SERVER:{}", TCP_PORT);
            let _ = socket.send_to(reply.as_bytes(), addr).await;
            log(&format!("Replied to discovery request from {}", addr)).await;
        }
    }
}

// --- Handle single client ---
async fn handle_client(stream: TcpStream, clients: Clients) -> Result<()> {
    let (reader, mut writer) = stream.into_split();
    let mut reader = BufReader::new(reader).lines();
    let (tx, mut rx) = mpsc::unbounded_channel::<String>();

    // First line is the username
    let username = match reader.next_line().await? {
        Some(name) => name.trim().to_string(),
        None => return Ok(()),
    };

    // Add client
    {
        let mut c = clients.lock().await;
        c.push((username.clone(), tx));
    }

    log(&format!("{} joined", username)).await;
    broadcast_system(&clients, &format!("{} has joined", username)).await;

    // --- Writer task ---
    let write_task = tokio::spawn(async move {
        while let Some(msg) = rx.recv().await {
            if writer.write_all(msg.as_bytes()).await.is_err()
                || writer.write_all(b"\n").await.is_err()
            {
                break;
            }
        }
    });

    // --- Reader loop ---
    while let Some(line) = reader.next_line().await? {
        let parsed: JsonResult<Message> = serde_json::from_str(&line);

        match parsed {
            Ok(Message::Chat { text, .. }) => {
                log(&format!("{}: {}", username, text)).await;
                broadcast(&clients, Message::Chat {
                    from: username.clone(),
                    text,
                }).await;
            }
            Ok(Message::System { text }) => {
                log(&format!("System from {}: {}", username, text)).await;
            }
            Err(_) => {
                log(&format!("{} sent invalid JSON", username)).await;
            }
            _ => {}
        }
    }

    // --- Disconnect ---
    {
        let mut c = clients.lock().await;
        c.retain(|(u, _)| *u != username);
    }

    log(&format!("{} left", username)).await;
    broadcast_system(&clients, &format!("{} has left", username)).await;

    write_task.abort();
    Ok(())
}

// --- Broadcast chat message ---
async fn broadcast(clients: &Clients, msg: Message) {
    let serialized = serde_json::to_string(&msg).unwrap();
    let c = clients.lock().await;

    for (_, tx) in c.iter() {
        let _ = tx.send(serialized.clone());
    }
}

// --- Broadcast system message ---
async fn broadcast_system(clients: &Clients, text: &str) {
    broadcast(clients, Message::System { text: text.to_string() }).await;
}
