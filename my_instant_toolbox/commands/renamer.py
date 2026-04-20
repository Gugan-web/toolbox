import os
import json
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.table import Table
import questionary

console = Console()

def to_snake_case(s: str) -> str:
    import re
    s = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', s)
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s).lower().replace(" ", "_").replace("-", "_")

def to_kebab_case(s: str) -> str:
    return to_snake_case(s).replace("_", "-")

def bulk_rename(
    directory: str,
    prefix: str = "",
    suffix: str = "",
    replace: str = "",
    replacement: str = "",
    pattern: str = "*",
    case: Optional[str] = None,
    numbering: bool = False,
    yes: bool = False
):
    """Advanced bulk renaming with preview and undo support."""
    path = Path(directory)
    if not path.exists() or not path.is_dir():
        console.print(f"[bold red]Error:[/] Directory '{directory}' does not exist.", style="red")
        return

    items = sorted([f for f in path.glob(pattern) if f.is_file()])
    if not items:
        console.print(f"[yellow]No files found matching pattern '{pattern}' in {directory}.[/]")
        return

    rename_tasks = []
    preview_table = Table(title="Rename Preview")
    preview_table.add_column("Original", style="dim")
    preview_table.add_column("New Name", style="bold green")

    for i, item in enumerate(items):
        old_name = item.stem
        ext = item.suffix
        
        new_name = old_name
        
        # 1. Case conversion
        if case == "upper":
            new_name = new_name.upper()
        elif case == "lower":
            new_name = new_name.lower()
        elif case == "title":
            new_name = new_name.title()
        elif case == "snake":
            new_name = to_snake_case(new_name)
        elif case == "kebab":
            new_name = to_kebab_case(new_name)
            
        # 2. String replacement
        if replace:
            new_name = new_name.replace(replace, replacement)
            
        # 3. Prefix/Suffix
        new_name = f"{prefix}{new_name}{suffix}"
        
        # 4. Numbering
        if numbering:
            new_name = f"{new_name}_{i+1}"
            
        new_filename = f"{new_name}{ext}"
        new_path = path / new_filename
        
        if new_filename != item.name:
            rename_tasks.append((item, new_path))
            preview_table.add_row(item.name, new_filename)

    if not rename_tasks:
        console.print("[yellow]No changes needed.[/]")
        return

    console.print(preview_table)
    
    if not yes:
        confirmed = questionary.confirm(f"Rename these {len(rename_tasks)} files?").ask()
        if not confirmed:
            console.print("[yellow]Aborted.[/]")
            return

    undo_log = []
    renamed_count = 0
    
    for old_path, new_path in rename_tasks:
        try:
            # Handle collision
            if new_path.exists() and new_path != old_path:
                new_path = new_path.parent / f"{new_path.stem}_{os.urandom(2).hex()}{new_path.suffix}"
            
            old_path.rename(new_path)
            undo_log.append({"old": str(old_path), "new": str(new_path)})
            renamed_count += 1
        except Exception as e:
            console.print(f"[yellow]Warning:[/] Could not rename {old_path.name}: {e}")

    # Write undo log
    undo_file = path / ".toolbox_undo.json"
    with open(undo_file, "w") as f:
        json.dump(undo_log, f, indent=2)

    console.print(f"[bold green]Success![/] Renamed {renamed_count} files.", style="green")
    console.print(f"[dim]Undo log saved to {undo_file}[/]")
