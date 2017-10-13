# -*- coding: utf-8 -*-

"""Console script for smart_hass."""

import click
import bayes


@click.command()
def main(args=None):
    """Console script for smart_hass."""
    click.echo("Replace this message by putting your code into "
               "smart_hass.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")

    print(bayes.update_probability(0.1, 0.2, 0.5))



if __name__ == "__main__":
    main()
