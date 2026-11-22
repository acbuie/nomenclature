"""
Cyclopts CLI.

Contains wrapper functions and pretty printing.
"""

from typing import Annotated

from cyclopts import App, Parameter
from rich.columns import Columns
from rich.console import Console

from nomenclature.target import Feature, Target, get_target_features

app = App(default_parameter=Parameter(negative=(), short_alias=True))
console = Console()


@app.default()
def main(
    target: Target,
    features: Annotated[list[Feature], Parameter(consume_multiple=True)],
) -> None:
    """
    Scrape & store GPN features from a target.

    Args:
        target: GPN target.
        features: GPN feature type.

    """

    console.print(f"Parsing {target}")
    console.print(f"Requested {features}")


@app.command()
def list_features(target: Target) -> None:
    """
    Display a list of valid targets for a feature.

    Args:
        target: GPN target.

    """
    columns = Columns(get_target_features(target), padding=(0, 3))

    console.print(f"{target.capitalize()} features", style="italic")
    console.print(columns)
