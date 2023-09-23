# grouvee_export

This is a partial [grouvee](https://www.grouvee.com/) (a video game database website) exporter.

To save your data from Grouvee:

1. Need to login with Grouvee Username/Password
1. Go to <https://www.grouvee.com/export/>
1. Get the download link sent to your email to download the CSV export

The python script installed here handles the first 2 steps, but the last depends on if you have some way to access your email programmatically. Personally, I use the script in [`bin`](./bin), running it once [evry 2 months](https://github.com/seanbreckenridge/dotfiles/blob/53919cd438659960dd71177f9cfc4ee27007562e/.local/scripts/linux/housekeeping#L46)

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
{
  "grouvee_id": 199,
  "name": "FIFA Soccer 07",
  "url": "https://www.grouvee.com/games/199-fifa-soccer-07/",
  "giantbomb_id": 37,
  "release_date": "2006-10-17",
  "rating": 2,
  "review": null,
  "shelves": [
    {
      "name": "Played",
      "added": "2017-01-31T14:30:39+00:00",
      "url": "https://www.grouvee.com/user/purplepinapples/shelves/106920-played/"
    }
  ],
  "genres": {
    "Simulation": "https://www.grouvee.com/games/?genre=simulation",
    "Soccer": "https://www.grouvee.com/games/?genre=soccer",
    "Sports": "https://www.grouvee.com/games/?genre=sports"
  },
  "franchises": {
    "FIFA": "https://www.grouvee.com/games/franchise/76-fifa/"
  },
  "developers": {
    "EA Canada": "https://www.grouvee.com/games/?developer=ea-canada"
  },
  "publishers": {
    "Electronic Arts": "https://www.grouvee.com/games/?publisher=electronic-arts"
  }
}
```

### Tests

```bash
git clone 'https://github.com/seanbreckenridge/grouvee_export'
cd ./grouvee_export
pip install mypy
mypy ./grouvee_export
```
