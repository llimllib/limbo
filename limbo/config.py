import logging
import os
from backports import configparser as confparser


class Config(object):

    def __init__(self):
        self.env_config = {}
        self.file_config = None  # type: confparser.ConfigParser
        self.load_env_config()
        self.load_config_file()

    def load_config_file(self):
        config_file = self.env_config.get("config_location", "config.ini")
        # check if config exists
        if not os.path.exists(config_file):
            logger = logging.getLogger(__name__)
            logger.warning("File for configuration not found")
        else:
            self.file_config = confparser.ConfigParser()
            self.file_config.read(config_file)

    def load_env_config(self):
        config = {}
        self._getif(config, "token", "SLACK_TOKEN")
        self._getif(config, "loglevel", "LIMBO_LOGLEVEL")
        self._getif(config, "logfile", "LIMBO_LOGFILE")
        self._getif(config, "logformat", "LIMBO_LOGFORMAT")
        self._getif(config, "plugins", "LIMBO_PLUGINS")
        self._getif(config, "config_location", "LIMBO_CONFIG_LOCATION")
        self.env_config = config

    def _getif(self, config, name, envvar):
        if envvar in os.environ:
            config[name] = os.environ.get(envvar)

    def get_by_section(self, plugin_name, item_name):
        if plugin_name and plugin_name + "_" + str(item_name) in self.env_config.keys():
            return self.env_config[plugin_name + "_" + item_name]
        if not self.file_config:
            return None
        try:
            return self.file_config.get(plugin_name, item_name)
        except confparser.Error:
            return None  # in case of not finding it anywhere

    def get(self, *args):
        if len(args) > 1:
            return self.get_by_section(args[0], args[1])
        return self.get_by_section("BOT", args[0])

    def __getitem__(self, item):
        return self.get("BOT", item)
