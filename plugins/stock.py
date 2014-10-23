"""$<ticker symbol> for a quote on a stock price"""
import re
import requests
from bs4 import BeautifulSoup
from urllib import quote

def stockprice(ticker):
    url = "https://www.google.com/finance?q={}"
    print url.format(quote(ticker))
    soup = BeautifulSoup(requests.get(url.format(quote(ticker))).text)

    try:
        ticker = re.findall("var _ticker = '(.*?)';", soup.text)[0]
        price = soup.select("#price-panel .pr span")[0].text
        change, pct = soup.select("#price-panel .nwp span")[0].text.split()
        pct.strip('()')

        emoji = ":chart_with_upwards_trend:" if change.startswith("+") else ":chart_with_downwards_trend"

        return "{} {}: {} {} {} {}".format(emoji, ticker, price, change, pct, emoji)
    except:
        return ""

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"\$\w{0,4}", text)
    if not match: return

    prices = [stockprice(ticker[1:]) for ticker in match]
    return "\n".join(p for p in prices if p)
