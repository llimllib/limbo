# -*- coding: UTF-8 -*-
import json
import os
import sys

import limbo
import pytest
import vcr

DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(DIR, "../../limbo/plugins"))


def msgobj(msg):
    return {"text": msg, "channel": "abc123"}


# Don't leak mapbox and darksky keys. To update the fixtures, you will need to
# disable this function, then manually replace the relevant keys with
# fake_mapbox_token and fake_darksky_key
@pytest.fixture(scope="function", autouse=True)
def weather_env_vars(monkeypatch):
    """Disable environment variables that mess up our tests"""
    monkeypatch.setenv("MAPBOX_API_TOKEN", "fake_mapbox_token")
    monkeypatch.setenv("OPENWEATHER_API_KEY", "fake_openweather_key")


def test_basic():
    from weather import on_message

    server = limbo.FakeServer()
    with vcr.use_cassette("test/fixtures/weather_basic.yaml"):
        on_message(msgobj(u"!weather Oahu, HI"), server)
        attachment = json.loads(server.slack.posted_messages[0][1]["attachments"])[0]
        assert "Weather for Oahu" in attachment["pretext"]
        assert attachment["fields"][0]["value"] == u":sun_behind_rain_cloud: 68°f"


def test_unicode():
    from weather import on_message

    server = limbo.FakeServer()
    with vcr.use_cassette("test/fixtures/weather_unicode.yaml"):
        on_message(msgobj(u"!weather กรุงเทพมหานคร"), server)
        # not blowing up == success


def test_units(monkeypatch):
    from weather import on_message

    monkeypatch.setenv("WEATHER_CELSIUS", "yes")

    server = limbo.FakeServer()
    with vcr.use_cassette("test/fixtures/weather_celsius.yaml"):
        on_message(msgobj(u"!weather Oahu, HI"), server)
        attachment = json.loads(server.slack.posted_messages[0][1]["attachments"])[0]
        assert "Weather for Oahu" in attachment["pretext"]
        assert attachment["fields"][0]["value"] == u":sun_behind_rain_cloud: 20°c"
