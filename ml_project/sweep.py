import os
import glob
import shutil

import click


def chop(f: str) -> str:
    *_, fname = f.rpartition("/")
    return fname


def join_path(*args: str):
    return os.path.normpath(os.path.join(*args))


@click.command()
@click.option("-s", "--source", default="outputs/**/*.*")
@click.option("-d", "--dest", default=".")
def main(source: str, dest: str) -> None:
    click.secho(f"Copying {source} to {dest}", fg="green")

    if not os.path.isdir(dest):
        os.mkdir(dest)
        click.secho(f"Created dir {dest}", fg="yellow")

    for file in glob.glob(source, recursive=True):
        filename = chop(file)
        click.secho(f"copying {file} to {dest}", fg="white")

        try:
            shutil.copy(file, join_path(dest, filename))
        except Exception as e:
            click.secho(f"{e}", fg="red")

    click.secho("Done", fg="green")


if __name__ == "__main__":
    main()
