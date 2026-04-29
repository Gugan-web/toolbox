import typer
import subprocess
import os
import shutil
from typing import Optional, List
from rich.console import Console
from rich.panel import Panel
from my_instant_toolbox.commands import (
    organizer, renamer, backup_tool, 
    search_replace, sys_monitor,
    hash_checker, text_tools, env_doctor
)

console = Console()
VERSION = "0.2.3"

BANNER = r"""
[bold cyan]
  __  __         _____           _              _   
 |  \/  |       |_   _|         | |            | |  
 | \  / |_   _    | |  _ __  ___| |_ __ _ _ __ | |_ 
 | |\/| | | | |   | | | '_ \/ __| __/ _` | '_ \| __|
 | |  | | |_| |  _| |_| | | \__ \ || (_| | | | | |_ 
 |_|  |_|\__, | |_____|_| |_|___/\__\__,_|_| |_|\__|
          __/ |                                     
         |___/                                      
  _______          _ _               
 |__   __|        | | |              
    | | ___   ___ | | |__   _____  __
    | |/ _ \ / _ \| | '_ \ / _ \ \/ /
    | | (_) | (_) | | |_) | (_) >  < 
    |_|\___/ \___/|_|_.__/ \___/_/\_\
                                     
            [bold white]v0.2.3 - Advanced CLI Suite[/]
[/]
"""

app = typer.Typer(
    name="toolbox",
    help="Instant Script Toolbox - A collection of essential automation scripts.",
    add_completion=False,
    no_args_is_help=True
)

def version_callback(value: bool):
    if value:
        console.print(f"My Instant Toolbox [cyan]v{VERSION}[/]")
        raise typer.Exit()

@app.callback()
def main(
    ctx: typer.Context,
    version: Optional[bool] = typer.Option(
        None, "--version", "-v", callback=version_callback, is_eager=True, help="Show version and exit."
    )
):
    """Modern automation toolbox for developers and power users."""
    if not ctx.resilient_parsing:
        console.print(BANNER)

@app.command()
def organize(
    directory: str = typer.Argument(..., help="Directory to organize"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview moves without touching files"),
    recursive: bool = typer.Option(False, "--recursive", "-r", help="Include subdirectories"),
):
    """Sort files into subfolders by extension."""
    organizer.organize_files(directory, dry_run=dry_run, recursive=recursive)

@app.command()
def rename(
    directory: str = typer.Argument(..., help="Directory containing files to rename"),
    prefix: str = typer.Option("", help="Add prefix to filenames"),
    suffix: str = typer.Option("", help="Add suffix to filenames"),
    replace: str = typer.Option("", help="String to find for replacement"),
    replacement: str = typer.Option("", help="Replacement string"),
    pattern: str = typer.Option("*", help="Glob pattern for files"),
    case: Optional[str] = typer.Option(None, help="Case conversion: upper, lower, title, snake, kebab"),
    numbering: bool = typer.Option(False, "--number", help="Append sequential index to filenames"),
    yes: bool = typer.Option(False, "-y", "--yes", help="Skip confirmation prompt"),
):
    """Bulk rename files with preview and undo support."""
    renamer.bulk_rename(
        directory, prefix, suffix, replace, replacement, 
        pattern=pattern, case=case, numbering=numbering, yes=yes
    )

@app.command()
def backup(
    source: str = typer.Argument(..., help="Directory to backup"),
    destination: str = typer.Option(".", help="Where to save the backup zip"),
    incremental: bool = typer.Option(False, "--incremental", "-i", help="Only backup new or modified files"),
    exclude: Optional[List[str]] = typer.Option(None, "--exclude", "-e", help="Exclusion patterns (can be used multiple times)"),
):
    """Create a timestamped archive of a directory."""
    backup_tool.create_backup(source, destination, incremental=incremental, exclude=exclude)

@app.command()
def find_replace(
    directory: str = typer.Argument(..., help="Directory to search in"),
    find: str = typer.Argument(..., help="Text to search for"),
    replace: str = typer.Argument(..., help="Text to replace with"),
    pattern: str = typer.Option("*", help="Glob pattern for files (e.g. *.txt)"),
    regex: bool = typer.Option(False, "--regex", help="Use regular expressions for searching"),
    ignore_case: bool = typer.Option(False, "--ignore-case", "-i", help="Case-insensitive search"),
    no_backup: bool = typer.Option(False, "--no-backup", help="Skip creating .bak files"),
):
    """Find and replace text with regex and diff preview."""
    search_replace.search_replace(
        directory, find, replace, pattern, 
        is_regex=regex, ignore_case=ignore_case, backup=not no_backup
    )

@app.command()
def sysinfo(live: bool = typer.Option(False, "--live", "-l", help="Live dashboard mode")):
    """Display system resource usage dashboard."""
    sys_monitor.show_sys_info(live=live)

@app.command()
def hash(
    file: str = typer.Argument(..., help="Path to file"),
    algo: str = typer.Option("sha256", "--algo", help="Algorithm: sha256, md5, sha1, blake2b"),
    verify: Optional[str] = typer.Option(None, "--verify", help="Expected hash to verify against"),
):
    """Compute or verify file checksums."""
    hash_checker.calculate_hash(file, algo=algo, verify=verify)

@app.command()
def text(
    file: str = typer.Argument(..., help="Path to text file"),
    top: int = typer.Option(0, "--top", help="Show top N frequent words"),
    unique: bool = typer.Option(False, "--unique", help="Show unique word count"),
):
    """Analyze text file statistics and word frequency."""
    text_tools.analyze_text(file, unique=unique, top_n=top)

@app.command()
def doctor():
    """Check environment health and dependencies."""
    env_doctor.run_doctor()

@app.command()
def publish(
    dry_run: bool = typer.Option(False, "--dry-run", help="Build the package without uploading"),
):
    """Clean, build, and upload the toolbox to PyPI."""
    try:
        # 1. Clean
        if os.path.exists("dist"):
            console.print("[yellow]Cleaning old build artifacts...[/yellow]")
            shutil.rmtree("dist")

        # 2. Build
        console.print(f"[bold blue]Building package v{VERSION}...[/bold blue]")
        subprocess.run(["python", "-m", "build"], check=True)
        console.print("[green]Build successful![/green]")

        if dry_run:
            console.print("[yellow]Dry run: skipping upload.[/yellow]")
            return

        # 3. Upload
        console.print("[bold cyan]Uploading to PyPI...[/bold cyan]")
        subprocess.run(["python", "-m", "twine", "upload", "dist/*"], check=True)
        console.print(f"[bold green]Successfully published v{VERSION} to PyPI![/bold green]")
        console.print("View at: https://pypi.org/project/my-instant-toolbox/")

    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error during publishing: {e}[/red]")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[red]An unexpected error occurred: {e}[/red]")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    try:
        app()
    except KeyboardInterrupt:
        console.print("\n[yellow]Program interrupted by user. Exiting...[/]")
        raise typer.Exit(0)
