// src/bin/server.rs
mod message;

use crate::message::Message;
use serde_json::{Deserializer, json};
use std::io::{BufReader, BufWriter, Write};
use std::net::{TcpListener, TcpStream};
use std::sync::{Arc, Mutex};
use std::thread;

struct Client {
    username: String,
    stream: TcpStream,
}

fn handle_client(stream: TcpStream, clients: Arc<Mutex<Vec<Client>>>) {
    let reader = BufReader::new(stream.try_clone().unwrap());
    let mut deserializer = Deserializer::from_reader(reader).into_iter::<Message>();

    // Expect first message = Join
    let join_msg = match deserializer.next() {
        Some(Ok(Message::Join { username })) => username,
        _ => return,
    };

    let mut username = join_msg.clone();
    {
        let mut clients_guard = clients.lock().unwrap();
        clients_guard.push(Client {
            username: username.clone(),
            stream: stream.try_clone().unwrap(),
        });
    }

    println!("{} joined the chat", username);
    broadcast(&clients, &Message::System { text: format!("*** {} joined ***", username) });

    for msg in deserializer {
        match msg {
            Ok(Message::Chat { from, text }) => {
                broadcast(&clients, &Message::Chat { from, text });
            }
            Ok(Message::Private { from, to, text }) => {
                let from_clone = from.clone();
                if !send_to_user(&clients, &to, &Message::Private { from, to: to.clone(), text }) {
                    send_to_user(
                        &clients,
                        &from_clone,
                        &Message::System { text: format!("User '{}' not found", to) },
                    );
                }
            }
            Ok(Message::ListRequest) => {
                let clients_guard = clients.lock().unwrap();
                let users: Vec<String> = clients_guard.iter().map(|c| c.username.clone()).collect();
                send_to_user(&clients, &username, &Message::ListResponse { users });
            }
            Ok(Message::Help) => {
                let help_msg = Message::System {
                    text: "Commands:\n/list\n/msg <user> <text>\n/help".into(),
                };
                send_to_user(&clients, &username, &help_msg);
            }
             Ok(Message::Join { .. }) => {
                // Shouldn't normally happen after first Join, but we can ignore
                eprintln!("{} tried to re-join", username);
            }
            Ok(Message::ListResponse { .. }) => {
                // Server never expects this; clients shouldn't send it.
                eprintln!("Unexpected ListResponse from client {}", username);
            }
            Ok(Message::System { text }) => {
                if text == "QUIT" {
                    println!("{} disconnected", username);
                    broadcast(&clients, &Message::System { text: format!("*** {} left ***", username) });
                    break; // exit loop → client removed after
                } else if text.starts_with("RENAME ") {
                    let new_name = text.trim_start_matches("RENAME ").to_string();
                    let mut clients_guard = clients.lock().unwrap();

                    // Check if new name is taken
                    if clients_guard.iter().any(|c| c.username == new_name) {
                        send_to_user(&clients, &username,
                            &Message::System { text: "Username already taken".into() });
                    } else {
                        // Update name
                        for client in clients_guard.iter_mut() {
                            if client.username == username {
                                client.username = new_name.clone();
                                break;
                            }
                        }
                        broadcast(&clients,
                            &Message::System { text: format!("*** {} is now known as {} ***", username, new_name) });
                        // Also update local `username` variable
                        // NOTE: needs mutable binding
                        username = new_name;
                    }
                } else {
                    eprintln!("Unexpected system text from {}: {}", username, text);
                }
            }
            Err(e) => {
                eprintln!("Error decoding message: {}", e);
                break;
            }
        }
    }

    println!("{} disconnected", username);
    broadcast(&clients, &Message::System { text: format!("*** {} left ***", username) });
    let mut clients_guard = clients.lock().unwrap();
    clients_guard.retain(|c| c.username != username);
}

fn broadcast(clients: &Arc<Mutex<Vec<Client>>>, message: &Message) {
    let mut clients_guard = clients.lock().unwrap();
    let encoded = serde_json::to_string(message).unwrap() + "\n";
    for client in clients_guard.iter_mut() {
        let mut writer = BufWriter::new(&client.stream);
        if let Err(e) = writer.write_all(encoded.as_bytes()) {
            eprintln!("Failed to send to {}: {}", client.username, e);
        }
    }
}

fn send_to_user(clients: &Arc<Mutex<Vec<Client>>>, target: &str, message: &Message) -> bool {
    let mut clients_guard = clients.lock().unwrap();
    let encoded = serde_json::to_string(message).unwrap() + "\n";
    for client in clients_guard.iter_mut() {
        if client.username == target {
            let mut writer = BufWriter::new(&client.stream);
            if let Err(e) = writer.write_all(encoded.as_bytes()) {
                eprintln!("Failed to send private message to {}: {}", target, e);
            }
            return true;
        }
    }
    false
}

fn main() {
    let listener = TcpListener::bind("127.0.0.1:7878").unwrap();
    println!("Server running on 127.0.0.1:7878");

    let clients: Arc<Mutex<Vec<Client>>> = Arc::new(Mutex::new(Vec::new()));

    for stream in listener.incoming() {
        match stream {
            Ok(stream) => {
                let clients_clone = Arc::clone(&clients);
                thread::spawn(move || handle_client(stream, clients_clone));
            }
            Err(e) => println!("Connection failed: {}", e),
        }
    }
}
