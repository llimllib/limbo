import os
from backports import configparser as confparser


class Config:
    env_config = {}
    file_config = None  # type: confparser.ConfigParser

    def __init__(self):
        self.load_env_config()
        self.load_config_file()

    def load_config_file(self):
        self.file_config = confparser.ConfigParser()
        config_file = self.env_config.get("config_location", "config.ini")
        # check if config exists
        import os
        if not os.path.exists(config_file):
            raise IOError("File for configuration not found")
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

    def get(self, plugin_name, item_name):
        if plugin_name and plugin_name + "_" + item_name in self.env_config.keys():
            return self.env_config[plugin_name + "_" + item_name]
        try:
            return self.file_config.get(plugin_name, item_name)
        except confparser.NoSectionError:
            return None  # in case of not finding it anywhere

    def __getitem__(self, item):
        return self.get("BOT", item)
