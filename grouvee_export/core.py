import sys
import os
import shutil
from pathlib import Path
from typing import NamedTuple, Optional
from functools import partial

import click
import yaml
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

default_local_dir = os.path.join(Path.home(), ".local", "share")
local_directory: str = os.environ.get("XDG_DATA_HOME", default_local_dir)
os.makedirs(local_directory, exist_ok=True)

default_credential_location = Path(local_directory) / "grouvee.yaml"

GROUVEE_LOGIN_PAGE = "https://www.grouvee.com/user/login"
GROUVEE_EXPORT_PAGE = "https://grouvee.com/export"

EMAIL_ID = "id_username"
PASSWORD_ID = "id_password"
SIGNIN_CSS_SELECTOR = "body > form > button[type='submit']"

eprint = partial(click.echo, err=True)


class Credentials(NamedTuple):
    username: str
    password: str

    @staticmethod
    def load(path: Path) -> "Credentials":
        if not path.exists():
            eprint(f"Expected credential file at {path}")
            sys.exit(1)
        with path.open() as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        return Credentials(username=data["username"], password=data["password"])


NO_CHROMEDRIVER_ERR = """Could not find chromedriver on your PATH
Provide a path to the chromedriver binary with the -c flag"""


def create_driver(chromedriver_path: Optional[str] = None) -> WebDriver:
    options = Options()
    if chromedriver_path is not None:
        options.binary_location = chromedriver_path
    dr = WebDriver(options=options)
    return dr


def login(driver: WebDriver, creds: Credentials) -> None:
    eprint("Logging in to Grouvee...")
    driver.get(GROUVEE_LOGIN_PAGE)
    driver.find_element(By.ID, EMAIL_ID).send_keys(creds.username)
    driver.find_element(By.ID, PASSWORD_ID).send_keys(creds.password)
    driver.find_element(By.CSS_SELECTOR, SIGNIN_CSS_SELECTOR).click()


def export(driver: WebDriver) -> None:
    eprint("Requesting export...")
    driver.get(GROUVEE_EXPORT_PAGE)


def login_and_export(
    credential_location: Optional[str] = None,
    chromedriver_location: Optional[str] = None,
) -> None:
    credloc: Path
    if credential_location is None:
        credloc = default_credential_location
    else:
        credloc = Path(credential_location)
    creds = Credentials.load(credloc)
    driver = None
    try:
        driver = create_driver(chromedriver_location)
        login(driver, creds)
        export(driver)
        eprint("Done!")
    finally:
        if driver:
            driver.quit()
