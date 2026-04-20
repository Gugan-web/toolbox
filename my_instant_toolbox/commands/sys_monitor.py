import psutil
import time
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich.layout import Layout
from rich.progress import BarColumn, Progress, TextColumn

console = Console()

def get_sys_data():
    """Fetches system metrics."""
    cpu_overall = psutil.cpu_percent(interval=None)
    cpu_per_core = psutil.cpu_percent(interval=None, percpu=True)
    memory = psutil.virtual_memory()
    disk = psutil.disk_partitions()
    net = psutil.net_io_counters()
    
    # Get top 5 processes by CPU
    procs = []
    for p in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            procs.append(p.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    top_procs = sorted(procs, key=lambda x: x['cpu_percent'], reverse=True)[:5]
    
    return cpu_overall, cpu_per_core, memory, disk, net, top_procs

def create_dashboard(data):
    cpu_overall, cpu_per_core, memory, disk_parts, net, top_procs = data
    
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body"),
        Layout(name="footer", size=3)
    )
    layout["body"].split_row(
        Layout(name="left"),
        Layout(name="right")
    )
    layout["left"].split_column(
        Layout(name="cpu"),
        Layout(name="memory")
    )
    
    # Header
    layout["header"].update(Panel(f"[bold cyan]System Monitor Dashboard[/] | {datetime.now().strftime('%H:%M:%S')}", border_style="blue"))
    
    # CPU Panel
    cpu_table = Table.grid(expand=True)
    cpu_table.add_column()
    cpu_table.add_row(f"Overall: {cpu_overall}%")
    for i, perc in enumerate(cpu_per_core):
        cpu_table.add_row(f"Core {i}: {perc}%")
    layout["cpu"].update(Panel(cpu_table, title="CPU Usage", border_style="magenta"))
    
    # Memory Panel
    mem_table = Table.grid(expand=True)
    mem_table.add_row(f"Used: {memory.used // (1024**2)} MB")
    mem_table.add_row(f"Total: {memory.total // (1024**2)} MB")
    layout["memory"].update(Panel(mem_table, title=f"RAM: {memory.percent}%", border_style="green"))
    
    # Right Panel: Top Procs and Network
    right_table = Table(title="Top 5 Processes", expand=True, show_header=True)
    right_table.add_column("PID")
    right_table.add_column("Name")
    right_table.add_column("CPU %", justify="right")
    for p in top_procs:
        right_table.add_row(str(p['pid']), p['name'], f"{p['cpu_percent']}%")
    
    layout["right"].split_column(
        Layout(Panel(right_table, border_style="yellow")),
        Layout(Panel(f"Sent: {net.bytes_sent // (1024**2)} MB\nRecv: {net.bytes_recv // (1024**2)} MB", title="Network I/O", border_style="cyan"))
    )
    
    # Footer: Disk info
    disk_info = " | ".join([f"{d.device}: {psutil.disk_usage(d.mountpoint).percent}%" for d in disk_parts if 'cdrom' not in d.opts])
    layout["footer"].update(Panel(f"Disks: {disk_info}", border_style="dim"))
    
    return layout

def show_sys_info(live: bool = False):
    """Displays system resource usage dashboard."""
    if not live:
        data = get_sys_data()
        # Fallback to simple table if not live, or just show one frame
        console.print(create_dashboard(data))
        return

    with Live(create_dashboard(get_sys_data()), console=console, refresh_per_second=1, screen=True) as live_display:
        try:
            while True:
                time.sleep(1)
                live_display.update(create_dashboard(get_sys_data()))
        except KeyboardInterrupt:
            pass
