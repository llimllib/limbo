"""!nr [-l] chart_name

Show a chart made from new relic data.

To list the available charts, use `!nr -l`
"""
import argparse
from datetime import datetime, timedelta
from dateutil.parser import parse
from io import BytesIO 
import os
from pytz import utc
import re
import requests
import shlex

import matplotlib
# need to call this before importing pyplot
matplotlib.use('Agg')
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from pandas.io.json import json_normalize
import seaborn as sns

NR_API_KEY = os.environ.get("NR_API_KEY")
NR_QUERY_KEY = os.environ.get("NR_QUERY_KEY")
NR_ACCOUNT_ID = os.environ.get("NR_ACCOUNT_ID")

# TODO set this with an mpl style
sns.set(style="darkgrid")

def dtparse(dt):
    return mdates.date2num(parse(dt))

def ffm_graph(nrql, title):
    url = "https://insights-api.newrelic.com/v1/accounts/{}/query?nrql={}".format(NR_ACCOUNT_ID, nrql)
    r = requests.get(url, headers={
        "Accept": "application/json",
        "X-Query-Key": NR_QUERY_KEY})
    pts = [(mdates.date2num(datetime.fromtimestamp(x['beginTimeSeconds'], utc)),
        x['results'][0]['percentiles']['50'],
        x['results'][0]['percentiles']['90'],
        x['results'][0]['percentiles']['95'],
        x['results'][0]['percentiles']['99'])
        for x in r.json()['timeSeries']]

    df = pd.DataFrame(pts, columns=['time', '50', '90', '95', '99'])
    df = df.set_index('time')

    fig, ax = plt.subplots()
    df.plot(ax=ax, title=title)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.yaxis.set_label_text("time in ms")
    ax.legend().set_title("percentiles")

    imgbuf = BytesIO()
    img = ax.figure.savefig(imgbuf, format='png')

    imgbuf.seek(0)
    return imgbuf

def ffm_payment():
    nrql = """SELECT percentile(duration, 50, 90, 95, 99)
                FROM Transaction SINCE 30 minutes ago
                WHERE appName = 'Plan Compare 2.0'
                  AND transactionType = 'Other'
                  AND name='OtherTransaction/Background/FFMGetPayment/run'
              TIMESERIES"""
    return ffm_graph(nrql, "FFM Payment Response Times")


def ffm_get():
    nrql = """SELECT percentile(duration, 50, 90, 95, 99)
                FROM Transaction SINCE 30 minutes ago
                WHERE appName = 'Plan Compare 2.0'
                  AND transactionType = 'Other'
                  AND name='OtherTransaction/Background/FFMGet/run'
              TIMESERIES"""
    return ffm_graph(nrql, "FFM Get Response Times")

def ffm_submit():
    nrql = """SELECT percentile(duration, 50, 90, 95, 99)
                FROM Transaction SINCE 30 minutes ago
                WHERE appName = 'Plan Compare 2.0'
                  AND transactionType = 'Other'
                  AND name='OtherTransaction/Background/FFMSubmit/run'
              TIMESERIES"""
    return ffm_graph(nrql, "FFM Submit Response Times")


def response_times():
    nrql = """SELECT percentile(duration, 50, 90, 95, 99)
                FROM Transaction SINCE 30 minutes ago
               WHERE appName = 'Plan Compare 2.0' AND transactionType = 'Web'
              TIMESERIES"""
    url = "https://insights-api.newrelic.com/v1/accounts/{}/query?nrql={}".format(NR_ACCOUNT_ID, nrql)
    r = requests.get(url, headers={
        "Accept": "application/json",
        "X-Query-Key": NR_QUERY_KEY})
    pts = [(mdates.date2num(datetime.fromtimestamp(x['beginTimeSeconds'], utc)),
        x['results'][0]['percentiles']['50'],
        x['results'][0]['percentiles']['90'],
        x['results'][0]['percentiles']['95'],
        x['results'][0]['percentiles']['99'])
        for x in r.json()['timeSeries']]

    df = pd.DataFrame(pts, columns=['time', '50', '90', '95', '99'])
    df = df.set_index('time')
    fig, ax = plt.subplots()
    df.plot(ax=ax, title="Response Times")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.yaxis.set_label_text("time in ms")
    ax.legend().set_title("percentiles")

    imgbuf = BytesIO()
    img = ax.figure.savefig(imgbuf, format='png')

    imgbuf.seek(0)
    return imgbuf

def count_graph(df, title, dateformat='%H:%M'):
    df = df.set_index('time')
    fig, ax = plt.subplots()
    ax.xaxis_date()
    df.plot(ax=ax, title=title)
    ax.xaxis.set_major_formatter(mdates.DateFormatter(dateformat))
    ax.yaxis.set_label_text("enrollments")

    imgbuf = BytesIO()
    img = ax.figure.savefig(imgbuf, format='png')

    imgbuf.seek(0)
    return imgbuf

def submit_success():
    rpm = requests.get('https://api.newrelic.com/v2/applications/30301056/metrics/data.json',
            headers={'X-Api-Key': NR_API_KEY},
            params={'names[]': 'submit_success', 'values[]': 'call_count'})
    data = rpm.json()
    pts = [(dtparse(x['from']), x['values']['call_count'])
            for x in data["metric_data"]['metrics'][0]['timeslices']]

    df = pd.DataFrame(pts, columns=['time', 'successful_requests'])
    return count_graph(df, "Successful Enrollments")

def submit_error():
    rpm = requests.get('https://api.newrelic.com/v2/applications/30301056/metrics/data.json',
            headers={'X-Api-Key': NR_API_KEY},
            params={'names[]': 'submit_error', 'values[]': 'call_count'})
    data = rpm.json()
    metrics = data["metric_data"]['metrics']
    pts = [(dtparse(x['from']), x['values']['call_count'])
            for x in data["metric_data"]['metrics'][0]['timeslices']]

    df = pd.DataFrame(pts, columns=['time', 'errored_requests'])
    return count_graph(df, "Errored Enrollments")

def ffm_week_over_week():
    nrql = """SELECT average(time)
                FROM PageAction
               WHERE actionName = 'FFMGet'
               SINCE 6 HOURS AGO
              COMPARE WITH 1 WEEK AGO TIMESERIES
    """

    url = "https://insights-api.newrelic.com/v1/accounts/{}/query?nrql={}".format(NR_ACCOUNT_ID, nrql)
    r = requests.get(url, headers={"Accept": "application/json", "X-Query-Key": NR_QUERY_KEY}).json()
    previous = [(d['beginTimeSeconds'], d['results'][0]['average'])
                for d in r['previous']['timeSeries']]
    current = [(d['beginTimeSeconds'], d['results'][0]['average'])
               for d in r['current']['timeSeries']]
    pts = []
    for i, (ts, d) in enumerate(current):
        ts = mdates.date2num(datetime.fromtimestamp(ts, utc))
        pts.append((ts, d, previous[i][1]))

    df = pd.DataFrame(pts, columns=['time', 'current', 'previous'])
    df = df.set_index('time')

    fig, ax = plt.subplots()
    df.plot(ax=ax, title="FFM Get Week over Week")
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.yaxis.set_label_text("time in ms")
    ax.legend().set_title("")

    imgbuf = BytesIO()
    img = ax.figure.savefig(imgbuf, format='png')

    imgbuf.seek(0)
    return imgbuf

def submit_weekly():
    now   = datetime.utcnow()
    from_ = (now - timedelta(7)).isoformat()
    to    = now.isoformat()

    rpm = requests.get('https://api.newrelic.com/v2/applications/30301056/metrics/data.json',
            headers={'X-Api-Key': NR_API_KEY},
            params='names[]=submit_success&names[]=submit_error&values[]=call_count'
                   '&from={}&to={}'.format(from_, to))
    data = rpm.json()

    metrics = data['metric_data']['metrics']

    pts = []
    for i in range(len(metrics[0]['timeslices'])):
        time = dtparse(metrics[0]['timeslices'][i]['from'])
        a = metrics[0]['timeslices'][i]['values']['call_count']
        b = metrics[1]['timeslices'][i]['values']['call_count']
        pts.append((time, a, b))

    df = pd.DataFrame(pts, columns=['time',
        metrics[0]['name'], metrics[1]['name']])

    sum_ = df.sum()
    success, errors = map(int, (sum_['submit_success'], sum_['submit_error']))
    title = 'Enrollments ({} success, {} error)'.format(success, errors)

    return count_graph(df, title, '%b %d')

def submit():
    rpm = requests.get('https://api.newrelic.com/v2/applications/30301056/metrics/data.json',
            headers={'X-Api-Key': NR_API_KEY},
            params='names[]=submit_success&names[]=submit_error&values[]=call_count')
    data = rpm.json()

    metrics = data['metric_data']['metrics']

    pts = []
    for i in range(len(metrics[0]['timeslices'])):
        time = dtparse(metrics[0]['timeslices'][i]['from'])
        a = metrics[0]['timeslices'][i]['values']['call_count']
        b = metrics[1]['timeslices'][i]['values']['call_count']
        pts.append((time, a, b))

    df = pd.DataFrame(pts, columns=['time',
        metrics[0]['name'], metrics[1]['name']])
    return count_graph(df, "Enrollments")

def throughput():
    rpm = requests.get('https://api.newrelic.com/v2/applications/30301056/metrics/data.json',
            headers={'X-Api-Key': NR_API_KEY},
            params={'names[]': 'HttpDispatcher', 'values[]': 'requests_per_minute'})
    data = rpm.json()

    # date2num converts from datetime to matplotlib's particular date format
    # http://matplotlib.org/api/dates_api.html
    pts = [(x['values']['requests_per_minute'], dtparse(x['from']))
            for x in data["metric_data"]['metrics'][0]['timeslices']]
    ds, ts = zip(*pts)

    fig, ax = plt.subplots()
    sns.tsplot(ds, ts, ax=ax, value='Requests Per Minute')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    imgbuf = BytesIO()
    img = fig.savefig(imgbuf, format='png')

    imgbuf.seek(0)
    return imgbuf

charts = {
    "throughput": throughput,
    "response_time": response_times,
    "ffm_get": ffm_get,
    "ffm_submit": ffm_submit,
    "ffm_payment": ffm_payment,
    "success": submit_success,
    "errors": submit_error,
    "submits": submit,
    "submits_weekly": submit_weekly,
    "ffm_get_perf": ffm_week_over_week,
}

def nrq(nrql):
    1/0

def nr(chart):
    return charts.get(chart, charts["throughput"])()

ARGPARSE = argparse.ArgumentParser()
ARGPARSE.add_argument('-l', action='store_true', help="list all available charts")
ARGPARSE.add_argument('-q', help="an NRQL query to run")
ARGPARSE.add_argument('graph', nargs='*', help="the chart to show")

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!nr(.*)?", text)
    if not match:
        return

    if not NR_API_KEY:
        return "New Relic API key not found. Please set the NR_API_KEY " \
               "environment variable to your New Relic API key"

    try:
        ns = ARGPARSE.parse_args(shlex.split(match[0]))
    except SystemExit:
        return __doc__

    if ns.l:
        return "Available charts: {}".format(", ".join(charts.keys()))

    # TODO ns.q
    if ns.q:
        return "not available yet"
        chart = "nrql"
        img = nrq(ns.q)
    else:
        chart = ns.graph[0]
        img = nr(ns.graph[0])

    r = server.slack.api_call("files.upload",
        post_data={"channels": msg["channel"]},
        files={'file': ('{}.png'.format(chart), img, 'image/png')})

    # don't return any messages via RTM
    return ""
