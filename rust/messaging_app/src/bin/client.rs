// src/bin/client.rs
mod message;

use crate::message::Message;
use serde_json::{Deserializer, json};
use std::io::{self, BufRead, BufReader, BufWriter, Write};
use std::net::TcpStream;
use std::thread;

fn main() {
    let mut stream = TcpStream::connect("127.0.0.1:7878").unwrap();
    let mut writer = BufWriter::new(stream.try_clone().unwrap());
    println!("Connected to server!");

    // Prompt for username
    print!("Enter your username: ");
    io::Write::flush(&mut io::stdout()).unwrap();
    let mut username = String::new();
    io::stdin().read_line(&mut username).unwrap();
    let username = username.trim().to_string();

    // Send join message
    let join_msg = Message::Join { username: username.clone() };
    let encoded = serde_json::to_string(&join_msg).unwrap() + "\n";
    writer.write_all(encoded.as_bytes()).unwrap();

    // Spawn thread to listen for messages
    let stream_clone = stream.try_clone().unwrap();
    thread::spawn(move || {
        let reader = BufReader::new(stream_clone);
        let deserializer = Deserializer::from_reader(reader).into_iter::<Message>();
        for msg in deserializer {
            match msg {
                Ok(Message::Chat { from, text }) => println!("{}: {}", from, text),
                Ok(Message::Private { from, to: _, text }) => println!("[PM from {}]: {}", from, text),
                Ok(Message::System { text }) => println!("{}", text),
                Ok(Message::ListResponse { users }) => println!("*** Connected users: {} ***", users.join(", ")),
                Ok(other) => println!("Received: {:?}", other),
                Err(e) => {
                    eprintln!("Error decoding: {}", e);
                    break;
                }
            }
        }
    });

    // Main loop: read from stdin
    let stdin = io::stdin();
    for line in stdin.lock().lines() {
        let line = line.unwrap();

        let msg = if line.starts_with("/msg ") {
            let parts: Vec<&str> = line.splitn(3, ' ').collect();
            if parts.len() < 3 {
                Message::System { text: "Usage: /msg <user> <message>".into() }
            } else {
                Message::Private {
                    from: username.clone(),
                    to: parts[1].into(),
                    text: parts[2].into(),
                }
            }
        } else if line == "/list" {
            Message::ListRequest
        } else if line == "/help" {
            Message::Help
        } else if line == "/quit" {
            println!("Goodbye!");
            break; // closes loop → socket closes → server detects disconnect
        } else if line.starts_with("/rename ") {
            let parts: Vec<&str> = line.splitn(2, ' ').collect();
            if parts.len() < 2 {
                Message::System { text: "Usage: /rename <newname>".into() }
            } else {
                // Send a system "rename request"
                Message::System { text: format!("RENAME {}", parts[1]) }
            }
        } else {
            Message::Chat { from: username.clone(), text: line }
        };

        let encoded = serde_json::to_string(&msg).unwrap() + "\n";
        writer.write_all(encoded.as_bytes()).unwrap();
        writer.flush().unwrap();
    }
}
