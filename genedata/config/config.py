import os
from ConfigParser import ConfigParser

from unipath import Path


class NotConfigured(Exception):
    pass


PROJECT_ROOT = Path(__file__).ancestor(3)
conf = ConfigParser()
path = os.path.join(PROJECT_ROOT, 'config.ini')
conf.read(path)

def get_setting(section, setting, config=conf):
    try:
        return conf.get(section, setting)
    except KeyError:
        error_msg = "Set {} in the {} section of {}".format(setting, section, path)
        raise NotConfigured(error_msg)
