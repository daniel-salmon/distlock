import asyncio
from typing import Annotated

import typer

from . import __version__
from .async_server import serve as serve_async
from .server import serve

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
    if run_async:
        asyncio.run(serve_async(address=address, port=port))
    else:
        serve(address=address, port=port, max_workers=max_workers)
