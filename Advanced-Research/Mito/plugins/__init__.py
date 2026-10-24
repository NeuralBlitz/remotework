"""
Mito Enterprise Plugin System
Massive plugin architecture with security, events, and lifecycle management
"""

from typing import Dict, Any, List, Optional, Callable, Type, Set
from dataclasses import dataclass, field
from pathlib import Path
from enum import Enum
import importlib.util
import json
import hashlib
import logging
from datetime import datetime
import asyncio
import aiohttp


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mito.plugins")


class PluginState(Enum):
    DISCOVERED = "discovered"
    INSTALLED = "installed"
    ENABLED = "enabled"
    DISABLED = "disabled"
    ERROR = "error"
    UPDATING = "updating"


class Permission(Enum):
    READ_FILES = "read_files"
    WRITE_FILES = "write_files"
    EXECUTE_COMMANDS = "execute_commands"
    NETWORK_ACCESS = "network_access"
    READ_ENV = "read_env"
    MODIFY_SETTINGS = "modify_settings"
    ACCESS_PLUGINS = "access_plugins"
    ADMIN = "admin"


@dataclass
class PluginMetadata:
    name: str
    version: str
    description: str
    author: str
    license: str = "MIT"
    homepage: str = ""
    repository: str = ""
    tags: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    permissions: List[str] = field(default_factory=list)
    min_mito_version: str = "1.0.0"
    checksum: str = ""


@dataclass
class PluginInfo:
    metadata: PluginMetadata
    state: PluginState = PluginState.DISCOVERED
    installed_at: Optional[datetime] = None
    enabled_at: Optional[datetime] = None
    error_message: str = ""


class PluginHook:
    def __init__(self, name: str, priority: int = 0):
        self.name = name
        self.priority = priority
        self.callbacks: List[Callable] = []
    
    def register(self, callback: Callable):
        self.callbacks.append(callback)
        self.callbacks.sort(key=lambda x: self.priority, reverse=True)
    
    def unregister(self, callback: Callable):
        if callback in self.callbacks:
            self.callbacks.remove(callback)
    
    async def emit(self, *args, **kwargs):
        results = []
        for callback in self.callbacks:
            try:
                result = callback(*args, **kwargs)
                if asyncio.iscoroutine(result):
                    result = await result
                results.append(result)
            except Exception as e:
                logger.error(f"Hook {self.name} error: {e}")
        return results


class EventBus:
    def __init__(self):
        self.hooks: Dict[str, PluginHook] = {}
    
    def subscribe(self, event: str, callback: Callable, priority: int = 0):
        if event not in self.hooks:
            self.hooks[event] = PluginHook(event, priority)
        self.hooks[event].register(callback)
    
    def unsubscribe(self, event: str, callback: Callable):
        if event in self.hooks:
            self.hooks[event].unregister(callback)
    
    async def publish(self, event: str, *args, **kwargs):
        if event in self.hooks:
            return await self.hooks[event].emit(*args, **kwargs)
        return []


class SecuritySandbox:
    def __init__(self):
        self.allowed_modules: Set[str] = {
            "os", "sys", "json", "math", "random", "datetime",
            "pathlib", "typing", "collections", "itertools"
        }
        self.denied_paths: Set[str] = {"/etc", "/root", "/home/runner/workspace/.git"}
    
    def check_permission(self, plugin: 'Plugin', permission: Permission) -> bool:
        perm_str = permission.value
        if perm_str in plugin.metadata.permissions:
            return True
        return perm_str == Permission.READ_FILES.value
    
    def check_module(self, module_name: str) -> bool:
        return module_name in self.allowed_modules
    
    def check_path(self, path: str) -> bool:
        for denied in self.denied_paths:
            if path.startswith(denied):
                return False
        return True


@dataclass
class PluginDependency:
    name: str
    version: str
    optional: bool = False


class DependencyResolver:
    def __init__(self):
        self.graph: Dict[str, List[PluginDependency]] = {}
    
    def add_plugin(self, name: str, dependencies: List[PluginDependency]):
        self.graph[name] = dependencies
    
    def resolve(self, plugin_name: str) -> List[str]:
        visited = set()
        result = []
        
        def visit(name: str):
            if name in visited:
                return
            visited.add(name)
            
            for dep in self.graph.get(name, []):
                if dep.name in self.graph:
                    visit(dep.name)
            
            result.append(name)
        
        visit(plugin_name)
        return result
    
    def check_conflicts(self, plugins: List[str]) -> List[str]:
        conflicts = []
        for i, p1 in enumerate(plugins):
            for p2 in plugins[i+1:]:
                deps1 = {d.name: d.version for d in self.graph.get(p1, [])}
                deps2 = {d.name: d.version for d in self.graph.get(p2, [])}
                
                for dep_name in set(deps1.keys()) & set(deps2.keys()):
                    if deps1[dep_name] != deps2[dep_name]:
                        conflicts.append(f"{p1} and {p2} conflict on {dep_name}")
        
        return conflicts


class Plugin:
    def __init__(self, metadata: PluginMetadata):
        self.metadata = metadata
        self.info = PluginInfo(metadata=metadata)
        self.commands: Dict[str, Callable] = {}
        self.hooks: Dict[str, Callable] = {}
        self.resources: Dict[str, Any] = {}
        self._instance = None
    
    def register_command(self, name: str, func: Callable):
        self.commands[name] = func
    
    def register_hook(self, event: str, callback: Callable):
        self.hooks[event] = callback
    
    def set_resource(self, key: str, value: Any):
        self.resources[key] = value
    
    def get_resource(self, key: str) -> Any:
        return self.resources.get(key)
    
    def enable(self):
        self.info.state = PluginState.ENABLED
        self.info.enabled_at = datetime.now()
        logger.info(f"Plugin {self.metadata.name} enabled")
    
    def disable(self):
        self.info.state = PluginState.DISABLED
        self.info.enabled_at = None
        logger.info(f"Plugin {self.metadata.name} disabled")
    
    def set_error(self, message: str):
        self.info.state = PluginState.ERROR
        self.info.error_message = message
        logger.error(f"Plugin {self.metadata.name} error: {message}")


class PluginLifecycle:
    def __init__(self, plugin: Plugin):
        self.plugin = plugin
    
    async def on_install(self):
        logger.info(f"Installing plugin: {self.plugin.metadata.name}")
        self.plugin.info.state = PluginState.INSTALLED
        self.plugin.info.installed_at = datetime.now()
    
    async def on_uninstall(self):
        logger.info(f"Uninstalling plugin: {self.plugin.metadata.name}")
        self.plugin.info.state = PluginState.DISCOVERED
        self.plugin.info.installed_at = None
    
    async def on_enable(self):
        self.plugin.enable()
    
    async def on_disable(self):
        self.plugin.disable()
    
    async def on_update(self, old_version: str):
        logger.info(f"Updating plugin {self.plugin.metadata.name} from {old_version} to {self.plugin.metadata.version}")
        self.plugin.info.state = PluginState.UPDATING


class PluginRepository:
    def __init__(self, cache_dir: str = "plugins/.cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.manifest_url = "https://plugins.mito.ai/manifest.json"
    
    async def fetch_manifest(self) -> List[PluginMetadata]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.manifest_url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return [PluginMetadata(**p) for p in data.get("plugins", [])]
        except Exception as e:
            logger.warning(f"Could not fetch manifest: {e}")
        
        return self._get_local_manifest()
    
    def _get_local_manifest(self) -> List[PluginMetadata]:
        manifest_file = self.cache_dir / "manifest.json"
        if manifest_file.exists():
            with open(manifest_file) as f:
                data = json.load(f)
                return [PluginMetadata(**p) for p in data.get("plugins", [])]
        return []
    
    async def download_plugin(self, metadata: PluginMetadata) -> Path:
        cache_file = self.cache_dir / f"{metadata.name}-{metadata.version}.py"
        
        if cache_file.exists():
            return cache_file
        
        url = f"https://plugins.mito.ai/download/{metadata.name}/{metadata.version}"
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        content = await resp.read()
                        with open(cache_file, "wb") as f:
                            f.write(content)
                        return cache_file
        except Exception as e:
            logger.error(f"Failed to download plugin {metadata.name}: {e}")
        
        raise FileNotFoundError(f"Could not download {metadata.name}")
    
    def verify_checksum(self, path: Path, expected: str) -> bool:
        with open(path, "rb") as f:
            actual = hashlib.sha256(f.read()).hexdigest()
        return actual == expected


class PluginManager:
    def __init__(self, plugin_dir: str = "plugins"):
        self.plugin_dir = Path(plugin_dir)
        self.plugins: Dict[str, Plugin] = {}
        self.command_registry: Dict[str, Callable] = {}
        self.event_bus = EventBus()
        self.security = SecuritySandbox()
        self.dependency_resolver = DependencyResolver()
        self.repository = PluginRepository()
        self.lifecycle_handlers: Dict[str, Callable] = {}
        
        self._register_default_hooks()
    
    def _register_default_hooks(self):
        self.event_bus.subscribe("plugin.enabled", self._on_plugin_enabled)
        self.event_bus.subscribe("plugin.disabled", self._on_plugin_disabled)
        self.event_bus.subscribe("command.executed", self._on_command_executed)
    
    async def _on_plugin_enabled(self, plugin: Plugin):
        logger.info(f"Plugin enabled: {plugin.metadata.name}")
    
    async def _on_plugin_disabled(self, plugin: Plugin):
        logger.info(f"Plugin disabled: {plugin.metadata.name}")
    
    async def _on_command_executed(self, command: str, result: Any):
        logger.debug(f"Command executed: {command}")
    
    def discover_plugins(self) -> List[Plugin]:
        if not self.plugin_dir.exists():
            self.plugin_dir.mkdir(parents=True)
            return []
        
        discovered = []
        
        for path in self.plugin_dir.glob("*.py"):
            if path.stem.startswith("_"):
                continue
            
            plugin = self._load_plugin(path)
            if plugin:
                discovered.append(plugin)
                self.plugins[plugin.metadata.name] = plugin
        
        return discovered
    
    def _load_plugin(self, path: Path) -> Optional[Plugin]:
        spec = importlib.util.spec_from_file_location(path.stem, path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            try:
                spec.loader.exec_module(module)
            except Exception as e:
                logger.error(f"Failed to load plugin from {path}: {e}")
                return None
            
            if hasattr(module, "PLUGIN_METADATA"):
                metadata = module.PLUGIN_METADATA
                plugin = Plugin(metadata)
                
                if hasattr(module, "register"):
                    try:
                        module.register(plugin)
                    except Exception as e:
                        logger.error(f"Failed to register plugin: {e}")
                        return None
                
                return plugin
        
        return None
    
    def register_lifecycle_handler(self, event: str, handler: Callable):
        self.lifecycle_handlers[event] = handler
    
    async def install_plugin(self, name: str, version: str, description: str, 
                            author: str, permissions: List[str] = None) -> Plugin:
        metadata = PluginMetadata(
            name=name,
            version=version,
            description=description,
            author=author,
            permissions=permissions or []
        )
        
        plugin = Plugin(metadata)
        lifecycle = PluginLifecycle(plugin)
        await lifecycle.on_install()
        
        self.plugins[name] = plugin
        self.dependency_resolver.add_plugin(
            name, 
            [PluginDependency(d) for d in metadata.dependencies]
        )
        
        return plugin
    
    async def uninstall_plugin(self, name: str):
        if name in self.plugins:
            plugin = self.plugins[name]
            lifecycle = PluginLifecycle(plugin)
            await lifecycle.on_uninstall()
            
            if name in self.plugins:
                await self.disable_plugin(name)
            del self.plugins[name]
    
    async def enable_plugin(self, name: str):
        if name not in self.plugins:
            raise ValueError(f"Plugin not found: {name}")
        
        plugin = self.plugins[name]
        
        deps = self.dependency_resolver.resolve(name)
        for dep in deps[:-1]:
            if dep in self.plugins and self.plugins[dep].info.state != PluginState.ENABLED:
                await self.enable_plugin(dep)
        
        lifecycle = PluginLifecycle(plugin)
        await lifecycle.on_enable()
        
        for cmd_name, cmd_func in plugin.commands.items():
            self.command_registry[cmd_name] = cmd_func
        
        await self.event_bus.publish("plugin.enabled", plugin)
    
    async def disable_plugin(self, name: str):
        if name not in self.plugins:
            return
        
        plugin = self.plugins[name]
        lifecycle = PluginLifecycle(plugin)
        await lifecycle.on_disable()
        
        for cmd_name in plugin.commands.keys():
            if cmd_name in self.command_registry:
                del self.command_registry[cmd_name]
        
        await self.event_bus.publish("plugin.disabled", plugin)
    
    async def update_plugin(self, name: str):
        if name not in self.plugins:
            raise ValueError(f"Plugin not found: {name}")
        
        plugin = self.plugins[name]
        old_version = plugin.metadata.version
        lifecycle = PluginLifecycle(plugin)
        await lifecycle.on_update(old_version)
    
    def execute_command(self, command: str, **kwargs) -> Any:
        if command in self.command_registry:
            result = self.command_registry[command](**kwargs)
            asyncio.create_task(self.event_bus.publish("command.executed", command, result))
            return result
        
        raise ValueError(f"Command '{command}' not found")
    
    def list_commands(self) -> Dict[str, str]:
        return {name: cmd.__doc__ or "" for name, cmd in self.command_registry.items()}
    
    def get_plugin_info(self, name: str) -> Optional[PluginInfo]:
        if name in self.plugins:
            return self.plugins[name].info
        return None
    
    def list_plugins(self, state: PluginState = None) -> List[Plugin]:
        if state:
            return [p for p in self.plugins.values() if p.info.state == state]
        return list(self.plugins.values())


def create_plugin_metadata(
    name: str,
    version: str,
    description: str,
    author: str,
    permissions: List[str] = None,
    dependencies: List[str] = None,
    **kwargs
) -> PluginMetadata:
    return PluginMetadata(
        name=name,
        version=version,
        description=description,
        author=author,
        permissions=permissions or [],
        dependencies=dependencies or [],
        **kwargs
    )


EXAMPLE_PLUGIN = '''
from mito.plugins import create_plugin_metadata, Plugin

PLUGIN_METADATA = create_plugin_metadata(
    name="example",
    version="1.0.0",
    description="Example enterprise plugin",
    author="Mito Team",
    permissions=["read_files", "network_access"],
    dependencies=["core-utils"]
)

def example_command(**kwargs):
    return "Hello from enterprise plugin!"

def example_hook(data):
    print(f"Hook received: {data}")
    return data

def register(plugin: Plugin):
    plugin.register_command("example_command", example_command)
    plugin.register_hook("pre_process", example_hook)
'''


if __name__ == '__main__':
    manager = PluginManager()
    plugins = manager.discover_plugins()
    print(f"Discovered {len(plugins)} plugins")
