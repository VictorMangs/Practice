use colored::*;

/// Log levels / categories
pub enum LogEvent<'a> {
    Startup(&'a str),
    Connection(&'a str),
    Join(&'a str),
    Leave(&'a str),
    Chat { user: &'a str, text: &'a str },
    Private { from: &'a str, to: &'a str, text: &'a str },
    Command { user: &'a str, name: &'a str, args: &'a [String] },
    Warning(&'a str),
    Error(&'a str),
}

pub fn log(event: LogEvent) {
    match event {
        LogEvent::Startup(msg) => println!("{}", format!("✅ {}", msg).green().bold()),
        LogEvent::Connection(addr) => println!("{}", format!("📡 Connection from {}", addr).cyan()),
        LogEvent::Join(user) => println!("{}", format!("👤 {} joined", user).yellow().bold()),
        LogEvent::Leave(user) => println!("{}", format!("👋 {} left", user).yellow().bold()),
        LogEvent::Chat { user, text } => println!("{}", format!("💬 {}: {}", user, text).white()),
        LogEvent::Private { from, to, text } => {
            println!("{}", format!("✉️  {} → {}: {}", from, to, text).magenta().bold())
        }
        LogEvent::Command { user, name, args } => {
            println!("{}", format!("📥 {} issued command: {} {:?}", user, name, args).blue())
        }
        LogEvent::Warning(msg) => println!("{}", format!("⚠️ {}", msg).red()),
        LogEvent::Error(msg) => eprintln!("{}", format!("❌ {}", msg).red().bold()),
    }
}
