from pathlib import Path
from typing import Optional

import click


@click.group(name="grouvee_export")
def main() -> None:
    """
    Grouvee Exporter/Parser
    """


@main.command(short_help="start a grouvee export")
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
    from .core import login_and_export

    login_and_export(
        credential_location=credential_path,
        chromedriver_location=chromedriver_location,
    )


@main.command(short_help="parse a grouvee csv export")
@click.argument(
    "CSV_EXPORT",
    type=click.Path(exists=True, dir_okay=False),
)
def parse(csv_export: str) -> None:
    """
    Parse information out of the CSV file into JSON
    """
    from .dal import parse_export, serialize_export

    click.echo(serialize_export(parse_export(Path(csv_export))))


if __name__ == "__main__":
    main(prog_name="grouvee_export")
