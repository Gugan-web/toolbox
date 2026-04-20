import sys
import shutil
import platform
import subprocess
from rich.console import Console
from rich.table import Table

console = Console()

def check_command(cmd: str) -> str:
    """Checks if a command exists and returns a status badge."""
    if shutil.which(cmd):
        return "[bold green]PASS[/]"
    return "[bold yellow]WARN[/]"

def run_doctor():
    """Environment health check."""
    console.print("\n[bold cyan]Diagnostic Check: My Instant Toolbox[/]\n")
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Component", style="cyan")
    table.add_column("Details")
    table.add_column("Status", justify="center")

    # 1. Python Check
    py_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    table.add_row("Python Version", py_ver, "[bold green]PASS[/]")

    # 2. Virtual Env Check
    is_venv = hasattr(sys, 'real_prefix') or (base_prefix := getattr(sys, 'base_prefix', sys.prefix)) != sys.prefix
    venv_status = "[bold green]YES[/]" if is_venv else "[bold yellow]NO (Global)[/]"
    table.add_row("Virtual Environment", f"Detected: {is_venv}", venv_status)

    # 3. Pip Check
    pip_ver = "Unknown"
    try:
        pip_ver = subprocess.check_output([sys.executable, "-m", "pip", "--version"]).decode().split()[1]
        pip_status = "[bold green]PASS[/]"
    except Exception:
        pip_status = "[bold red]FAIL[/]"
    table.add_row("Pip Installer", pip_ver, pip_status)

    # 4. OS Check
    table.add_row("Operating System", platform.system() + " " + platform.release(), "[bold green]PASS[/]")

    # 5. External Tools
    tools = ["git", "node", "docker", "npm"]
    for tool in tools:
        table.add_row(f"Tool: {tool}", "CLI Binary", check_command(tool))

    console.print(table)
    console.print("\n[dim]* Note: WARN status for tools like Docker doesn't prevent Toolbox functionality.[/]")
