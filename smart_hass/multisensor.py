import os
import sys
import jinja2

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(os.path.abspath(THIS_DIR), 'templates')

def render_sketch_file(sensor_name):
    wifi_ssid = os.environ.get('WIFI_SSID')
    wifi_pwd = os.environ.get('WIFI_PWD')

    mqtt_server = os.environ.get('MQTT_SERVER')
    mqtt_user = os.environ.get('MQTT_USER')
    mqtt_pwd = os.environ.get('MQTT_PWD')
    mqtt_port = os.environ.get('MQTT_PORT')

    ota_pwd = os.environ.get('OTA_PWD')

    j2_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(TEMPLATE_DIR), trim_blocks=True)
    template = j2_env.get_template('bruh_mqtt_multisensor.j2')

    output_str = template.render(
        wifi_ssid=wifi_ssid,
        wifi_pwd=wifi_pwd,
        mqtt_server=mqtt_server,
        mqtt_user=mqtt_user,
        mqtt_pwd=mqtt_pwd,
        mqtt_port=mqtt_port,
        sensor_name=sensor_name,
        ota_pwd=ota_pwd)

    return output_str


def render_hass_config(sensor_name):
    j2_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(TEMPLATE_DIR), trim_blocks=True)
    template = j2_env.get_template('home_assistant_configuration.j2')

    output_str = template.render(sensor_name=sensor_name)

    return output_str
