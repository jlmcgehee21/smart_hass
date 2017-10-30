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

### Multisensor

Generate an Arduino sketch for an
[ESP-MQTT-JSON-Multisensor](https://github.com/bruhautomation/ESP-MQTT-JSON-Multisensor)
via:

```
$ smass multisensor --name kitchen
```

Yields: `./multisensor/multisensor.ino`, which can then be flashed to a Node MCU
via the Arduino IDE.

In order for this to function properly, you should set the following environment
variables to use for your multisensor.
* WIFI_SSID
* WIFI_PWD
* MQTT_SERVER
* MQTT_USER
* MQTT_PWD
* MQTT_PORT
* OTA_PWD

#### Wiring Diagram for Multi Sensor
![MultiSensor Wiring Diagram](assets/wiring_diagram_v2.png)


## Credits

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
project template.

The multisensor is derived from
[ESP-MQTT-JSON-Multisensor](https://github.com/bruhautomation/ESP-MQTT-JSON-Multisensor).
