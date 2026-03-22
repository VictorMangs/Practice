use crossterm::event::{self, Event, KeyCode, MouseEventKind, EnableMouseCapture, DisableMouseCapture};
use crossterm::execute;
use crossterm::terminal::{Clear, ClearType};
use ratatui::{
    backend::CrosstermBackend,
    style::{Color, Modifier, Style},
    widgets::{Block, Borders, List, ListItem, ListState},
    Terminal,
};
use std::{
    fs::{self, File},
    io::{self, Write},
    path::{Path, PathBuf},
    process::Command,
};
use walkdir::WalkDir;
use zip::write::FileOptions;

fn main() -> io::Result<()> {
    // 1️⃣ Discover Rust projects
    let projects = discover_projects("..")?;
    if projects.is_empty() {
        println!("No valid Rust projects found in parent directories.");
        return Ok(());
    }

    // 2️⃣ Run TUI for project selection
    let selected = run_tui(&projects)?;
    println!("Selected project: {}", selected.display());

    // 3️⃣ Vendor dependencies (runs cargo update first)
    let vendor_success = match vendor(&selected) {
        Ok(_) => true,
        Err(_) => false,
    };

    // 4️⃣ Zip vendor folder only if vendoring succeeded
    let vendor_path = selected.join("vendor");
    let zip_file = selected.join("vendor.zip");

    if vendor_success && vendor_path.exists() {
        if let Err(e) = zip_dir(&vendor_path, &zip_file) {
            eprintln!("Warning: failed to zip vendor folder: {}", e);
        } else {
            println!("Vendor directory zipped at: {}", zip_file.display());
        }
    } else {
        println!("Vendoring failed or vendor folder missing. Skipping zip.");
    }

    // 5️⃣ Remove vendor folder in any case
    if vendor_path.exists() {
        if let Err(e) = fs::remove_dir_all(&vendor_path) {
            eprintln!("Warning: could not remove vendor folder: {}", e);
        } else {
            println!("Vendor folder removed after vendoring/zipping.");
        }
    }

    Ok(())
}

// Discover Rust projects
fn discover_projects(base: &str) -> io::Result<Vec<PathBuf>> {
    let mut projects = Vec::new();

    for entry in fs::read_dir(base)? {
        let entry = entry?;
        let path = entry.path();
        if path.is_dir() && path.join("Cargo.toml").exists() {
            let valid = Command::new("cargo")
                .arg("metadata")
                .arg("--no-deps")
                .current_dir(&path)
                .status()
                .map(|s| s.success())
                .unwrap_or(false);

            if valid {
                projects.push(path);
            }
        }
    }

    Ok(projects)
}

// Mouse-clickable project selection with Esc/q support
fn run_tui(projects: &[PathBuf]) -> io::Result<PathBuf> {
    let mut stdout = io::stdout();
    execute!(stdout, Clear(ClearType::All))?;
    crossterm::terminal::enable_raw_mode()?;
    execute!(stdout, EnableMouseCapture)?;

    let backend = CrosstermBackend::new(&mut stdout);
    let mut terminal = Terminal::new(backend)?;
    let mut state = ListState::default();
    state.select(Some(0));
    let mut selected_index = 0;

    loop {
        terminal.draw(|f| {
            let size = f.size();
            if size.height < 5 || size.width < 20 {
                return;
            }

            let items: Vec<ListItem> = projects
                .iter()
                .map(|p| {
                    let s = p.display().to_string();
                    let truncated = if s.len() > (size.width as usize - 6) {
                        format!("{}...", &s[..(size.width as usize - 9)])
                    } else {
                        s
                    };
                    ListItem::new(truncated)
                })
                .collect();

            let list = List::new(items)
                .block(
                    Block::default()
                        .borders(Borders::ALL)
                        .title("Select a project to vendor (q/Esc to quit)")
                        .border_style(Style::default().fg(Color::White)),
                )
                .highlight_style(
                    Style::default()
                        .bg(Color::Blue)
                        .add_modifier(Modifier::BOLD),
                )
                .highlight_symbol(">> ");

            f.render_stateful_widget(list, size, &mut state);
        })?;

        if let Event::Mouse(mouse_event) = event::read()? {
            if let MouseEventKind::Down(_) = mouse_event.kind {
                let row = mouse_event.row as usize;
                let clicked_index = row.saturating_sub(1);
                if clicked_index < projects.len() {
                    selected_index = clicked_index;
                    break; // exit TUI immediately
                }
            }
        }

        if let Event::Key(key) = event::read()? {
            match key.code {
                KeyCode::Up => {
                    if let Some(selected) = state.selected() {
                        let new_index = selected.saturating_sub(1);
                        state.select(Some(new_index));
                        selected_index = new_index;
                    }
                }
                KeyCode::Down => {
                    if let Some(selected) = state.selected() {
                        let new_index = (selected + 1).min(projects.len() - 1);
                        state.select(Some(new_index));
                        selected_index = new_index;
                    }
                }
                KeyCode::Enter => break,
                KeyCode::Char('q') | KeyCode::Esc => exit_tui(&mut terminal),
                _ => {}
            }
        }
    }

    // Clean up terminal immediately
    crossterm::terminal::disable_raw_mode()?;
    drop(terminal);
    execute!(io::stdout(), DisableMouseCapture, Clear(ClearType::All))?;

    Ok(projects[selected_index].clone())
}

// Exit function
fn exit_tui<B: ratatui::backend::Backend>(terminal: &mut Terminal<B>) -> ! {
    crossterm::terminal::disable_raw_mode().ok();
    drop(terminal);
    execute!(io::stdout(), DisableMouseCapture, Clear(ClearType::All)).ok();
    std::process::exit(0);
}

// Simplified vendoring: no progress bar, normal Cargo output
fn vendor(project: &Path) -> io::Result<()> {
    println!("Updating dependencies for: {}", project.display());

    let status = Command::new("cargo")
        .arg("update")
        .current_dir(project)
        .status()?;
    if !status.success() {
        eprintln!("cargo update failed!");
        return Err(io::Error::new(io::ErrorKind::Other, "cargo update failed"));
    }

    println!("Dependencies updated, starting vendoring...");

    let status = Command::new("cargo")
        .arg("vendor")
        .current_dir(project)
        .status()?;
    if !status.success() {
        eprintln!("cargo vendor failed!");
        return Err(io::Error::new(io::ErrorKind::Other, "cargo vendor failed"));
    }

    println!("Vendoring complete!");
    Ok(())
}

// Zip a directory recursively with safe strip_prefix
fn zip_dir(src_dir: &Path, zip_file: &Path) -> zip::result::ZipResult<()> {
    let file = File::create(zip_file)?;
    let mut zip = zip::ZipWriter::new(file);
    let options = FileOptions::default().compression_method(zip::CompressionMethod::Stored);

    for entry in WalkDir::new(src_dir).into_iter().filter_map(|e| e.ok()) {
        let path = entry.path();

        // Skip paths that can't be relativized
        let name = match path.strip_prefix(src_dir) {
            Ok(p) => p,
            Err(_) => continue,
        };

        if path.is_file() {
            zip.start_file(name.to_string_lossy(), options)?;
            let mut f = File::open(path)?;
            std::io::copy(&mut f, &mut zip)?;
        } else if !name.as_os_str().is_empty() {
            zip.add_directory(name.to_string_lossy(), options)?;
        }
    }

    zip.finish()?;
    Ok(())
}
