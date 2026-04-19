import shutil
import datetime
from pathlib import Path
from rich.console import Console

console = Console()

def create_backup(source_dir: str, destination_dir: str = "."):
    """Creates a timestamped zip backup of a directory."""
    source_path = Path(source_dir)
    if not source_path.exists() or not source_path.is_dir():
        console.print(f"[bold red]Error:[/] Source directory '{source_dir}' does not exist.", style="red")
        return

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{source_path.name}_backup_{timestamp}"
    destination_path = Path(destination_dir) / backup_name
    
    try:
        shutil.make_archive(str(destination_path), 'zip', source_dir)
        console.print(f"[bold green]Success![/] Backup created: [cyan]{destination_path}.zip[/]", style="green")
    except Exception as e:
        console.print(f"[bold red]Error:[/] Failed to create backup: {e}", style="red")
