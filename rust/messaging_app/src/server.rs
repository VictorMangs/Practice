use tokio::{
    net::{TcpListener, TcpStream},
    io::{AsyncBufReadExt, AsyncWriteExt, BufReader},
    sync::{Mutex, mpsc},
};
use std::sync::Arc;
use serde_json::Result as JsonResult;

use crate::message::Message;
use crate::log_event::{log, LogEvent};

type Clients = Arc<Mutex<Vec<(String, mpsc::UnboundedSender<String>)>>>;

pub async fn run() -> anyhow::Result<()> {
    let listener = TcpListener::bind("127.0.0.1:8080").await?;
    let clients: Clients = Arc::new(Mutex::new(Vec::new()));

    log(LogEvent::Startup("Server running on 127.0.0.1:8080"));

    loop {
        let (stream, addr) = listener.accept().await?;
        let clients = clients.clone();

        log(LogEvent::Connection(&addr.to_string()));

        tokio::spawn(async move {
            if let Err(e) = handle_client(stream, clients).await {
                log(LogEvent::Error(&format!("Client error: {:?}", e)));
            }
        });
    }
}

async fn handle_client(stream: TcpStream, clients: Clients) -> anyhow::Result<()> {
    let (reader, mut writer) = stream.into_split();
    let mut reader = BufReader::new(reader).lines();

    let (tx, mut rx) = mpsc::unbounded_channel::<String>();

    // First line should be the username
    let username = if let Some(line) = reader.next_line().await? {
        line
    } else {
        return Ok(()); // no username, drop
    };

    {
        let mut c = clients.lock().await;
        c.push((username.clone(), tx));
    }

    log(LogEvent::Join(&username));
    broadcast_system(&clients, &format!("{} has joined", username)).await;

    // Task for sending messages to this client
    let mut write_task = tokio::spawn(async move {
        while let Some(msg) = rx.recv().await {
            if writer.write_all(msg.as_bytes()).await.is_err() {
                break;
            }
            if writer.write_all(b"\n").await.is_err() {
                break;
            }
        }
    });

    // Task for receiving messages
    while let Some(line) = reader.next_line().await? {
        let parsed: JsonResult<Message> = serde_json::from_str(&line);
        match parsed {
            Ok(msg) => match msg {
                Message::Command { name, args } => {
                    log(LogEvent::Command { user: &username, name: &name, args: &args });

                    match name.as_str() {
                        "list" => {
                            let c = clients.lock().await;
                            let users: Vec<String> = c.iter().map(|(u, _)| u.clone()).collect();
                            send_to_user(&clients, &username,
                                Message::System { text: format!("Online: {:?}", users) }).await;
                        }
                        "quit" => {
                            break;
                        }
                        "help" => {
                            send_to_user(&clients, &username,
                                Message::System { text: "/msg <user> <text>, /list, /help, /quit".into() }).await;
                        }
                        "msg" => {
                            if args.len() >= 2 {
                                let target = &args[0];
                                let text = args[1..].join(" ");
                                log(LogEvent::Private { from: &username, to: target, text: &text });
                                send_to_user(&clients, target,
                                    Message::Private { from: username.clone(), to: target.clone(), text }).await;
                            }
                        }
                        _ => {
                            log(LogEvent::Warning(&format!("{} sent unknown command: {}", username, name)));
                        }
                    }
                }
                Message::Chat { text, .. } => {
                    log(LogEvent::Chat { user: &username, text: &text });
                    broadcast(&clients,
                        Message::Chat { from: username.clone(), text }).await;
                }
                _ => {}
            },
            Err(_) => {
                log(LogEvent::Warning(&format!("{} sent invalid JSON", username)));
            }
        }
    }

    // Clean up
    {
        let mut c = clients.lock().await;
        c.retain(|(u, _)| *u != username);
    }
    log(LogEvent::Leave(&username));
    broadcast_system(&clients, &format!("{} has left", username)).await;

    write_task.abort();
    Ok(())
}

async fn broadcast(clients: &Clients, msg: Message) {
    let serialized = serde_json::to_string(&msg).unwrap();
    let c = clients.lock().await;
    for (_, tx) in c.iter() {
        let _ = tx.send(serialized.clone());
    }
}

async fn broadcast_system(clients: &Clients, text: &str) {
    broadcast(clients, Message::System { text: text.to_string() }).await;
}

async fn send_to_user(clients: &Clients, user: &str, msg: Message) {
    let serialized = serde_json::to_string(&msg).unwrap();
    let c = clients.lock().await;
    for (u, tx) in c.iter() {
        if u == user {
            let _ = tx.send(serialized.clone());
        }
    }
}
