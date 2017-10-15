import click
import yaml


@click.command()
@click.option('--conf',
              default=None, help='File to parse for binary bayes sensors.')
def main(conf):
    if conf is None:
        stdin_text = click.get_text_stream('stdin').read()
        parsed_yaml = yaml.load(stdin_text)

    else:
        with open(conf, 'r') as conf_file:
            parsed_yaml = yaml.load(conf_file)

    click.echo(parsed_yaml)


def update_probability(prior, prob_true, prob_false):
    """Update probability using Bayes' rule."""
    numerator = prob_true * prior
    denominator = numerator + prob_false * (1 - prior)

    probability = numerator / denominator
    return probability


def load_bayesian_binary_config(path):
    pass


if __name__ == '__main__':
    main()
