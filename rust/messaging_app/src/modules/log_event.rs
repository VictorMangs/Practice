use std::{
    fs::OpenOptions,
    io::Write,
    sync::Mutex,
};
use once_cell::sync::Lazy;
use chrono::Local;

/// Global log file wrapped in a Mutex for thread-safe access
pub static LOG_FILE: Lazy<Mutex<Option<std::fs::File>>> = Lazy::new(|| Mutex::new(None));

/// Initialize the logger: opens `server.log` for appending
pub async fn init_logger() {
    let file = OpenOptions::new()
        .append(true)
        .create(true)
        .open("server.log")
        .expect("Failed to open server.log");

    *LOG_FILE.lock().unwrap() = Some(file);
}

/// Log a message to stdout and optionally to `server.log`
pub async fn log(message: &str) {
    // Prepend timestamp
    let timestamp = Local::now().format("%Y-%m-%d %H:%M:%S");
    let log_entry = format!("[{}] {}", timestamp, message);

    // Print to console
    println!("{}", log_entry);

    // Write to file
    if let Some(file) = &mut *LOG_FILE.lock().unwrap() {
        let _ = writeln!(file, "{}", log_entry);
        let _ = file.flush();
    }
}
