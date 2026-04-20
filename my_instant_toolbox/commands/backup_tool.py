import os
import zipfile
import datetime
import json
from pathlib import Path
from typing import List, Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

def create_backup(
    source_dir: str, 
    destination_dir: str = ".", 
    incremental: bool = False,
    exclude: Optional[List[str]] = None
):
    """Advanced backup tool with incremental and glob exclusion support."""
    source_path = Path(source_dir).resolve()
    dest_path = Path(destination_dir).resolve()
    
    if not source_path.exists() or not source_path.is_dir():
        console.print(f"[bold red]Error:[/] Source directory '{source_dir}' does not exist.", style="red")
        return

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"{source_path.name}_backup_{timestamp}.zip"
    backup_file = dest_path / backup_name
    
    # Default excludes
    if exclude is None:
        exclude = []
    exclude.extend([".git", "__pycache__", ".ipynb_checkpoints", backup_name])

    # For incremental: find last manifest
    last_manifest = None
    manifest_files = sorted(dest_path.glob(f"{source_path.name}_manifest_*.json"))
    if incremental and manifest_files:
        with open(manifest_files[-1], "r") as f:
            last_manifest = json.load(f)
        console.print(f"[cyan]Last backup found: {manifest_files[-1].name}[/]")

    files_to_backup = []
    manifest_data = {"timestamp": timestamp, "files": {}}

    for item in source_path.rglob("*"):
        if item.is_file():
            # Check excludes
            skip = False
            for pattern in exclude:
                if item.match(pattern) or any(p.match(pattern) for p in item.parents):
                    skip = True
                    break
            if skip:
                continue

            mtime = item.stat().st_mtime
            rel_path = str(item.relative_to(source_path))
            
            # Incremental check
            if incremental and last_manifest:
                last_mtime = last_manifest["files"].get(rel_path)
                if last_mtime and mtime <= last_mtime:
                    continue
            
            files_to_backup.append(item)
            manifest_data["files"][rel_path] = mtime

    if not files_to_backup:
        console.print("[yellow]No new or modified files to backup.[/]")
        return

    dest_path.mkdir(exist_ok=True, parents=True)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task(f"[cyan]Backing up {len(files_to_backup)} files...", total=len(files_to_backup))
        
        with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in files_to_backup:
                zipf.write(file, file.relative_to(source_path))
                progress.update(task, advance=1)

    # Save manifest
    manifest_path = dest_path / f"{source_path.name}_manifest_{timestamp}.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest_data, f, indent=2)

    console.print(f"[bold green]Success![/] Backup created: [cyan]{backup_file}[/]", style="green")
    console.print(f"[dim]Manifest saved to {manifest_path}[/]")
