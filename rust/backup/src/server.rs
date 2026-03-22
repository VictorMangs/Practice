use std::sync::Arc;
use tokio::{
    io::{AsyncBufReadExt, AsyncWriteExt, BufReader},
    net::{TcpListener, TcpStream, UdpSocket},
    sync::{mpsc, Mutex},
};

use anyhow::Result;
use serde_json::Result as JsonResult;

use crate::{log_event::log, log_event::init_logger, message::Message};

type Clients = Arc<Mutex<Vec<(String, mpsc::UnboundedSender<String>)>>>;

const TCP_PORT: u16 = 8080;
const DISCOVERY_PORT: u16 = 8888;

/// Starts the main chat server, handling both TCP clients and UDP discovery.
pub async fn run_server() -> Result<()> {
    // Initialize async logger
    init_logger().await;

    // Start UDP discovery in the background
    tokio::spawn(run_discovery());

    let listener = TcpListener::bind(("0.0.0.0", TCP_PORT)).await?;
    let addr = listener.local_addr()?;
    log(&format!("Server running on {}", addr)).await;

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

/// Handles UDP broadcast discovery requests for auto-detecting the chat server.
async fn run_discovery() -> Result<()> {
    let socket = UdpSocket::bind(("0.0.0.0", DISCOVERY_PORT)).await?;
    log(&format!(
        "Discovery service listening on UDP {}",
        DISCOVERY_PORT
    ))
    .await;

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

/// Manages a single client’s lifecycle — join, message handling, and disconnect.
/// Manages a single client’s lifecycle — join, message handling, and disconnect.
async fn handle_client(stream: TcpStream, clients: Clients) -> Result<()> {
    let (reader, mut writer) = stream.into_split();
    let mut reader = BufReader::new(reader).lines();
    let (tx, mut rx) = mpsc::unbounded_channel::<String>();

    // Loop until the client provides a unique username
    let username = loop {
        // Ask for the first line (username)
        let name = match reader.next_line().await? {
            Some(n) => n.trim().to_string(),
            None => return Ok(()), // client disconnected immediately
        };

        let mut c = clients.lock().await;
        if c.iter().any(|(u, _)| *u == name) {
            // Username taken; ask client to choose another
            let _ = writer
                .write_all(
                    serde_json::to_string(&Message::System {
                        text: "Username already taken. Please choose another.".to_string(),
                    })
                    .unwrap()
                    .as_bytes(),
                )
                .await;
            let _ = writer.write_all(b"\n").await;
        } else {
            // Unique username; accept it
            c.push((name.clone(), tx.clone()));
            break name;
        }
    };

    log(&format!("{} joined", username)).await;
    broadcast_system(&clients, &format!("{} has joined", username)).await;

    // Writer task (outgoing messages)
    let write_task = tokio::spawn(async move {
        while let Some(msg) = rx.recv().await {
            if writer.write_all(msg.as_bytes()).await.is_err()
                || writer.write_all(b"\n").await.is_err()
            {
                break;
            }
        }
    });

    // Reader loop (incoming messages)
    while let Some(line) = reader.next_line().await? {
        let parsed: JsonResult<Message> = serde_json::from_str(&line);

        match parsed {
            Ok(Message::Chat { text, .. }) => {
                log(&format!("{}: {}", username, text)).await;
                broadcast(
                    &clients,
                    Message::Chat {
                        from: username.clone(),
                        text,
                    },
                )
                .await;
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

    // Disconnect: remove from clients list
    {
        let mut c = clients.lock().await;
        c.retain(|(u, _)| *u != username);
    }

    log(&format!("{} left", username)).await;
    broadcast_system(&clients, &format!("{} has left", username)).await;

    write_task.abort();
    Ok(())
}


/// Broadcasts a message to all connected clients.
async fn broadcast(clients: &Clients, msg: Message) {
    let serialized = serde_json::to_string(&msg).unwrap();
    let c = clients.lock().await;

    for (_, tx) in c.iter() {
        let _ = tx.send(serialized.clone());
    }
}

/// Broadcasts a system message.
async fn broadcast_system(clients: &Clients, text: &str) {
    broadcast(clients, Message::System { text: text.to_string() }).await;
}
