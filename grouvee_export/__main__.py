from typing import Optional

import click

from .core import login_and_export


@click.command(name="grouvee_export")
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
def main(chromedriver_location: Optional[str], credential_path: Optional[str]) -> None:
    login_and_export(
        credential_location=credential_path,
        chromedriver_location=chromedriver_location,
    )


if __name__ == "__main__":
    main(prog_name="grouvee_export")
