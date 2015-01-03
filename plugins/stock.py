"""$<ticker symbol> for a quote on a stock price"""
from __future__ import print_function
import re
import requests
from bs4 import BeautifulSoup
from urllib import quote


def stockprice(ticker):
    url = "https://www.google.com/finance?q={0}"
    print(url.format(quote(ticker)))
    soup = BeautifulSoup(requests.get(url.format(quote(ticker))).text)

    try:
        company, ticker = re.findall(u"^(.+?)\xa0\xa0(.+?)\xa0", soup.text, re.M)[0]
        price = soup.select("#price-panel .pr span")[0].text
        change, pct = soup.select("#price-panel .nwp span")[0].text.split()
        pct.strip('()')

        emoji = ":chart_with_upwards_trend:" if change.startswith("+") else ":chart_with_downwards_trend:"

        return "{0} {1} {2}: {3} {4} {5} {6}".format(emoji, company, ticker, price, change, pct, emoji)
    except Exception as e:
        return ""


def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"\$\w{0,4}", text)
    if not match: return

    prices = [stockprice(ticker[1:]) for ticker in match]
    return "\n".join(p for p in prices if p)
