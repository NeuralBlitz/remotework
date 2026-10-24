use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs;
use std::path::PathBuf;
use std::sync::Mutex;
use tauri::{Manager, State};
use tracing::{error, info, warn};
use uuid::Uuid;
use chrono::{DateTime, Utc};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Command {
    pub name: String,
    pub description: String,
    pub category: String,
    pub args: Vec<Arg>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Arg {
    pub name: String,
    pub required: bool,
    pub default: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Plugin {
    pub id: String,
    pub name: String,
    pub version: String,
    pub description: String,
    pub author: String,
    pub enabled: bool,
    pub permissions: Vec<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AppState {
    pub initialized: bool,
    pub version: String,
    pub config_dir: PathBuf,
    pub data_dir: PathBuf,
}

impl Default for AppState {
    fn default() -> Self {
        Self {
            initialized: false,
            version: "1.0.0".to_string(),
            config_dir: dirs::config_dir().unwrap_or_else(|| PathBuf::from(".")).join("mito"),
            data_dir: dirs::data_dir().unwrap_or_else(|| PathBuf::from(".")).join("mito"),
        }
    }
}

pub struct MitoState {
    pub state: Mutex<AppState>,
    pub plugins: Mutex<HashMap<String, Plugin>>,
    pub commands: Mutex<Vec<Command>>,
}

impl Default for MitoState {
    fn default() -> Self {
        Self {
            state: Mutex::new(AppState::default()),
            plugins: Mutex::new(HashMap::new()),
            commands: Mutex::new(vec![
                Command {
                    name: "chat".to_string(),
                    description: "Interactive chat with LLM".to_string(),
                    category: "core".to_string(),
                    args: vec![
                        Arg { name: "model".to_string(), required: false, default: Some("gpt2".to_string()) },
                    ],
                },
                Command {
                    name: "textgen".to_string(),
                    description: "Generate text from prompt".to_string(),
                    category: "core".to_string(),
                    args: vec![
                        Arg { name: "prompt".to_string(), required: true, default: None },
                        Arg { name: "max_tokens".to_string(), required: false, default: Some("256".to_string()) },
                    ],
                },
                Command {
                    name: "sentiment".to_string(),
                    description: "Analyze sentiment of text".to_string(),
                    category: "nlp".to_string(),
                    args: vec![
                        Arg { name: "text".to_string(), required: true, default: None },
                    ],
                },
                Command {
                    name: "ocr".to_string(),
                    description: "Extract text from images".to_string(),
                    category: "vision".to_string(),
                    args: vec![
                        Arg { name: "image".to_string(), required: true, default: None },
                    ],
                },
                Command {
                    name: "classify".to_string(),
                    description: "Classify images".to_string(),
                    category: "vision".to_string(),
                    args: vec![
                        Arg { name: "image".to_string(), required: true, default: None },
                    ],
                },
                Command {
                    name: "embed".to_string(),
                    description: "Generate text embeddings".to_string(),
                    category: "nlp".to_string(),
                    args: vec![
                        Arg { name: "text".to_string(), required: true, default: None },
                    ],
                },
                Command {
                    name: "tts".to_string(),
                    description: "Convert text to speech".to_string(),
                    category: "speech".to_string(),
                    args: vec![
                        Arg { name: "text".to_string(), required: true, default: None },
                    ],
                },
                Command {
                    name: "translate".to_string(),
                    description: "Translate text".to_string(),
                    category: "nlp".to_string(),
                    args: vec![
                        Arg { name: "text".to_string(), required: true, default: None },
                        Arg { name: "target".to_string(), required: false, default: Some("en".to_string()) },
                    ],
                },
                Command {
                    name: "summarize".to_string(),
                    description: "Summarize text".to_string(),
                    category: "nlp".to_string(),
                    args: vec![
                        Arg { name: "text".to_string(), required: true, default: None },
                    ],
                },
                Command {
                    name: "qa".to_string(),
                    description: "Question answering".to_string(),
                    category: "nlp".to_string(),
                    args: vec![
                        Arg { name: "question".to_string(), required: true, default: None },
                        Arg { name: "context".to_string(), required: true, default: None },
                    ],
                },
                Command {
                    name: "detect".to_string(),
                    description: "Detect objects in images".to_string(),
                    category: "vision".to_string(),
                    args: vec![
                        Arg { name: "image".to_string(), required: true, default: None },
                    ],
                },
                Command {
                    name: "segment".to_string(),
                    description: "Segment images".to_string(),
                    category: "vision".to_string(),
                    args: vec![
                        Arg { name: "image".to_string(), required: true, default: None },
                    ],
                },
                Command {
                    name: "speech".to_string(),
                    description: "Speech recognition".to_string(),
                    category: "speech".to_string(),
                    args: vec![
                        Arg { name: "audio".to_string(), required: true, default: None },
                    ],
                },
                Command {
                    name: "rag".to_string(),
                    description: "RAG-based Q&A".to_string(),
                    category: "agents".to_string(),
                    args: vec![
                        Arg { name: "query".to_string(), required: true, default: None },
                    ],
                },
                Command {
                    name: "agent".to_string(),
                    description: "Execute agent task".to_string(),
                    category: "agents".to_string(),
                    args: vec![
                        Arg { name: "task".to_string(), required: true, default: None },
                    ],
                },
                Command {
                    name: "server".to_string(),
                    description: "Start API server".to_string(),
                    category: "server".to_string(),
                    args: vec![
                        Arg { name: "host".to_string(), required: false, default: Some("0.0.0.0".to_string()) },
                        Arg { name: "port".to_string(), required: false, default: Some("8000".to_string()) },
                    ],
                },
            ]),
        }
    }
}

#[tauri::command]
fn get_app_info(state: State<MitoState>) -> Result<HashMap<String, String>, String> {
    let app_state = state.state.lock().map_err(|e| e.to_string())?;
    let mut info = HashMap::new();
    info.insert("version".to_string(), app_state.version.clone());
    info.insert("name".to_string(), "Mito AI Toolkit".to_string());
    info.insert("description".to_string(), "The Powerhouse AI Toolkit".to_string());
    Ok(info)
}

#[tauri::command]
fn list_commands(state: State<MitoState>) -> Result<Vec<Command>, String> {
    let commands = state.commands.lock().map_err(|e| e.to_string())?;
    Ok(commands.clone())
}

#[tauri::command]
fn list_plugins(state: State<MitoState>) -> Result<Vec<Plugin>, String> {
    let plugins = state.plugins.lock().map_err(|e| e.to_string())?;
    Ok(plugins.values().cloned().collect())
}

#[tauri::command]
fn get_plugin(id: String, state: State<MitoState>) -> Result<Option<Plugin>, String> {
    let plugins = state.plugins.lock().map_err(|e| e.to_string())?;
    Ok(plugins.get(&id).cloned())
}

#[tauri::command]
fn enable_plugin(id: String, state: State<MitoState>) -> Result<(), String> {
    let mut plugins = state.plugins.lock().map_err(|e| e.to_string())?;
    if let Some(plugin) = plugins.get_mut(&id) {
        plugin.enabled = true;
        info!("Plugin enabled: {}", id);
        Ok(())
    } else {
        Err(format!("Plugin not found: {}", id))
    }
}

#[tauri::command]
fn disable_plugin(id: String, state: State<MitoState>) -> Result<(), String> {
    let mut plugins = state.plugins.lock().map_err(|e| e.to_string())?;
    if let Some(plugin) = plugins.get_mut(&id) {
        plugin.enabled = false;
        info!("Plugin disabled: {}", id);
        Ok(())
    } else {
        Err(format!("Plugin not found: {}", id))
    }
}

#[tauri::command]
fn register_plugin(
    name: String,
    version: String,
    description: String,
    author: String,
    permissions: Vec<String>,
    state: State<MitoState>,
) -> Result<Plugin, String> {
    let id = Uuid::new_v4().to_string();
    let plugin = Plugin {
        id: id.clone(),
        name: name.clone(),
        version,
        description,
        author,
        enabled: true,
        permissions,
    };
    
    let mut plugins = state.plugins.lock().map_err(|e| e.to_string())?;
    plugins.insert(id.clone(), plugin.clone());
    
    info!("Plugin registered: {} ({})", name, id);
    Ok(plugin)
}

#[tauri::command]
fn execute_command(
    command: String,
    args: HashMap<String, String>,
    state: State<MitoState>,
) -> Result<String, String> {
    info!("Executing command: {} with args: {:?}", command, args);
    
    let commands = state.commands.lock().map_err(|e| e.to_string())?;
    let cmd = commands.iter().find(|c| c.name == command);
    
    match cmd {
        Some(_) => {
            Ok(format!("Command '{}' would execute with args: {:?}", command, args))
        }
        None => Err(format!("Unknown command: {}", command)),
    }
}

#[tauri::command]
async fn run_mito_command(command: String, args: Vec<String>) -> Result<String, String> {
    info!("Running mito command: {} {:?}", command, args);
    
    let mut cmd_args = vec![command];
    cmd_args.extend(args);
    
    #[cfg(target_os = "windows")]
    {
        let output = std::process::Command::new("cmd")
            .args(["/C", "mito"])
            .args(&cmd_args)
            .output()
            .map_err(|e| e.to_string())?;
        
        Ok(String::from_utf8_lossy(&output.stdout).to_string())
    }
    
    #[cfg(not(target_os = "windows"))]
    {
        let output = std::process::Command::new("./mito")
            .args(&cmd_args)
            .output()
            .map_err(|e| e.to_string())?;
        
        Ok(String::from_utf8_lossy(&output.stdout).to_string())
    }
}

#[tauri::command]
fn get_config_dir(state: State<MitoState>) -> Result<String, String> {
    let app_state = state.state.lock().map_err(|e| e.to_string())?;
    Ok(app_state.config_dir.to_string_lossy().to_string())
}

#[tauri::command]
fn get_data_dir(state: State<MitoState>) -> Result<String, String> {
    let app_state = state.state.lock().map_err(|e| e.to_string())?;
    Ok(app_state.data_dir.to_string_lossy().to_string())
}

#[tauri::command]
fn log_event(level: String, message: String) -> Result<(), String> {
    match level.as_str() {
        "error" => error!("{}", message),
        "warn" => warn!("{}", message),
        _ => info!("{}", message),
    }
    Ok(())
}

pub fn init_logging() {
    use tracing_subscriber::{fmt, prelude::*, EnvFilter};
    
    let log_dir = dirs::data_dir()
        .unwrap_or_else(|| PathBuf::from("."))
        .join("mito")
        .join("logs");
    
    fs::create_dir_all(&log_dir).ok();
    
    let file_appender = tracing_appender::rolling::daily(&log_dir, "mito.log");
    let (non_blocking, _guard) = tracing_appender::non_blocking(file_appender);
    
    tracing_subscriber::registry()
        .with(EnvFilter::new("info"))
        .with(fmt::layer().with_writer(std::io::stdout))
        .with(fmt::layer().with_writer(non_blocking).with_ansi(false))
        .init();
    
    info!("Mito desktop application started");
    info!("Log directory: {:?}", log_dir);
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    init_logging();
    
    tauri::Builder::default()
        .manage(MitoState::default())
        .invoke_handler(tauri::generate_handler![
            get_app_info,
            list_commands,
            list_plugins,
            get_plugin,
            enable_plugin,
            disable_plugin,
            register_plugin,
            execute_command,
            run_mito_command,
            get_config_dir,
            get_data_dir,
            log_event,
        ])
        .setup(|app| {
            info!("Application setup complete");
            
            let app_handle = app.handle();
            let state: State<MitoState> = app_handle.state();
            let mut app_state = state.state.lock().unwrap();
            app_state.initialized = true;
            
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
