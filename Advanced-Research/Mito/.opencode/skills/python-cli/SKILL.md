---
name: python-cli
description: Building CLI applications with Python Click and Typer
license: MIT
metadata:
  audience: python-developers
  category: cli-development
---

# Skill: Python CLI (Click & Typer)

## What I do
Build production-ready command-line interface applications using Python's most popular CLI frameworks - Click for maximum control and Typer for Pythonic type-hint-based development.

## When to use me
When building CLI tools, command-line utilities, automation scripts, or any Python application that needs to accept command-line arguments and options.

## Click vs Typer

| Feature | Click | Typer |
|---------|-------|-------|
| API Style | Decorators | Type Hints |
| Boilerplate | More | Less |
| Type Safety | Manual | Automatic |
| Completions | Manual | Built-in |
| Built On | - | Click |

## Click Framework

### Installation
```bash
pip install click rich
```

### Basic Command
```python
import click
from rich.console import Console

console = Console()

@click.command()
@click.option("--name", default="World", help="Name to greet")
@click.option("--loud", is_flag=True, help="Shout the greeting")
def hello(name, loud):
    """A simple greeting command."""
    greeting = f"Hello, {name}!"
    if loud:
        greeting = greeting.upper()
    console.print(greeting, style="bold green")

if __name__ == "__main__":
    hello()
```

### With Subcommands
```python
import click

@click.group()
@click.version_option(version="1.0.0")
def cli():
    """My awesome CLI application."""
    pass

@cli.group()
def config():
    """Manage configuration."""
    pass

@config.command("set")
@click.option("--key", required=True)
@click.option("--value", required=True)
def config_set(key, value):
    """Set a configuration value."""
    click.echo(f"Setting {key} = {value}")

@config.command("get")
@click.argument("key")
def config_get(key):
    """Get a configuration value."""
    click.echo(f"Getting {key}")

@cli.command()
@click.argument("files", nargs=-1, type=click.Path())
@click.option("--verbose", "-v", count=True)
def process(files, verbose):
    """Process files with optional verbosity."""
    for f in files:
        click.echo(f"Processing: {f}")
    if verbose:
        click.echo(f"[debug] Verbosity level: {verbose}")
```

### Prompts & Confirmations
```python
@click.command()
def setup():
    """Interactive setup wizard."""
    name = click.prompt("Enter your name", type=str)
    age = click.prompt("Enter your age", type=int, default=18)
    
    if click.confirm("Continue with setup?"):
        click.echo(f"Welcome, {name}!")
    else:
        click.echo("Setup cancelled.")
        raise SystemExit(0)
```

### Progress Bars
```python
import time

@click.command()
@click.option("--count", default=10)
def task(count):
    """Process items with progress bar."""
    with click.progressbar(range(count), label="Processing") as bar:
        for i in bar:
            time.sleep(0.1)
```

### Rich Integration
```python
import click
from rich.console import Console
from rich.table import Table
from rich.progress import Progress

console = Console()

@click.command()
def list_users():
    """Display users in a formatted table."""
    users = [
        {"name": "Alice", "role": "admin", "active": True},
        {"name": "Bob", "role": "user", "active": False},
    ]
    
    table = Table(title="Users")
    table.add_column("Name", style="cyan")
    table.add_column("Role", style="magenta")
    table.add_column("Status", style="green")
    
    for user in users:
        status = "[green]Active[/green]" if user["active"] else "[red]Inactive[/red]"
        table.add_row(user["name"], user["role"], status)
    
    console.print(table)
```

## Typer Framework

### Installation
```bash
pip install typer[all] rich
```

### Basic Command
```python
import typer
from typing import Optional

app = typer.Typer(
    name="myapp",
    help="My awesome CLI application",
    rich_markup_mode="rich"
)

@app.command()
def hello(name: str = "World", loud: bool = False):
    """[bold green]Greet[/bold green] someone by name."""
    greeting = f"Hello, {name}!"
    if loud:
        greeting = greeting.upper()
    typer.echo(greeting)

if __name__ == "__main__":
    app()
```

### Type Annotations
```python
from typing import Optional, List
from pathlib import Path
import typer

app = typer.Typer()

@app.command()
def deploy(
    env: str = typer.Option(..., help="Environment (prod/staging/dev)"),
    config: Optional[Path] = typer.Option(None, help="Config file path"),
    replicas: int = typer.Option(3, min=1, max=10),
    dry_run: bool = typer.Option(False, "--dry-run/--no-dry-run"),
):
    """Deploy application to an environment."""
    typer.echo(f"Deploying to {env} with {replicas} replicas")
    if dry_run:
        typer.echo("[yellow]DRY RUN MODE[/yellow]")
```

### Subcommands with Typer
```python
from typer import Typer, Argument

app = Typer()

@app.command()
def init(name: str):
    """Initialize a new project."""
    typer.echo(f"Initializing {name}")

@app.command()
def build(project: str):
    """Build a project."""
    typer.echo(f"Building {project}")

@app.command()
def deploy(project: str, env: str = "prod"):
    """Deploy a project."""
    typer.echo(f"Deploying {project} to {env}")

# Run: myapp init myproject
# Run: myapp build myproject  
# Run: myapp deploy myproject --env staging
```

### Rich Console Output
```python
from rich.console import Console
from rich.progress import Progress
from rich.table import Table
import typer

console = Console()

@app.command()
def status():
    """Show application status."""
    table = Table(title="Service Status")
    table.add_column("Service", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Uptime")
    
    services = [
        ("API", "Running", "5d 3h"),
        ("Database", "Running", "5d 3h"),
        ("Cache", "Warning", "2h"),
    ]
    
    for service, status, uptime in services:
        style = "green" if status == "Running" else "yellow"
        table.add_row(service, f"[{style}]{status}[/{style}]", uptime)
    
    console.print(table)
```

### Progress Bars with Rich
```python
import time
from rich.progress import Progress, SpinnerColumn, TextColumn

@app.command()
def process(count: int = 10):
    """Process items with progress."""
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Processing...", total=count)
        for i in range(count):
            time.sleep(0.1)
            progress.advance(task)
```

## Shell Completion

### Click Completion
```python
@click.command()
@click.option("--name", shell_complete=lambda ctx, **_: ["alice", "bob"])
def hello(name):
    click.echo(f"Hello, {name}")
```

### Typer Completion (Automatic)
```bash
# Bash
eval "$(_MYAPP_COMPLETE=bash_source myapp)"

# Zsh
eval "$(_MYAPP_COMPLETE=zsh_source myapp)"

# Fish
myapp --show-completion fish > ~/.config/fish/completions/myapp.fish
```

## Testing

### Click Test Example
```python
from click.testing import CliRunner

def test_hello():
    runner = CliRunner()
    result = runner.invoke(hello, ["--name", "Test"])
    assert result.exit_code == 0
    assert "Hello, Test!" in result.output
```

### Typer Test Example
```python
from typer.testing import CliRunner

def test_hello():
    runner = CliRunner()
    result = runner.invoke(app, ["--name", "Test"])
    assert result.exit_code == 0
    assert "Hello, Test" in result.stdout
```

## Best Practices

1. **Use Click** for complex CLIs needing fine control
2. **Use Typer** for rapid development with type hints
3. **Group commands** logically with subcommands
4. **Validate early** - let frameworks handle validation
5. **Add Rich** for professional terminal output
6. **Enable shell completion** for power users
7. **Test CLIs** like any other Python code
8. **Version your CLI** with `--version`
