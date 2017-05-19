"""!define - Returns the oxford dictionary definition of the given term"""
import os
import re
import requests

def define(word):
    app_id = os.environ.get('OXFORD_APP_ID', '')
    app_key = os.environ.get('OXFORD_APP_KEY', '')

    if not app_id or not app_key:
        return "Please set the OXFORD_APP_ID and OXFORD_APP_KEY environment variables " \
               "to valid (free) Oxford dictionary API keys: " \
               "https://developer.oxforddictionaries.com/"

    # LANGUAGE CODES AVAILABLE HERE: https://developer.oxforddictionaries.com/documentation/languages
    language = os.environ.get('OXFORD_LANG_CODE', 'en')

    info = {
        'language': language.lower(),
        'word': word.lower()
    }
    headers = {
        'app_id': app_id,
        'app_key': app_key
    }

    if len(word.split(" ")) > 1:
        return "Please only attempt to define a single word at a time!"

    request_url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/{language}/{word}'.format(**info)
    definition_url = 'https://{language}.oxforddictionaries.com/definition/{word}'.format(**info)

    result = requests.get(request_url, headers=headers)
    if result.status_code == 404:
        return "Oxford has no definition for {0}. If you're searching for the plural, try the singular term".format(
            word)
    elif result.status_code != 200:
        return "Something went wrong when searching for _{0}_! Please try again later".format(word)
    else:
        data = result.json()
        try:
            info['example'] = data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['examples'][0][
                'text']
        except KeyError:
            info['example'] = 'Well this is awkward, no example is given for this definition... :scream:'
        info['definition'] = data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
        info['definition_url'] = definition_url

        return """*Oxford Dictionary Definition for _{word}_*:
>{definition}

*Example usage*:
_{example}_

{definition_url}""".format(**info)

def on_message(msg, server):
    text = msg.get("text", "")
    match = re.findall(r"!define (.*)", text)
    if not match:
        return

    word = match[0]
    return define(word)
