import json
import requests
import click


@click.command()
@click.option("-p", "--port", default=5000)
@click.option("-h", "--host", default="127.0.0.1")
@click.option("-d", "--data", default="tmp/payload.json")
def main(port, host, data):
    click.secho("Sample Client", fg="green")
    try:
        with open(data, "r") as f:
            params = json.load(f)
            payload = {"payload": json.dumps(params)}

            click.secho(params, fg="white")
        url = f"http://{host}:{port}/predict"
        click.secho("Connecting to " + url, fg="green")
        with requests.get(url=url, params=payload) as response:
            response.raise_for_status()
            click.secho(response.text, fg="white")
    except Exception as e:
        click.secho(f"Exception: {e}", fg="red")
    click.secho("Done", fg="green")


if __name__ == "__main__":
    main()
