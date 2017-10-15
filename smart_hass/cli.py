# -*- coding: utf-8 -*-
"""Console script for smart_hass."""

import click


@click.command()
def main(args=None):
    """Console script for smart_hass."""
    click.echo("Replace this message by putting your code into "
               "smart_hass.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")


@click.command()
def bayes_fun():
    stdin_text = click.get_text_stream('stdin')
    click.echo(stdin_text)


if __name__ == "__main__":
    main()
