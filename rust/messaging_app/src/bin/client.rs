use messaging_app::message::Message;
use messaging_app::log_event::log;
use messaging_app::utils::*;
use messaging_app::tui::TuiClient;

use std::collections::{HashMap, HashSet};
use std::io::{self, Write};
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::Duration;

use tokio::io::{AsyncBufReadExt, AsyncWriteExt, BufReader};
use tokio::net::TcpStream;
use tokio::sync::mpsc as tokio_mpsc;

use ratatui::text::Line;

const DEFAULT_PORT: u16 = 8080;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // --- Get username ---
    let username = std::env::var("USER")
        .or_else(|_| std::env::var("LOGNAME"))
        .unwrap_or_else(|_| {
            print!("Enter username: ");
            io::stdout().flush().unwrap();
            let mut input = String::new();
            io::stdin().read_line(&mut input).unwrap();
            input.trim().to_string()
        });

    // --- Connect to server ---
    let server_addr = format!("{}:{}", get_local_ip().unwrap_or("127.0.0.1".parse().unwrap()), DEFAULT_PORT);
    log(&format!("Connecting to server at {}", server_addr)).await;

    let stream = TcpStream::connect(&server_addr).await?;
    let (reader, mut writer) = stream.into_split();
    let mut reader = BufReader::new(reader).lines();

    // --- Channels ---
    let (tui_tx, tui_rx) = std::sync::mpsc::channel::<Line<'static>>();
    let (input_tx, mut input_rx) = tokio_mpsc::unbounded_channel::<String>();

    // --- Send username to server ---
    writer.write_all(format!("{}\n", username).as_bytes()).await?;
    writer.flush().await?;

    // --- Username colors ---
    let user_colors = Arc::new(Mutex::new(HashMap::<String, ratatui::style::Color>::new()));
    let used_colors = Arc::new(Mutex::new(HashSet::<ratatui::style::Color>::new()));

    // --- Spawn reader task ---
    {
        let tui_tx_clone = tui_tx.clone();
        let user_colors = Arc::clone(&user_colors);
        let used_colors = Arc::clone(&used_colors);
        let username_clone = username.clone();

        tokio::spawn(async move {
            while let Ok(Some(line)) = reader.next_line().await {
                if let Ok(msg) = serde_json::from_str::<Message>(&line) {
                    let styled_line = match msg {
                        Message::Chat { from, text } => {
                            let style = get_username_style(&from, &mut user_colors.lock().unwrap(), &mut used_colors.lock().unwrap());
                            Line::from(format!("{}: {}", from, text)).style(style)
                        }
                        Message::System { text } => Line::from(format!("[System] {}", text))
                            .style(ratatui::style::Style::default().fg(ratatui::style::Color::Yellow).add_modifier(ratatui::style::Modifier::ITALIC)),
                        Message::Join { username } => Line::from(format!("[System] {} has joined!", username))
                            .style(ratatui::style::Style::default().fg(ratatui::style::Color::Yellow).add_modifier(ratatui::style::Modifier::ITALIC)),
                        _ => continue,
                    };
                    let _ = tui_tx_clone.send(styled_line);
                }
            }
        });
    }

    // --- Spawn writer task ---
    {
        let mut writer_clone = writer;
        tokio::spawn(async move {
            while let Some(msg) = input_rx.recv().await {
                let _ = writer_clone.write_all(format!("{}\n", msg).as_bytes()).await;
                let _ = writer_clone.flush().await;
            }
        });
    }

    // --- Start TUI ---
    let mut tui_client = TuiClient::new(username.clone());
    tui_client.start(tui_rx, input_tx)?;

    Ok(())
}
