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
use std::collections::{HashMap, HashSet};
use tokio::sync::mpsc as tokio_mpsc;

use crate::utils::{replace_emojis, get_username_style};

pub struct TuiClient {
    username: String,
    user_colors: HashMap<String, Color>,
    used_colors: HashSet<Color>,
    input_buffer: Arc<Mutex<String>>,
}

impl TuiClient {
    pub fn new(username: String) -> Self {
        Self {
            username,
            user_colors: HashMap::new(),
            used_colors: HashSet::new(),
            input_buffer: Arc::new(Mutex::new(String::new())),
        }
    }

    pub fn start(
        &mut self,
        tui_rx: std::sync::mpsc::Receiver<Line<'static>>,
        input_tx: tokio_mpsc::UnboundedSender<String>,
    ) -> anyhow::Result<()> {
        let username_clone = self.username.clone();
        let input_buffer_clone = Arc::clone(&self.input_buffer);
        let mut user_colors = self.user_colors.clone();
        let mut used_colors = self.used_colors.clone();

        let tui_handle = thread::spawn(move || -> anyhow::Result<()> {
            let mut stdout = std::io::stdout();
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

                // Resize handling
                if size.width != last_width {
                    let old_messages: Vec<Line> = wrapped_messages.drain(..).collect();
                    for line in old_messages {
                        let text = line.to_string();
                        let style = line.spans[0].style;
                        let mut start = 0;
                        while start < text.len() {
                            let end = (start + msg_area_width).min(text.len());
                            wrapped_messages.push(Line::from(Span::styled(
                                text[start..end].to_string(),
                                style,
                            )));
                            start += msg_area_width;
                        }
                    }
                    last_width = size.width;
                }

                // Collect new messages
                while let Ok(msg) = tui_rx.try_recv() {
                    let text = msg.to_string();
                    let style = msg.spans[0].style;
                    let mut start = 0;
                    while start < text.len() {
                        let end = (start + msg_area_width).min(text.len());
                        wrapped_messages.push(Line::from(Span::styled(
                            text[start..end].to_string(),
                            style,
                        )));
                        start += msg_area_width;
                    }
                    if auto_scroll {
                        scroll_offset = 0;
                    }
                }

                // Layout
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

                let messages_widget =
                    Paragraph::new(Text::from(display_lines.to_vec()))
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

                    f.set_cursor(
                        chunks[1].x + (cursor_pos - visible_start) as u16 + 1,
                        chunks[1].y + 1,
                    );
                })?;

                // Handle key events
                if event::poll(Duration::from_millis(100))? {
                    if let event::Event::Key(key) = event::read()? {
                        if key.kind != KeyEventKind::Press {
                            continue;
                        }

                        match key.code {
                            KeyCode::Char(c) => {
                                input.insert(cursor_pos, c);
                                cursor_pos += 1;
                                *input_buffer_clone.lock().unwrap() = input.clone();
                            }
                            KeyCode::Backspace => {
                                if cursor_pos > 0 {
                                    input.remove(cursor_pos - 1);
                                    cursor_pos -= 1;
                                }
                                *input_buffer_clone.lock().unwrap() = input.clone();
                            }
                            KeyCode::Delete => {
                                if cursor_pos < input.len() {
                                    input.remove(cursor_pos);
                                }
                                *input_buffer_clone.lock().unwrap() = input.clone();
                            }
                            KeyCode::Left => if cursor_pos > 0 { cursor_pos -= 1; }
                            KeyCode::Right => if cursor_pos < input.len() { cursor_pos += 1; }
                            KeyCode::Home => cursor_pos = 0,
                            KeyCode::End => cursor_pos = input.len(),
                            KeyCode::Enter => {
                                if !input.trim().is_empty() {
                                    let msg = replace_emojis(&input);
                                    let _ = input_tx.send(msg);
                                    input.clear();
                                    cursor_pos = 0;
                                    *input_buffer_clone.lock().unwrap() = String::new();
                                }
                            }
                            KeyCode::Esc => break,
                            KeyCode::Up | KeyCode::PageUp => {
                                scroll_offset = (scroll_offset + 1).min(max_scroll);
                                auto_scroll = false;
                            }
                            KeyCode::Down | KeyCode::PageDown => {
                                scroll_offset = scroll_offset.saturating_sub(1);
                                if scroll_offset == 0 {
                                    auto_scroll = true;
                                }
                            }
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
}
