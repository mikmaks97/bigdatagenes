import os
from configparser import ConfigParser

from unipath import Path


class NotConfigured(Exception):
    pass


PROJECT_ROOT = Path(__file__).ancestor(3)
config = ConfigParser()
path = os.path.join(PROJECT_ROOT, 'config.ini')
config.read(path)

def get_setting(section, setting, config=config):
    try:
        return config[section][setting]
    except KeyError:
        error_msg = "Set {} in the {} section of {}".format(setting, section, path)
        raise NotConfigured(error_msg)
