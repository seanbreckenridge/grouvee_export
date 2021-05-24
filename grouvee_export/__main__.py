from pathlib import Path
from typing import Optional

import click

from .core import login_and_export
from .dal import parse_export, serialize_export


@click.group(name="grouvee_export")
def main() -> None:
    """
    Grouvee Exporter/Parser
    """


@main.command()
@click.option(
    "-c",
    "chromedriver_location",
    type=click.Path(exists=True),
    help="Path to chromedriver",
    default=None,
)
@click.option(
    "--secret",
    "credential_path",
    type=click.Path(exists=True),
    help="Credentials file",
    default=None,
)
def export(
    chromedriver_location: Optional[str], credential_path: Optional[str]
) -> None:
    """
    Use a chromedriver to login and start a Grouvee export
    """
    login_and_export(
        credential_location=credential_path,
        chromedriver_location=chromedriver_location,
    )


@main.command()
@click.argument("CSV_EXPORT", type=click.Path(exists=True))
def parse(csv_export: str) -> None:
    """
    Parse information out of the CSV file into JSON
    """
    click.echo(serialize_export(parse_export(Path(csv_export))))


if __name__ == "__main__":
    main(prog_name="grouvee_export")
