import requests, re, random
from bs4 import BeautifulSoup


COMEDIAN_NAMES = {'Seth': 'Seth Meyers',
                  'Letterman': 'David Letterman',
                  'Kimmel': 'Jimmy Kimmel',
                  'Conan': 'Conan O\'Brian',
                  'Fallon': 'Jimmy Fallon',
                  'Ferguson': "Craig Ferguson"}


def get_name(string):
    for name in COMEDIAN_NAMES:
        if len(re.findall(name, string)):
            return COMEDIAN_NAMES[name]


def monologue(msg):
    """!monologue: joke from night shows """
    body = "%(body)s" % msg
    reg = re.compile('!monologue', re.IGNORECASE)
    match = reg.findall(body)
    if not match:
        return False
    monologue_dict = {}
    r = requests.get('http://www.newsmax.com/jokes/')
    soup = BeautifulSoup(r.text)
    jokepage = soup.body.find('div', 'jokespage')
    for comedian in jokepage.find_all('div'):
        if 'jokesHeader' not in comedian.attrs['class']:
            break
        img_name = comedian.find('img').attrs.get('alt')
        comedian_name = get_name(img_name)
        monologue = comedian.find_next('p')
        while(monologue.name == 'p'):
            monologue_dict.setdefault(comedian_name, []).append(monologue.text)
            monologue = monologue.find_next()

    name = random.choice(monologue_dict.keys())
    monologue = random.choice(monologue_dict[name])
    return monologue + ' --' + name


def hedberg_joke(msg):
    body = "%(body)s" % msg
    reg = re.compile('!hedberg', re.IGNORECASE)
    match = reg.findall(body)
    if not match:
        return False
    url = "https://raw.githubusercontent.com/petdance/scraps/master/mitch-fortunes.txt"
    r = requests.get(url)
    if r.status_code != 200:
        return "Error"
    jokes = r.text.split('%')
    return random.choice(jokes)


def on_message(msg, server):
    return monologue(msg) or hedberg_joke(msg)

