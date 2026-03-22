use serde::{Deserialize, Serialize};

/// Defines all types of messages exchanged between clients and the server.
/// Tagged enum allows Serde to encode `{"type":"chat",...}` cleanly.
#[derive(Serialize, Deserialize, Debug, Clone)]
#[serde(tag = "type", rename_all = "lowercase")]
pub enum Message {
    /// Sent when a user joins the chat.
    Join { username: String },

    /// Chat text message from one user to others.
    Chat { from: String, text: String },

    /// Internal or broadcast system messages.
    System { text: String },

    Command { name: String, args: Vec<String> },
}
