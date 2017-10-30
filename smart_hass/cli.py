# -*- coding: utf-8 -*-
"""Console script for smart_hass."""


from .bayes import BayesProcessor
from .multisensor import render_hass_config, render_sketch_file
from . import cli_utils

import click
import json
import os
import textwrap
import shutil
import sys
import yaml


@click.group()
def cli(args=None):
    """Console script for smart_hass."""
    pass

@cli.command()
@click.option('--conf', '-c', default=None,
              help='File to parse for Bayesian Binary sensors.')
@click.option('--true/--false', '-t/-f', default=True,
              help=''.join(['Output combinations that evaluate to True/False',
                           ', respectively']))
@click.option('--sensor-ind', '-si', default=None, type=int,
              help=''.join(['Index of Bayesian Binary sensor if multiple',
                            ' sensors are present']))
@click.option('--target-entity', '-te', default=None,
              help=''.join(['Only return observation combinations which',
                            ' include this entity']))
@click.option('--to_state', '-ts', default=None,
              help=''.join(['Combine with --target-entity to restrict',
                            ' observations which include both']))
@click.option('--above', '-a', default=None, type=float,
              help=''.join(['Combine with --target-entity to restrict',
                            ' observations which include both']))
@click.option('--below', '-b', default=None, type=float,
              help=''.join(['Combine with --target-entity to restrict',
                            ' observations which include both']))
@click.option('--summarize', '-s', is_flag=True,
              help='Output results as a summary')
def bayes(conf, true, sensor_ind, target_entity, to_state,
         above, below, summarize):

    if conf is not None:
        with open(conf, 'r') as conf_file:
            parsed_yaml = yaml.load(conf_file.read())

    elif not click.get_text_stream('stdin').isatty:
        message = '''You must pipe valid YAML to STDIN or load a YAML file via
                  the --conf option'''

        click.echo(textwrap.fill(message))
        sys.exit(1)

    else:
        stdin_text = click.get_text_stream('stdin').read()
        parsed_yaml = yaml.load(stdin_text)

    above = cli_utils.load_number_arg(above)
    below = cli_utils.load_number_arg(below)

    target_entity = {
        'entity_id': target_entity,
        'to_state': to_state,
        'above': above,
        'below': below
    }
    target_entity = dict(
        (k, v) for k, v in target_entity.items() if v is not None)


    processor = BayesProcessor(parsed_yaml, true, sensor_ind,
                               target_entity)

    processor.proc_sensors(summarize)

    click.echo(json.dumps(processor.summaries))


@cli.command()
@click.option('--name', '-n', default=None,
              help='Name of sensor.')
def multisensor(name):
    sketch_str = render_sketch_file(name)

    if os.path.exists('multisensor'):
        shutil.rmtree('multisensor')

    os.mkdir('multisensor')

    ino_out = os.path.join('multisensor', 'multisensor' + '.ino')
    with open(ino_out, 'w') as sketch_file:
        sketch_file.write(sketch_str)

    hass_str = render_hass_config(name)
    click.echo('#########################################')
    click.echo('## Copy Below and Place in Hass Config ##')
    click.echo('#########################################')
    click.echo(hass_str)

if __name__ == "__main__":
    cli()
