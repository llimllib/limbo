"""$<ticker symbol> for a quote on a stock price"""
from __future__ import print_function
import logging
import re
try:
    from urllib import quote
except ImportError:
    from urllib.request import quote

from bs4 import BeautifulSoup
import requests

logger = logging.getLogger(__name__)

def stockprice(ticker):
    url = "https://www.google.com/finance?q={0}"
    soup = BeautifulSoup(requests.get(url.format(quote(ticker))).text)

    try:
        company, ticker = re.findall(u"^(.+?)\xa0\xa0(.+?)\xa0", soup.text, re.M)[0]
    except IndexError:
        logging.info("Unable to find stock {0}".format(ticker))
        return ""
    price = soup.select("#price-panel .pr span")[0].text
    change, pct = soup.select("#price-panel .nwp span")[0].text.split()
    pct.strip('()')

    emoji = ":chart_with_upwards_trend:" if change.startswith("+") else ":chart_with_downwards_trend:"

    return "{0} {1} {2}: {3} {4} {5} {6}".format(emoji, company, ticker, price, change, pct, emoji)


def on_message(msg, server):
    text = msg.get("text", "")
    matches = re.findall(r"\$[a-zA-Z]\w{0,3}", text)
    if not matches:
        return

    prices = [stockprice(ticker[1:].encode("utf8")) for ticker in matches]
    return "\n".join(p for p in prices if p)
