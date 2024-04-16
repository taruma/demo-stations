"""Load the application configuration from the specified YAML file."""

from box import Box

_CONFIG_PATH = "app_config.yml"
appConfig = Box.from_yaml(filename=_CONFIG_PATH)
