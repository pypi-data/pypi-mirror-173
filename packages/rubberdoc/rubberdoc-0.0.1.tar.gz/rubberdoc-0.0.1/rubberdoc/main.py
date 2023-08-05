import typer
from rubberdoc import __version__

app = typer.Typer()

@app.command()
def version():
    """ show current version """
    typer.echo(f"rubberdoc v{__version__}")

@app.command()
def quack():
    """ say hello """
    typer.secho("🦆 Quack!", fg='yellow')