"""Console script for celery_debounce."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for celery_debounce."""
    click.echo("Replace this message by putting your code into "
               "celery_debounce.cli.main")
    click.echo("See click documentation at https://click.palletsprojects.com/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
