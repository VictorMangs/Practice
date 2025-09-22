use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize, Debug, Clone)]
#[serde(tag = "type", rename_all = "lowercase")]
pub enum Message {
    Chat { from: String, text: String },
    Private { from: String, to: String, text: String },
    System { text: String },
    Command { name: String, args: Vec<String> },
}
