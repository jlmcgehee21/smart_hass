# smart\_hass

[![image](https://img.shields.io/pypi/v/smart_hass.svg)](https://pypi.python.org/pypi/smart_hass)

[![image](https://img.shields.io/travis/jlmcgehee21/smart_hass.svg)](https://travis-ci.org/jlmcgehee21/smart_hass)

Tools I find useful in my interactions with Home Assistant.

-   Free software: GNU General Public License v3

## Installation
```
$ pip install smart_hass
```

## Usage

This is a command line tool meant to work in a Unix shell.

If you don't know what to do, try:

```
$ smass --help
```

### Binary Bayes introspection
Determine which combinations of observations can cause your Bayesian Binary
sensor to be True/False.

Latest functionality can be found via:

```
$ smass bayes --help
```

Pipe valid YAML from a Bayesian Binary config:

```
$ pbpaste | smass bayes
```

Identify and analyze Bayesian Binary sensors in a config file:

```
$ smass bayes --conf ~/hass_config/binary_sensors.yaml
```

List all cases where a Bayesian Binary sensor evaluates to True with an
observation of `on` for `binary_sensor.bedroom_motion`

```
$ pbpaste | smass bayes -te binary_sensor.bedroom_modtion -ts on | json_pp
```





## Credits

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
project template.
