# -*- coding: utf-8 -*-
"""!mlb <team> will return that team's upcoming games"""

from datetime import datetime
import re

import requests
from bs4 import BeautifulSoup as Soup

schedules = {
    'arizona diamondbacks': 'http://espn.go.com/mlb/team/schedule/_/name/ari/arizona-diamondbacks',
    'atlanta braves': 'http://espn.go.com/mlb/team/schedule/_/name/atl/atlanta-braves',
    'baltimore orioles': 'http://espn.go.com/mlb/team/schedule/_/name/bal/baltimore-orioles',
    'boston red sox': 'http://espn.go.com/mlb/team/schedule/_/name/bos/boston-red-sox',
    'chicago cubs': 'http://espn.go.com/mlb/team/schedule/_/name/chc/chicago-cubs',
    'chicago white sox': 'http://espn.go.com/mlb/team/schedule/_/name/chw/chicago-white-sox',
    'cincinnati reds': 'http://espn.go.com/mlb/team/schedule/_/name/cin/cincinnati-reds',
    'cleveland indians': 'http://espn.go.com/mlb/team/schedule/_/name/cle/cleveland-indians',
    'colorado rockies': 'http://espn.go.com/mlb/team/schedule/_/name/col/colorado-rockies',
    'detroit tigers': 'http://espn.go.com/mlb/team/schedule/_/name/det/detroit-tigers',
    'houston astros': 'http://espn.go.com/mlb/team/schedule/_/name/hou/houston-astros',
    'kansas city royals': 'http://espn.go.com/mlb/team/schedule/_/name/kc/kansas-city-royals',
    'los angeles angels': 'http://espn.go.com/mlb/team/schedule/_/name/laa/los-angeles-angels',
    'los angeles dodgers': 'http://espn.go.com/mlb/team/schedule/_/name/lad/los-angeles-dodgers',
    'miami marlins': 'http://espn.go.com/mlb/team/schedule/_/name/mia/miami-marlins',
    'milwaukee brewers': 'http://espn.go.com/mlb/team/schedule/_/name/mil/milwaukee-brewers',
    'minnesota twins': 'http://espn.go.com/mlb/team/schedule/_/name/min/minnesota-twins',
    'new york mets': 'http://espn.go.com/mlb/team/schedule/_/name/nym/new-york-mets',
    'new york yankees': 'http://espn.go.com/mlb/team/schedule/_/name/nyy/new-york-yankees',
    'oakland athletics': 'http://espn.go.com/mlb/team/schedule/_/name/oak/oakland-athletics',
    'philadelphia phillies': 'http://espn.go.com/mlb/team/schedule/_/name/phi/philadelphia-phillies',
    'pittsburgh pirates': 'http://espn.go.com/mlb/team/schedule/_/name/pit/pittsburgh-pirates',
    'san diego padres': 'http://espn.go.com/mlb/team/schedule/_/name/sd/san-diego-padres',
    'san francisco giants': 'http://espn.go.com/mlb/team/schedule/_/name/sf/san-francisco-giants',
    'seattle mariners': 'http://espn.go.com/mlb/team/schedule/_/name/sea/seattle-mariners',
    'st. louis cardinals': 'http://espn.go.com/mlb/team/schedule/_/name/stl/st-louis-cardinals',
    'tampa bay rays': 'http://espn.go.com/mlb/team/schedule/_/name/tb/tampa-bay-rays',
    'texas rangers': 'http://espn.go.com/mlb/team/schedule/_/name/tex/texas-rangers',
    'toronto blue jays': 'http://espn.go.com/mlb/team/schedule/_/name/tor/toronto-blue-jays',
    'washington nationals': 'http://espn.go.com/mlb/team/schedule/_/name/wsh/washington-nationals'
}

def fmtdatetime(dt):
    hour = datetime.strftime(dt, "%I").lstrip('0')
    return datetime.strftime(dt, "%m/%d {0}%p".format(hour))

def schedule(query):
    url = None
    query = query.lower()
    for team in schedules:
        if query in team:
            url = schedules[team]
            break

    if not url:
        return "Unable to find {0}".format(query)

    r = requests.get(url)
    soup = Soup(r.text)
    sched = soup.find("table", attrs={"class": "tablehead"})
    games = []
    for row in sched.findAll("tr")[2:]:
        # month name rows have OPPONENT in them
        if "OPPONENT" in row.text:
            continue

        rawdt, rawopp, time = [t.text for t in row.findAll("td")][0:3]
        yr = datetime.strftime(datetime.now(), "%Y")
        try:
            dt = datetime.strptime("{0} {1} {2}".format(rawdt, yr, time), "%a, %b %d %Y %I:%M %p")
        except ValueError:
            # some games are TBA
            dt = datetime.strptime(dt, "%a, %b %d")
        # away games come as @, which is fine. Home games should have the
        # leading "vs" stripped
        opp = rawopp.lstrip("vs")
        games.append((dt, opp))

    next3 = [
        "{0} {1}".format(fmtdatetime(dt), opp)
        for dt, opp
        in games
        if dt > datetime.now()
    ][:3]
    return "{0}: ".format(team.title()) + " :baseball: ".join(next3)

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!mlb (.*)", text)
    if not match:
        return

    return schedule(match[0])
