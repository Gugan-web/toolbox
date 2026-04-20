import re
from pathlib import Path
from collections import Counter
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def analyze_text(
    file_path: str, 
    wordcount: bool = True, 
    linecount: bool = True, 
    charcount: bool = True,
    unique: bool = False,
    top_n: int = 0
):
    """Provides statistics and analysis for a text file."""
    path = Path(file_path)
    if not path.exists() or not path.is_file():
        console.print(f"[bold red]Error:[/] File '{file_path}' does not exist.", style="red")
        return

    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        console.print(f"[bold red]Error:[/] File '{file_path}' is not a valid text file.", style="red")
        return

    # Basic stats
    lines = content.splitlines()
    words = re.findall(r'\w+', content.lower())
    chars = len(content)

    stats_table = Table(title=f"Text Analysis: {path.name}", show_header=False)
    if linecount: stats_table.add_row("Line Count", str(len(lines)))
    if wordcount: stats_table.add_row("Word Count", str(len(words)))
    if charcount: stats_table.add_row("Char Count", str(chars))
    if unique: stats_table.add_row("Unique Words", str(len(set(words))))

    console.print(Panel(stats_table, expand=False, border_style="cyan"))

    # Top N Frequent Words
    if top_n > 0:
        # Filter common small words (optional, but let's just show raw for now)
        counts = Counter(words)
        common = counts.most_common(top_n)
        
        freq_table = Table(title=f"Top {top_n} Frequent Words", show_header=True, header_style="bold magenta")
        freq_table.add_column("Word")
        freq_table.add_column("Count", justify="right")
        freq_table.add_column("Frequency", justify="left")

        max_count = common[0][1] if common else 1
        
        for word, count in common:
            # Simple bar using characters
            bar_len = int((count / max_count) * 20)
            bar = "█" * bar_len
            freq_table.add_row(word, str(count), f"[green]{bar}[/]")
            
        console.print(freq_table)
