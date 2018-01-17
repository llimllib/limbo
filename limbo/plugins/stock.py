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
    soup = BeautifulSoup(
        requests.get(url.format(quote(ticker))).text, "html5lib")

    try:
        company, ticker = re.findall(u"^(.+?)\xa0\xa0(.+?)\xa0", soup.text,
                                     re.M)[0]
    except IndexError:
        logging.info("Unable to find stock {0}".format(ticker))
        return ""
    price = soup.select("#price-panel .pr span")[0].text
    change, pct = soup.select("#price-panel .nwp span")[0].text.split()
    time = " ".join(soup.select(".mdata-dis")[0].parent.text.split()[:4])
    pct.strip('()')

    emoji = ":chart_with_upwards_trend:" if change.startswith("+") \
            else ":chart_with_downwards_trend:"

    return "{0} {1} {2}: {3} {4} {5} {6} {7}".format(
        emoji, company, ticker, price, change, pct, time, emoji)


def on_message(msg, server):
    text = msg.get("text", "")
    basic_re = r"\B\$([a-zA-Z]\w{0,3}(?:\.\w{1,3})?)\b"
    # slack linkifies some tickers, which results in: $<http://wbc.ax|wbc.ax>
    link_re = r"\$<http://([a-zA-Z]\w{0,3}(?:\.\w{1,3})?)\|"
    matches = re.findall(r"{}|{}".format(basic_re, link_re, text), text)
    if not matches:
        return

    tickers = (''.join(list(x)).encode("utf8") for x in matches)
    prices = (stockprice(ticker) for ticker in tickers)
    return "\n".join(p for p in prices if p)


on_bot_message = on_message
