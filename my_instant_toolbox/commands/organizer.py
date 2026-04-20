import os
import shutil
from pathlib import Path
from collections import defaultdict
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

console = Console()

def organize_files(directory: str, dry_run: bool = False, recursive: bool = False):
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

    files_to_move = []
    search_pattern = "**/*" if recursive else "*"
    
    for item in path.glob(search_pattern):
        if item.is_file():
            # Skip files already in a category folder to avoid nesting
            parent_name = item.parent.name
            if parent_name in extensions_map or parent_name == "Others":
                continue
            files_to_move.append(item)

    if not files_to_move:
        console.print("[yellow]No files found to organize.[/]")
        return

    stats = defaultdict(int)
    moved_count = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Organizing files...", total=len(files_to_move))
        
        for item in files_to_move:
            ext = item.suffix.lower()
            target_subdir = "Others"
            
            for folder, exts in extensions_map.items():
                if ext in exts:
                    target_subdir = folder
                    break
            
            target_path = path / target_subdir
            
            if not dry_run:
                target_path.mkdir(exist_ok=True)
                try:
                    dest = target_path / item.name
                    # Handle name collisions
                    if dest.exists():
                        dest = target_path / f"{item.stem}_{os.urandom(2).hex()}{item.suffix}"
                    
                    shutil.move(str(item), str(dest))
                    moved_count += 1
                except Exception as e:
                    progress.console.print(f"[yellow]Warning:[/] Could not move {item.name}: {e}")
            else:
                moved_count += 1
            
            stats[target_subdir] += 1
            progress.update(task, advance=1)

    # Summary Table
    table = Table(title="Organization Summary" + (" (DRY RUN)" if dry_run else ""))
    table.add_column("Category", style="magenta")
    table.add_column("Files Processed", justify="right", style="green")
    
    for category, count in sorted(stats.items()):
        table.add_row(category, str(count))
    
    console.print(table)
    
    if dry_run:
        console.print(f"[bold yellow]Dry Run Complete:[/] Would have organized {moved_count} files.", style="yellow")
    else:
        console.print(f"[bold green]Success![/] Organized {moved_count} files into categories.", style="green")
