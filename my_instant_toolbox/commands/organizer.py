import os
import shutil
from pathlib import Path
from rich.console import Console

console = Console()

def organize_files(directory: str):
    """Sorts files in a directory into subdirectories based on their extension."""
    path = Path(directory)
    if not path.exists() or not path.is_dir():
        console.print(f"[bold red]Error:[/] Directory '{directory}' does not exist.", style="red")
        return

    extensions_map = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
        "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv", ".md"],
        "Audio": [".mp3", ".wav", ".flac", ".m4a", ".aac"],
        "Video": [".mp4", ".mkv", ".mov", ".avi", ".wmv"],
        "Archives": [".zip", ".tar", ".gz", ".rar", ".7z"],
        "Scripts": [".py", ".sh", ".js", ".html", ".css", ".php", ".c", ".cpp"],
    }

    moved_count = 0
    for item in path.iterdir():
        if item.is_file():
            ext = item.suffix.lower()
            target_subdir = "Others"
            
            for folder, exts in extensions_map.items():
                if ext in exts:
                    target_subdir = folder
                    break
            
            target_path = path / target_subdir
            target_path.mkdir(exist_ok=True)
            
            try:
                shutil.move(str(item), str(target_path / item.name))
                moved_count += 1
            except Exception as e:
                console.print(f"[yellow]Warning:[/] Could not move {item.name}: {e}")

    console.print(f"[bold green]Success![/] Organized {moved_count} files into categories.", style="green")
