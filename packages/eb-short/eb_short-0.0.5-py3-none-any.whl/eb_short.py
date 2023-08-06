import json
import typer
from os.path import exists, expanduser, isdir

import requests

EB_CONFIG_FILE_PATH = f"{expanduser('~')}/.eb-config.json"
CONFIG_FILE_API_KEY_KEY = "eb-shortener-api-key"
SHORTENER_URL = "https://s.eb8.ch/rest/v3/short-urls"


app = typer.Typer()


@app.command("add-key")
def add_key(key: str):
    """Add the key to the ~/.eb-config.json file."""
    if exists(EB_CONFIG_FILE_PATH) and not isdir(EB_CONFIG_FILE_PATH):
        with open(EB_CONFIG_FILE_PATH, "r") as eb_config_file:
            eb_config_dict = json.load(eb_config_file)
            print(eb_config_dict)
            eb_config_dict[CONFIG_FILE_API_KEY_KEY] = key
    else:
        eb_config_dict = {CONFIG_FILE_API_KEY_KEY: key}
        print(eb_config_dict)

    with open(EB_CONFIG_FILE_PATH, "w") as eb_config_file:
        json.dump(eb_config_dict, eb_config_file, indent=2)

    typer.secho("api key added to ~/.eb-config.json", fg=typer.colors.GREEN)


@app.command("short")
def short(url: str):
    """Shorten the given url."""
    if not exists(EB_CONFIG_FILE_PATH) or isdir(EB_CONFIG_FILE_PATH):
        typer.secho(
            "~./eb-config.json file is missing, use add-key command to generate it",
            fg=typer.colors.RED,
        )
    else:
        with open(EB_CONFIG_FILE_PATH, "r") as eb_config_file:
            eb_config_dict = json.load(eb_config_file)

        if not CONFIG_FILE_API_KEY_KEY in eb_config_dict:
            typer.secho(
                f"~./eb-config.json does not contain {CONFIG_FILE_API_KEY_KEY} entry, use add-key command to generate it",
                fg=typer.colors.RED,
            )
        else:
            api_key = eb_config_dict[CONFIG_FILE_API_KEY_KEY]
            payload = {"longUrl": url}

            response = requests.post(
                url=SHORTENER_URL,
                json=payload,
                headers={"Content-Type": "application/json", "X-Api-Key": api_key},
            )

            if response.status_code == 200:
                typer.secho(response.json()["shortUrl"], fg=typer.colors.GREEN)

            else:
                typer.secho(
                    "something went wront, do you have a valid api key",
                    fg=typer.colors.RED,
                )


def main():
    app()


if __name__ == "__main__":
    app()
