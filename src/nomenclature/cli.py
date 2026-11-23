"""
Cyclopts CLI.

Contains wrapper functions and pretty printing.
"""

from typing import Annotated

from cyclopts import App, Parameter
from rich.columns import Columns
from rich.console import Console

from nomenclature.target import (
    Feature,
    Target,
    get_target_features,
    lookup_feature_id,
    validate_target_features,
)

app = App(default_parameter=Parameter(negative=(), short_alias=True))
console = Console()


@app.default()
def main(
    target: Target,
    features: Annotated[list[Feature], Parameter(consume_multiple=1)],
) -> None:
    """
    Scrape & store GPN features from a target.

    Args:
        target: GPN target.
        features: GPN feature type.

    """

    # Validate input
    features = list(set(features))  # remove duplicates

    validation = validate_target_features(target, features)
    if validation:
        msg = "is" if len(validation) == 1 else "are"
        console.print(
            f"[red]Warning:[/red] {validation} {msg} not{' a' if msg == 'is' else ''} "
            f"valid feature{'' if msg == 'is' else 's'} on [bold]{target}[/bold], ignoring.",
            style="italic",
        )

    found_features = lookup_feature_id(target, features)
    for feature_type, feats in found_features.items():
        console.print(
            f"- {feature_type.capitalize()}: found {len(feats)} record{'' if len(feats) < 1 else 's'}."
        )


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
