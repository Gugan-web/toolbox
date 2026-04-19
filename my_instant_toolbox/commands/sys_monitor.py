import psutil
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def show_sys_info():
    """Displays a quick dashboard of system resource usage."""
    
    cpu_usage = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    table = Table(title="System Monitor Dashboard", show_header=True, header_style="bold magenta")
    table.add_column("Resource", style="cyan")
    table.add_column("Usage", justify="right")
    table.add_column("Status", justify="center")

    def get_status(percent):
        if percent < 60: return "[green]OK[/]"
        if percent < 85: return "[yellow]Warning[/]"
        return "[bold red]Critical[/]"

    table.add_row("CPU", f"{cpu_usage}%", get_status(cpu_usage))
    table.add_row("Memory", f"{memory.percent}% ({memory.used // (1024**2)}MB / {memory.total // (1024**2)}MB)", get_status(memory.percent))
    table.add_row("Disk", f"{disk.percent}% ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)", get_status(disk.percent))

    console.print(Panel(table, expand=False, border_style="blue"))
