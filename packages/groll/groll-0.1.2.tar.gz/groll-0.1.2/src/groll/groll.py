import math
import random
import re
from typing import List, Optional

import rich
import typer

__version__ = "0.1.2"

app = typer.Typer(rich_markup_mode="rich")
console = rich.console.Console()


def int_(dstring: str):
    if dstring:
        return int(dstring)
    else:
        return 1


class DicePool:
    def __init__(self, user_input, verbose):
        self.input = " ".join(user_input)
        self.dice = re.findall(r"\d*d\d+", self.input)
        self.result_dict = {die: self._roll(die) for die in self.dice}
        self.subbed = self._sub()
        self.result = self._eval_pool()
        self.verbose = verbose

    def __str__(self):
        if self.verbose:
            return f"{self.subbed} -> {self.result}"
        else:
            return f"{self.result}"

    def _roll(self, die):
        num, sides = map(int_, die.split("d"))
        local_results = list()
        for i in range(num):
            local_results.append(random.randint(1, sides))
        return local_results

    def _sub(self):
        out = self.input
        for k in self.result_dict:
            out = out.replace(k, f"({' + '.join(map(str, self.result_dict[k]))})")
        return out

    def _eval_pool(self):
        try:
            return math.floor(eval(self.subbed, {"__builtins__": {}}, {}))
        except NameError as e:
            console.print(f"[bold red]{e}![/]")
            raise typer.Exit(1)
        except SyntaxError as e:
            console.print(f"[bold red]Unable to parse '{e.text}'![/]")
            raise typer.Exit(1)


def version_callback(value: bool) -> None:
    if value:
        console.print(
            f"[bold]Groll[/bold] (version [green]{__version__}[/])", highlight=False)
        raise typer.Exit(0)


@app.command()
def main(
    dice: List[str] = typer.Argument(..., hidden=True),
    version: Optional[bool] = typer.Option(
        False,
        "--version", "-v",
        callback=version_callback,
        is_eager=True,
        help="Print version and exit.",
    ),
    long: Optional[bool] = typer.Option(
        False,
        "--long", "-l",
        help="Show rolled values in ouput."
    )
):
    """Roll [bold]DICE[/] and print result."""
    pool = DicePool(dice, long)
    console.print(pool, highlight=False)
