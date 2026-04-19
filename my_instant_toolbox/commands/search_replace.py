import os
from pathlib import Path
from rich.console import Console

console = Console()

def search_replace(directory: str, find_text: str, replace_text: str, file_pattern: str = "*"):
    """Searches and replaces text in files matching a pattern within a directory."""
    path = Path(directory)
    if not path.exists() or not path.is_dir():
        console.print(f"[bold red]Error:[/] Directory '{directory}' does not exist.", style="red")
        return

    modified_count = 0
    for file_path in path.rglob(file_pattern):
        if file_path.is_file():
            try:
                # Basic check to avoid binary files
                content = file_path.read_text(encoding="utf-8")
                if find_text in content:
                    new_content = content.replace(find_text, replace_text)
                    file_path.write_text(new_content, encoding="utf-8")
                    modified_count += 1
                    console.print(f"[dim]Modified:[/] {file_path.relative_to(path)}")
            except (UnicodeDecodeError, PermissionError):
                continue
            except Exception as e:
                console.print(f"[yellow]Warning:[/] Error processing {file_path}: {e}")

    console.print(f"[bold green]Success![/] Replaced text in {modified_count} files.", style="green")
