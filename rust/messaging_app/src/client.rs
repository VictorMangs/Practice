// ... (rest of the file is the same)
use anyhow::Result;
use serde_json::Result as JsonResult;
use std::io::{self, Write};
use tokio::io::{AsyncBufReadExt, AsyncWriteExt, BufReader};
use tokio::net::TcpStream;
use tokio::sync::mpsc;

use crate::log_event::{log, LogEvent};
use crate::message::Message;

pub async fn run() -> Result<()> {
    let stream = TcpStream::connect("127.0.0.1:8080").await?;
    let (reader, mut writer) = stream.into_split();
    let mut reader = BufReader::new(reader).lines();

    // Create a channel to pass messages from the blocking task to the async writer
    let (tx, mut rx) = mpsc::unbounded_channel::<String>();

    // Ask username
    print!("Enter username: ");
    io::stdout().flush()?;
    let mut username = String::new();
    io::stdin().read_line(&mut username)?;
    let username = username.trim().to_string();

    writer.write_all(format!("{}\n", username).as_bytes()).await?;
    writer.flush().await?;

    log(LogEvent::Startup(&format!("Connected as {}", username)));

    // Clone username for the reader task so it can filter its own messages
    let username_for_reader = username.clone();

    // Spawn a task to handle incoming messages
    let reader_task = tokio::spawn(async move {
        while let Some(line) = reader.next_line().await.unwrap_or(None) {
            let parsed: JsonResult<Message> = serde_json::from_str(&line);
            match parsed {
                Ok(msg) => match msg {
                    Message::System { text } => {
                        if !text.contains(&username_for_reader) {
                            log(LogEvent::Startup(&format!("SYSTEM: {}", text)))
                        }
                    }
                    Message::Chat { from, text } => {
                        // **Added filter**: Only log the message if it's NOT from us.
                        if from != username_for_reader {
                            log(LogEvent::Chat {
                                user: &from,
                                text: &text,
                            })
                        }
                    }
                    Message::Private { from, to, text } => {
                        log(LogEvent::Private {
                            from: &from,
                            to: &to,
                            text: &text,
                        })
                    }
                    Message::Command { .. } => {
                        log(LogEvent::Warning("Unexpected command from server"))
                    }
                },
                Err(_) => log(LogEvent::Warning("Invalid JSON from server")),
            }
        }
    });
    
    let username_for_input = username.clone();

    // Spawn a task to handle user input
    // Spawn a task to handle user input
    tokio::task::spawn_blocking(move || {
        let mut input = String::new();
        loop {
            // Print the username as the prompt
            print!("{} > ", username_for_input);
            io::stdout().flush().unwrap();

            input.clear();
            if io::stdin().read_line(&mut input).is_err() {
                break;
            }
            let trimmed = input.trim();
            if trimmed.is_empty() {
                continue;
            }

            let serialized = if trimmed.starts_with('/') {
                let parts: Vec<&str> = trimmed[1..].split_whitespace().collect();
                if parts.is_empty() {
                    continue;
                }
                let name = parts[0].to_string();
                let args = parts[1..].iter().map(|s| s.to_string()).collect::<Vec<_>>();
                let msg = Message::Command { name, args };
                serde_json::to_string(&msg).unwrap()
            } else {
                let msg = Message::Chat {
                    from: username_for_input.clone(),
                    text: trimmed.to_string(),
                };
                serde_json::to_string(&msg).unwrap()
            };

            // Send the serialized message through the channel
            if tx.send(serialized).is_err() {
                break;
            }
        }
    });


    // Main loop to send messages from the channel
    let writer_task = tokio::spawn(async move {
        while let Some(serialized) = rx.recv().await {
            if writer.write_all(format!("{}\n", serialized).as_bytes()).await.is_err() {
                break;
            }
            if writer.flush().await.is_err() {
                break;
            }
        }
    });

    // Wait until either side ends
    tokio::select! {
        _ = reader_task => {}
        _ = writer_task => {}
    }

    log(LogEvent::Leave(&username));
    Ok(())
}
