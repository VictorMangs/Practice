use std::collections::{HashMap, HashSet};
use std::collections::hash_map::DefaultHasher;
use std::hash::{Hash, Hasher};
use std::net::UdpSocket;
use ratatui::style::{Color, Style, Modifier};

const USER_COLORS: &[Color] = &[
    Color::Blue, Color::Green, Color::Red, Color::Magenta,
    Color::Cyan, Color::Yellow, Color::DarkGray, Color::Gray,
    Color::LightBlue, Color::LightGreen, Color::LightRed,
    Color::LightMagenta, Color::LightCyan, Color::LightYellow,
];

pub fn get_username_style(
    username: &str,
    user_colors: &mut HashMap<String, Color>,
    used_colors: &mut HashSet<Color>,
) -> Style {
    if !user_colors.contains_key(username) {
        let mut hasher = DefaultHasher::new();
        username.hash(&mut hasher);
        let mut index = (hasher.finish() as usize) % USER_COLORS.len();

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

pub fn replace_emojis(text: &str) -> String {
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

pub fn get_local_ip() -> Option<std::net::IpAddr> {
    let socket = UdpSocket::bind("0.0.0.0:0").ok()?;
    socket.connect("8.8.8.8:80").ok()?;
    socket.local_addr().ok().map(|addr| addr.ip())
}
