// src/message.rs
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize, Debug)]
#[serde(tag = "type")]
pub enum Message {
    Join { username: String },
    Chat { from: String, text: String },
    Private { from: String, to: String, text: String },
    ListRequest,
    ListResponse { users: Vec<String> },
    Help,
    System { text: String },
}
