from typing import Annotated

import typer

from . import __version__

app = typer.Typer()


@app.command()
def run(
    version: Annotated[
        bool, typer.Option(help="Print the version number and exit")
    ] = False,
    address: Annotated[
        str, typer.Option(help="Address on which to run the server")
    ] = "[::]",
    port: Annotated[int, typer.Option(help="Port on which to run the server")] = 50051,
    max_workers: Annotated[
        int,
        typer.Option(
            "--max-workers",
            help="Maximum number of workers for multithreaded server. Does not matter when running with --run-async.",
        ),
    ] = 5,
    run_async: Annotated[
        bool, typer.Option("--run-async", help="Should the server be run async?")
    ] = False,
) -> None:
    if version:
        print(f"{__version__}")
        raise typer.Exit()
    print("here")
