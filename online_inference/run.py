from typing import Optional
import click
from dotenv import load_dotenv

from app import make_app, AppConfig


@click.command()
@click.option("-e", "--environment", default=None)
def main(environment: Optional[str]):
    # .env file specified as CLI argument
    if environment:
        click.secho(
            f"Exporting variables from .env file: {environment}",
            fg="green"
        )
        load_dotenv(environment)
    else:
        click.secho("No user-environment given", fg="yellow")

    cfg = AppConfig()
    make_app(cfg).run(host=cfg.host, port=cfg.port)


if __name__ == "__main__":
    main()
