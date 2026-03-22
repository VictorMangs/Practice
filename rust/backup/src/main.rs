use std::env;

mod log_event;
mod message;
mod server;
mod tui_client;

use log_event::{log, init_logger};

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    // Initialize logger first
    init_logger().await;

    let args: Vec<String> = env::args().collect();

    match args.get(1).map(|s| s.as_str()) {
        Some("server") => {
            log("Starting chat server...").await;
            server::run_server().await?;
        }
        Some("client") => {
            log("Launching TUI chat client...").await;
            let server_addr = args.get(2).map(|s| s.as_str());
            tui_client::run_client(server_addr).await?;
        }
        _ => {
            eprintln!("Usage: chat_app [server|client]");
        }
    }

    Ok(())
}
