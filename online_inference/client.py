import json
import requests
import click


PREDICT_ENDPOINT = "predict"


@click.command()
@click.option("-p", "--port", default=5000)
@click.option("-h", "--host", default="127.0.0.1")
@click.option("-d", "--data", default="data/payload.json")
@click.option("-e", "--endpoint", default=PREDICT_ENDPOINT)
def main(port, host, data, endpoint):
    click.secho("Runs testing client", fg="green")
    try:
        if endpoint == PREDICT_ENDPOINT:
            with open(data, "r") as f:
                click.secho(f"Loads payload JSON from {data}", fg="yellow")
                params = json.load(f)
                payload = {"payload": json.dumps(params)}
                click.secho(payload, fg="white")
        else:
            payload = None

        url = f"http://{host}:{port}/{endpoint}"
        click.secho("Connecting to " + url, fg="yellow")

        with requests.get(url=url, params=payload) as response:
            response.raise_for_status()
            click.secho(response.text, fg="white")

    except Exception as e:
        click.secho(f"Exception: {e}", fg="red")
    click.secho("Done", fg="green")


if __name__ == "__main__":
    main()
