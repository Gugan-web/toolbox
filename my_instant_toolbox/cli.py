import typer
import subprocess
import os
import shutil
from typing import Optional
from rich.console import Console
from my_instant_toolbox.commands import organizer, renamer, backup_tool, search_replace, sys_monitor

console = Console()

app = typer.Typer(
    name="toolbox",
    help="Instant Script Toolbox - A collection of essential automation scripts.",
    add_completion=False,
)

@app.command()
def organize(directory: str = typer.Argument(..., help="Directory to organize")):
    """Sort files into subfolders by extension."""
    organizer.organize_files(directory)

@app.command()
def rename(
    directory: str = typer.Argument(..., help="Directory containing files to rename"),
    prefix: str = typer.Option("", help="Add prefix to filenames"),
    suffix: str = typer.Option("", help="Add suffix to filenames"),
    replace: str = typer.Option("", help="String to find for replacement"),
    replacement: str = typer.Option("", help="Replacement string"),
):
    """Bulk rename files with prefixes, suffixes, or text replacement."""
    renamer.bulk_rename(directory, prefix, suffix, replace, replacement)

@app.command()
def backup(
    source: str = typer.Argument(..., help="Directory to backup"),
    destination: str = typer.Option(".", help="Where to save the backup zip"),
):
    """Create a timestamped ZIP backup of a directory."""
    backup_tool.create_backup(source, destination)

@app.command()
def find_replace(
    directory: str = typer.Argument(..., help="Directory to search in"),
    find: str = typer.Argument(..., help="Text to search for"),
    replace: str = typer.Argument(..., help="Text to replace with"),
    pattern: str = typer.Option("*", help="Glob pattern for files (e.g. *.txt)"),
):
    """Find and replace text across multiple files."""
    search_replace.search_replace(directory, find, replace, pattern)

@app.command()
def sysinfo():
    """Display system resource usage dashboard."""
    sys_monitor.show_sys_info()

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
        console.print("[bold blue]Building package...[/bold blue]")
        subprocess.run(["python", "-m", "build"], check=True)
        console.print("[green]Build successful![/green]")

        if dry_run:
            console.print("[yellow]Dry run: skipping upload.[/yellow]")
            return

        # 3. Upload
        console.print("[bold cyan]Uploading to PyPI...[/bold cyan]")
        subprocess.run(["python", "-m", "twine", "upload", "dist/*"], check=True)
        console.print("[bold green]Successfully published to PyPI![/bold green]")
        console.print("View at: https://pypi.org/project/my-instant-toolbox/")

    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error during publishing: {e}[/red]")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[red]An unexpected error occurred: {e}[/red]")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
