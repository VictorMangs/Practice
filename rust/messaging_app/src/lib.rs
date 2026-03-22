// src/lib.rs
// Tell Rust where the modules are
#[path = "modules/message.rs"]
pub mod message;
#[path = "modules/log_event.rs"]
pub mod log_event;
#[path = "modules/utils.rs"]
pub mod utils;
#[path = "modules/tui.rs"]
pub mod tui;
