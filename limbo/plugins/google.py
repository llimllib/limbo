"""!search <query> will return the top google result for that query (!google is an alias)"""
from bs4 import BeautifulSoup
import re
try:
    from urllib import quote, unquote
except ImportError:
    from urllib.request import quote, unquote
import requests

google_api_key = None
google_cse_id = None

def on_init(server):
    global google_api_key
    global google_cse_id
    google_api_key = server.config.get("GOOGLE", "API")
    google_cse_id = server.config.get("GOOGLE", "CSE")

def improved_google(q):
    # google custom search is more acurate than the old search
    # in order to use google custom search configure your account and get your API KEY and CSE ID
    # instructions to configure can be found here: https://stackoverflow.com/a/45911123/2999723
    results = requests.get("https://www.googleapis.com/customsearch/v1?key=%s&cx=%s&q=%s"%(google_api_key, google_cse_id, query)).json()
    #pprint.pprint(results)
    if not results or "items" not in results.keys():
        return ":crying_cat_face: Sorry, google doesn't have an answer for you :crying_cat_face:"
    result = results["items"][0]
    return result["title"] + " in: "+ result["link"]  

def google(q):
    query = quote(q)
    url = "https://encrypted.google.com/search?q={0}".format(query)
    soup = BeautifulSoup(requests.get(url).text, "html5lib")

    answer = soup.findAll("h3", attrs={"class": "r"})
    if not answer:
        return ":crying_cat_face: Sorry, google doesn't have an answer for you :crying_cat_face:"

    try:
        return unquote(re.findall(r"q=(.*?)&", str(answer[0]))[0])
    except IndexError:
        # in this case there is a first answer without a link, which is a
        # google response! Let's grab it and display it to the user.
        return ' '.join(answer[0].stripped_strings)


def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!(?:google|search) (.*)", text)
    if not match:
        return
    if google_api_key and google_cse_id:
        return improved_google(match[0])
    else:
        return google(match[0])


on_bot_message = on_message
