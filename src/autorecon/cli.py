import typer
from pathlib import Path
from rich.console import Console

from autorecon.core.config import load_config
from autorecon.core.scanner import Scanner

app = typer.Typer(help="Recon automation for HTB/TryHackMe boxes")
console = Console()

@app.command()
def scan(
    target: str = typer.Argument(...),
    full: bool = typer.Option(False, "--full"),
    output: Path = typer.Option(Path("output"), "--output"),
    ctx: typer.Context = typer.Option(None, hidden=True),
    domain: str = typer.Option(None,"--domain", help = "Domain name for subdomain enumeration"),
):
    cfg = load_config()
    outdir = output / target
    scanner = Scanner(target, outdir, cfg.scanner.model_dump())

    console.print(f"[bold green]Escaneando {target}[/]")
    data = scanner.run_full() if full else scanner.run_fast()
    scanner.save(data)

    # Si hay dominio, agregamos entrada ficticia para que el plugin se active
    if domain:
        data["domain"] = domain

    # Lanzamos enumerator (incluye subdom discovery)
    from autorecon.core.enumerator import Enumerator
    enum = Enumerator(target, outdir, cfg)
    enum.run(data)

    # Generamos reporte
    from autorecon.core.reporter import Reporter
    rep = Reporter(outdir)
    path = rep.run()
    console.print(f"[bold blue]Report en[/] {path}")

@app.command()
def report(
    target: str = typer.Argument(..., help="IP objetivo"),
    output: Path = typer.Option(Path("output"), "--output", help="Carpeta base"),
):
    """Genera report.md a partir de scan.json"""
    from autorecon.core.reporter import Reporter
    outdir = output / target
    if not (outdir / "scan.json").exists():
        console.print("[red]No se encontró scan.json[/]")
        raise typer.Exit(1)
    path = Reporter(outdir).run()
    console.print(f"[bold blue]Report en[/] {path}")
    