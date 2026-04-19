import os
from pathlib import Path
from rich.console import Console

console = Console()

def bulk_rename(directory: str, prefix: str = "", suffix: str = "", replace: str = "", replacement: str = ""):
    """Renames files in a directory with prefixes, suffixes, or string replacement."""
    path = Path(directory)
    if not path.exists() or not path.is_dir():
        console.print(f"[bold red]Error:[/] Directory '{directory}' does not exist.", style="red")
        return

    renamed_count = 0
    for item in path.iterdir():
        if item.is_file():
            old_name = item.stem
            ext = item.suffix
            
            new_name = old_name
            if replace:
                new_name = new_name.replace(replace, replacement)
            
            new_name = f"{prefix}{new_name}{suffix}{ext}"
            new_path = path / new_name
            
            try:
                item.rename(new_path)
                renamed_count += 1
            except Exception as e:
                console.print(f"[yellow]Warning:[/] Could not rename {item.name}: {e}")

    console.print(f"[bold green]Success![/] Renamed {renamed_count} files.", style="green")
