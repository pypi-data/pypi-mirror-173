import os
import typer

from rubberdoc import __version__
from rubberdoc.generator import RubberDoc
from rubberdoc.doc_handler import doc_handler_selection
from rubberdoc.config_provider import RubberDocConfig


app = typer.Typer()

@app.command()
def version():
    """ show current version """
    typer.echo(f"RubberDoc v{__version__}")

@app.command()
def quack():
    """ say hello """
    typer.secho("🦆 Quack!", fg='yellow')

@app.command()
def generate(from_dir: str or None = None, 
             to_dir: str or None = None, 
             config: str or None = None,
             style: str = 'material'):
    """Generates documentation from `from-dir` to `to-dir`  
    
    __Optional Parameters__  
    - `--from-dir` The directory of your python codebase. Defaults to current_directory  
    - `--to-dir` The directory to generate .md files to. Defaults to current_directory/docs  
    - `--config` The direct path to a .json configuration file  
    """
    rd_config = RubberDocConfig(path_to_config=config)
    doc_handler_cls = doc_handler_selection(rd_config, style)
    if doc_handler_cls:
        typer.secho(f"Using {doc_handler_cls.__name__} for generation.", fg='green')
        rd = RubberDoc(config=rd_config, doc_handler=doc_handler_cls)
        rd.generate(
            input_directory=from_dir or os.curdir, 
            output_directory=to_dir or (os.curdir + '/docs'))
    else:
        typer.secho(f"Incorrect DocHandler class provided", fg='red')