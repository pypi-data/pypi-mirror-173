import math
import random
import re
from typing import List, Optional

import rich
import typer

from . import __version__
from .diceparser import DiceParser

app = typer.Typer(rich_markup_mode="rich")
console = rich.console.Console()


def version_callback(value: bool) -> None:
    if value:
        console.print(
            f"[bold]Groll[/bold] (version [green]{__version__}[/])", highlight=False
        )
        raise typer.Exit(0)


@app.command()
def main(
    dice: List[str] = typer.Argument(..., hidden=True),
    version: Optional[bool] = typer.Option(
        False,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Print version and exit.",
    ),
    debug: Optional[bool] = typer.Option(
        False, "--debug", "-D", help="Print calculations for debugging."
    ),
    roundup: Optional[bool] = typer.Option(
        False, "--round-up", "-R", help="Round values up to the nearest integer."
    ),
):
    """Roll [bold]DICE[/] and print result."""
    parser = DiceParser(roundup=roundup, debug=debug)
    console.print(f"[green]{parser.roll(' '.join(dice))}[/]", highlight=False)
