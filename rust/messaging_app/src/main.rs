mod message;
mod server;
mod client;
mod log_event;

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let args: Vec<String> = std::env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: {} <server|client> ...", args[0]);
        return Ok(());
    }

    match args[1].as_str() {
        "server" => server::run().await?,
        "client" => client::run().await?,
        _ => eprintln!("Unknown mode: {}", args[1]),
    }

    Ok(())
}
