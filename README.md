# grouvee_export

This is a partial [grouvee](https://www.grouvee.com/) (a video game database website) exporter.

To save your data from Grouvee:

1. Need to login with Grouvee Username/Password
1. Go to <https://www.grouvee.com/export/>
1. Get the link sent to your email, go to it to download your export

The python script installed here handles the first 2 steps, but the last depends on if you have some way to access your email programatically. Personally, I use the script in [`bin`](./bin)

This also includes a command to parse the resulting CSV file, once you've downloaded it to your computer

## Installation

Requires `python3.7+`

To install with pip, run:

    python3 -m pip install git+https://github.com/seanbreckenridge/grouvee_export

Requires a chromedriver binary. See [here](https://gist.github.com/seanbreckenridge/709a824b8c56ea22dbf4e86a7804287d)

## Usage

Expects a file at `~/.local/share/grouvee.yaml` like

```yaml
username: grouveeUsername
password: grouveePassword
```

Then run: `python3 -m grouvee_export export -c /path/to/chromedriver` -- which logs you in using your credentials and goes to the export page. After about 10 minutes, an email should be sent to you with a link to the CSV file

After you've downloaded the CSV file, you can use the `python3 -m grouvee_export parse` command to parse the export:

```
$ python3 -m grouvee_export parse ~/data/grouvee/1621762287.csv | jq '.[0]'
```

### Tests

```bash
git clone 'https://github.com/seanbreckenridge/grouvee_export'
cd ./grouvee_export
pip install mypy
mypy ./grouvee_export
```
