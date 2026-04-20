import os
import re
import shutil
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

console = Console()

def search_replace(
    directory: str, 
    find_text: str, 
    replace_text: str, 
    file_pattern: str = "*", 
    is_regex: bool = False,
    ignore_case: bool = False,
    backup: bool = True
):
    """Advanced search and replace with regex, case-insensitivity, and diff previews."""
    path = Path(directory)
    if not path.exists() or not path.is_dir():
        console.print(f"[bold red]Error:[/] Directory '{directory}' does not exist.", style="red")
        return

    flags = re.IGNORECASE if ignore_case else 0
    modified_count = 0
    
    for file_path in path.rglob(file_pattern):
        if file_path.is_file():
            try:
                content = file_path.read_text(encoding="utf-8")
                
                changed = False
                if is_regex:
                    if re.search(find_text, content, flags):
                        new_content = re.sub(find_text, replace_text, content, flags=flags)
                        changed = True
                else:
                    search_str = find_text
                    if ignore_case:
                        # Case insensitive literal is tricky, use regex with escape
                        new_content = re.sub(re.escape(find_text), replace_text, content, flags=re.IGNORECASE)
                        if new_content != content:
                            changed = True
                    elif find_text in content:
                        new_content = content.replace(find_text, replace_text)
                        changed = True

                if changed:
                    # Show Diff Preview
                    console.print(f"\n[bold cyan]File:[/] {file_path.relative_to(path)}")
                    
                    # Find context (simple version: find first occurrence)
                    idx = content.find(find_text) if not is_regex else re.search(find_text, content, flags).start()
                    start = max(0, idx - 40)
                    end = min(len(content), idx + len(find_text) + 40)
                    
                    before_ctx = content[start:end].replace("\n", "↵")
                    after_ctx = new_content[start:end].replace("\n", "↵")
                    
                    console.print(Panel(
                        f"[red]- {before_ctx}[/]\n[green]+ {after_ctx}[/]", 
                        title="Diff Preview", 
                        border_style="dim"
                    ))

                    if backup:
                        shutil.copy2(file_path, str(file_path) + ".bak")
                    
                    file_path.write_text(new_content, encoding="utf-8")
                    modified_count += 1
                    
            except (UnicodeDecodeError, PermissionError):
                continue
            except Exception as e:
                console.print(f"[yellow]Warning:[/] Error processing {file_path}: {e}")

    console.print(f"\n[bold green]Success![/] Replaced text in {modified_count} files.", style="green")
    if backup and modified_count > 0:
        console.print("[dim]Original files backed up with .bak extension.[/]")
