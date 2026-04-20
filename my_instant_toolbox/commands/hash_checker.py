import hashlib
from pathlib import Path
from rich.console import Console

console = Console()

def calculate_hash(file_path: str, algo: str = "sha256", verify: str = None):
    """Computes and optionally verifies the hash of a file."""
    path = Path(file_path)
    if not path.exists() or not path.is_file():
        console.print(f"[bold red]Error:[/] File '{file_path}' does not exist.", style="red")
        return

    try:
        hash_func = getattr(hashlib, algo.lower())()
    except AttributeError:
        console.print(f"[bold red]Error:[/] Unsupported algorithm '{algo}'.", style="red")
        console.print("Supported: md5, sha1, sha256, sha512, blake2b")
        return

    # Read in chunks for large files
    try:
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        
        result = hash_func.hexdigest()
        
        console.print(f"\n[bold cyan]{algo.upper()} Hash:[/] [green]{result}[/]")
        
        if verify:
            if result.lower() == verify.lower():
                console.print("[bold green]Verification Successful: Matches![/]")
            else:
                console.print(f"[bold red]Verification Failed![/]")
                console.print(f"Expected: {verify.lower()}")
                console.print(f"Actual:   {result.lower()}")
                
    except Exception as e:
        console.print(f"[bold red]Error:[/] {e}", style="red")
