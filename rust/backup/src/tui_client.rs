
use std::collections::{HashMap, HashSet, hash_map::DefaultHasher};
use std::hash::{Hash, Hasher};
use std::io::{self, Write};
use std::net::{IpAddr, UdpSocket};
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::Duration;

use crossterm::{
    event::{self, Event, KeyCode, KeyEventKind},
    execute,
    terminal::{disable_raw_mode, enable_raw_mode, EnterAlternateScreen, LeaveAlternateScreen},
};
use ratatui::{
    backend::CrosstermBackend,
    layout::{Constraint, Direction, Layout},
    style::{Color, Modifier, Style},
    text::{Line, Span, Text},
    widgets::{Block, Borders, Paragraph, Wrap},
    Terminal,
};

use tokio::io::{AsyncBufReadExt, AsyncWriteExt, BufReader};
use tokio::net::TcpStream;
use tokio::sync::mpsc as tokio_mpsc;

use crate::{log_event::log, message::Message};

const DISCOVERY_PORT: u16 = 8888;

// --- Safe bright colors for username backgrounds ---
const USER_COLORS: &[Color] = &[
    Color::Blue, Color::Green, Color::Red, Color::Magenta,
    Color::Cyan, Color::Yellow, Color::DarkGray, Color::Gray,
    Color::LightBlue, Color::LightGreen, Color::LightRed, Color::LightMagenta,
    Color::LightCyan, Color::LightYellow,
];

// --- Deterministic username style ---
pub fn get_username_style(
    username: &str,
    user_colors: &mut HashMap<String, Color>,
    used_colors: &mut HashSet<Color>,
) -> Style {
    if !user_colors.contains_key(username) {
        // Deterministic hash → initial preferred color
        let mut hasher = DefaultHasher::new();
        username.hash(&mut hasher);
        let mut index = (hasher.finish() as usize) % USER_COLORS.len();

        // Collision avoidance: find the next free color
        let mut attempts = 0;
        while used_colors.contains(&USER_COLORS[index]) && attempts < USER_COLORS.len() {
            index = (index + 1) % USER_COLORS.len();
            attempts += 1;
        }

        let color = USER_COLORS[index];
        used_colors.insert(color);
        user_colors.insert(username.to_string(), color);
    }

    Style::default()
        .fg(*user_colors.get(username).unwrap())
        .add_modifier(Modifier::BOLD)
}

// --- Emoji replacement helper ---
fn replace_emojis(text: &str) -> String {
    let mut map = HashMap::new();
    map.insert(":smile:", "😄");
    map.insert(":laugh:", "😂");
    map.insert(":sad:", "😢");
    map.insert(":thumbsup:", "👍");
    map.insert(":heart:", "❤️");
    map.insert(":fire:", "🔥");
    map.insert(":ok:", "👌");
    map.insert(":wave:", "👋");

    let mut result = text.to_string();
    for (k, v) in map {
        result = result.replace(k, v);
    }
    result
}

// --- Get local IP for fallback ---
fn get_local_ip() -> Option<IpAddr> {
    let socket = UdpSocket::bind("0.0.0.0:0").ok()?;
    socket.connect("8.8.8.8:80").ok()?;
    socket.local_addr().ok().map(|addr| addr.ip())
}

// --- Discover server via UDP broadcast ---
async fn discover_server() -> Option<String> {
    let socket = UdpSocket::bind("0.0.0.0:0").ok()?;
    socket.set_broadcast(true).ok()?;
    let broadcast_addr = format!("255.255.255.255:{}", DISCOVERY_PORT);
    let _ = socket.send_to(b"DISCOVER_CHAT_SERVER", &broadcast_addr).ok()?;

    let mut buf = [0u8; 1024];
    socket.set_read_timeout(Some(Duration::from_secs(2))).ok()?;
    if let Ok((len, addr)) = socket.recv_from(&mut buf) {
        let msg = String::from_utf8_lossy(&buf[..len]);
        if msg.starts_with("CHAT_SERVER:") {
            let tcp_port = &msg["CHAT_SERVER:".len()..];
            return Some(format!("{}:{}", addr.ip(), tcp_port));
        }
    }
    None
}

// --- Main client entry ---
pub async fn run_client(cli_server_addr: Option<&str>) -> anyhow::Result<()> {
    // --- Determine server address ---
    let server_addr = if let Some(addr) = cli_server_addr {
        log(&format!("Using server address from CLI: {}", addr)).await;
        addr.to_string()
    } else if let Some(addr) = discover_server().await {
        log(&format!("Discovered server at {}", addr)).await;
        addr
    } else {
        let default_ip = get_local_ip().unwrap_or_else(|| "127.0.0.1".parse().unwrap());
        let default_addr = format!("{}:8080", default_ip);
        log(&format!("Using default server address {}", default_addr)).await;
        default_addr
    };

    let stream = TcpStream::connect(&server_addr).await?;
    let (reader, mut writer) = stream.into_split();
    let mut reader = BufReader::new(reader).lines();

    let (tui_tx, tui_rx) = std::sync::mpsc::channel::<Line<'static>>();
    let (input_tx, mut input_rx) = tokio_mpsc::unbounded_channel::<String>();

    // --- Prompt for username, enforcing uniqueness ---
    let username = loop {
        let mut input_username = std::env::var("USER")
            .or_else(|_| std::env::var("LOGNAME"))
            .unwrap_or_else(|_| {
                print!("Enter username: ");
                io::stdout().flush().unwrap();
                let mut input = String::new();
                io::stdin().read_line(&mut input).unwrap();
                input.trim().to_string()
            });

        writer.write_all(format!("{}\n", input_username).as_bytes()).await?;
        writer.flush().await?;

        if let Some(line) = reader.next_line().await? {
            if let Ok(msg) = serde_json::from_str::<Message>(&line) {
                if let Message::System { text } = &msg {
                    if text.contains("already taken") {
                        println!("{}", text);
                        continue; // ask again
                    }
                }
            }
        }

        break input_username;
    };

    log(&format!("Connected as {}", username)).await;

    let input_buffer = Arc::new(Mutex::new(String::new()));
    let username_clone = username.clone();
    let input_buffer_clone = Arc::clone(&input_buffer);

    // --- Color tracking ---
    let mut user_colors: HashMap<String, Color> = HashMap::new();
    let mut used_colors: HashSet<Color> = HashSet::new();

    // --- Incoming messages ---
    {
        let tui_tx_clone = tui_tx.clone();
        let mut user_colors = user_colors.clone();
        let mut used_colors = used_colors.clone();

        tokio::spawn(async move {
            while let Ok(Some(line)) = reader.next_line().await {
                if let Ok(msg) = serde_json::from_str::<Message>(&line) {
                    let styled_line = match &msg {
                        Message::Chat { from, text } => {
                            let style = get_username_style(from, &mut user_colors, &mut used_colors);
                            Line::from(Span::styled(format!("{}: {}", from, text), style))
                        }
                        Message::System { text } => {
                            if text.ends_with("has left!") {
                                if let Some(left_user) = text.strip_suffix(" has left!") {
                                    if let Some(color) = user_colors.remove(left_user) {
                                        used_colors.remove(&color);
                                    }
                                }
                            }
                            Line::from(Span::styled(
                                format!("[System] {}", text),
                                Style::default().fg(Color::Yellow).add_modifier(Modifier::ITALIC),
                            ))
                        }
                        Message::Join { username } => {
                            let style = get_username_style(username, &mut user_colors, &mut used_colors);
                            Line::from(Span::styled(
                                format!("[System] {} has joined!", username),
                                style,
                            ))
                        }
                        Message::Command { .. } => continue,
                    };
                    let _ = tui_tx_clone.send(styled_line);
                }
            }
        });
    }

    // --- Outgoing messages ---
    {
        let mut writer_clone = writer;
        tokio::spawn(async move {
            while let Some(msg) = input_rx.recv().await {
                let _ = writer_clone.write_all(format!("{}\n", msg).as_bytes()).await;
                let _ = writer_clone.flush().await;
            }
        });
    }

    // --- TUI thread ---
    let tui_handle = thread::spawn(move || -> anyhow::Result<()> {
        let mut stdout = io::stdout();
        enable_raw_mode()?;
        execute!(stdout, EnterAlternateScreen)?;
        let backend = CrosstermBackend::new(stdout);
        let mut terminal = Terminal::new(backend)?;
        terminal.clear()?;

        let mut input = String::new();
        let mut cursor_pos: usize = 0;
        let mut wrapped_messages: Vec<Line> = Vec::new();
        let mut scroll_offset: usize = 0;
        let mut auto_scroll = true;
        let mut last_width = terminal.size()?.width;

        loop {
            let size = terminal.size()?;
            let msg_area_width = size.width.saturating_sub(4) as usize;

            // --- Resize handling ---
            if size.width != last_width {
                let old_messages: Vec<Line> = wrapped_messages.drain(..).collect();
                for line in old_messages {
                    let text = line.to_string();
                    let style = line.spans[0].style;
                    let mut start = 0;
                    while start < text.len() {
                        let end = (start + msg_area_width).min(text.len());
                        wrapped_messages.push(Line::from(Span::styled(text[start..end].to_string(), style)));
                        start += msg_area_width;
                    }
                }
                last_width = size.width;
            }

            // --- Collect new messages ---
            while let Ok(msg) = tui_rx.try_recv() {
                let text = msg.to_string();
                let style = msg.spans[0].style;
                let mut start = 0;
                while start < text.len() {
                    let end = (start + msg_area_width).min(text.len());
                    wrapped_messages.push(Line::from(Span::styled(text[start..end].to_string(), style)));
                    start += msg_area_width;
                }
                if auto_scroll { scroll_offset = 0; }
            }

            // --- Layout ---
            let chunks = Layout::default()
                .direction(Direction::Vertical)
                .margin(1)
                .constraints([Constraint::Min(1), Constraint::Length(3)].as_ref())
                .split(ratatui::layout::Rect::new(0, 0, size.width, size.height));

            let msg_area = chunks[0];
            let page_height = msg_area.height.saturating_sub(2) as usize;
            let total_wrapped = wrapped_messages.len();
            let max_scroll = total_wrapped.saturating_sub(page_height);
            let scroll = scroll_offset.min(max_scroll);
            let start_idx = total_wrapped.saturating_sub(page_height + scroll);
            let end_idx = total_wrapped.saturating_sub(scroll);
            let display_lines = &wrapped_messages[start_idx..end_idx];

            let messages_widget = Paragraph::new(Text::from(display_lines.to_vec()))
                .block(Block::default().title("Messages").borders(Borders::ALL))
                .wrap(Wrap { trim: true });

            terminal.draw(|f| {
                f.render_widget(messages_widget, msg_area);

                let input_width = chunks[1].width.saturating_sub(4) as usize;
                let visible_start = cursor_pos.saturating_sub(input_width.saturating_sub(1));
                let visible_end = (visible_start + input.len()).min(input.len());
                let visible_str = &input[visible_start..visible_end];

                let input_widget = Paragraph::new(visible_str.to_string())
                    .block(Block::default().title(format!("{} >", username_clone)).borders(Borders::ALL));
                f.render_widget(input_widget, chunks[1]);

                f.set_cursor(chunks[1].x + (cursor_pos - visible_start) as u16 + 1, chunks[1].y + 1);
            })?;

            // --- Handle key events ---
            if event::poll(Duration::from_millis(100))? {
                if let Event::Key(key) = event::read()? {
                    if key.kind != KeyEventKind::Press { continue; }

                    match key.code {
                        KeyCode::Char(c) => {
                            input.insert(cursor_pos, c);
                            cursor_pos += 1;
                            *input_buffer_clone.lock().unwrap() = input.clone();
                        }
                        KeyCode::Backspace => { if cursor_pos>0 { input.remove(cursor_pos-1); cursor_pos-=1; } *input_buffer_clone.lock().unwrap() = input.clone(); }
                        KeyCode::Delete => { if cursor_pos<input.len() { input.remove(cursor_pos); } *input_buffer_clone.lock().unwrap() = input.clone(); }
                        KeyCode::Left => if cursor_pos>0 { cursor_pos-=1; }
                        KeyCode::Right => if cursor_pos<input.len() { cursor_pos+=1; }
                        KeyCode::Home => cursor_pos=0,
                        KeyCode::End => cursor_pos=input.len(),
                        KeyCode::Enter => {
                            if !input.trim().is_empty() {
                                let chat_msg = Message::Chat { from: username_clone.clone(), text: replace_emojis(&input) };
                                let _ = input_tx.send(serde_json::to_string(&chat_msg)?);
                                input.clear();
                                cursor_pos=0;
                                *input_buffer_clone.lock().unwrap()=String::new();
                            }
                        }
                        KeyCode::Esc => break,
                        KeyCode::Up|KeyCode::PageUp => { scroll_offset=(scroll_offset+1).min(max_scroll); auto_scroll=false; }
                        KeyCode::Down|KeyCode::PageDown => { scroll_offset=scroll_offset.saturating_sub(1); if scroll_offset==0{auto_scroll=true;} }
                        _ => {}
                    }
                }
            }
        }

        disable_raw_mode()?;
        execute!(terminal.backend_mut(), LeaveAlternateScreen)?;
        terminal.show_cursor()?;
        Ok(())
    });

    tui_handle.join().unwrap()?;
    Ok(())
}
