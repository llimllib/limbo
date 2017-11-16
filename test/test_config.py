# -*- coding: UTF-8 -*-
import os

DIR = os.path.dirname(os.path.realpath(__file__))
PARENT = os.path.split(DIR)[0]

from limbo.config import Config


def test_config():
    # test wrong config location
    os.environ["LIMBO_CONFIG_LOCATION"] = "config_non_existent.ini"
    try:
        config = Config()
        assert False
    except IOError:
        assert True

    # know a correct config location
    os.environ["LIMBO_CONFIG_LOCATION"] = "config.ini"
    config = Config()
    assert config["SLACK_TOKEN"] == "token"

    # test non existing setting
    result = config.get("weather", "weather_token")
    assert not result

