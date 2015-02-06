# Slask
### A [Slack](https://slack.com/) chatbot

![](https://travis-ci.org/llimllib/slask.svg)

## Installation

1. Clone the repo
2. `pip install -r requirements.txt`
3. [Create a bot user](https://my.slack.com/services/new/bot) if you don't have one yet, and copy the API Token
4. Copy `config.py.sample` to `config.py` and paste in the token you got in step 4
5. `python slask.py`
6. Invite Slask into any channels you want it in, or just message it in #general. Try typing `!gif dubstep cat` to test it out

![kitten mittens](http://i.imgur.com/xhmD6QO.png)

## Commands

It's super easy to add your own commands! Just create a python file in the plugins directory with an `on_message` function that returns a string.

You can use the `!help` command to print out all available commands and a brief help message about them. `!help <plugin>` will return just the help for a particular plugin.

These are the current default plugins:

* [calc](https://github.com/llimllib/slask#calc)
* [emoji](https://github.com/llimllib/slask#emoji)
* [flip](https://github.com/llimllib/slask#flip)
* [gif](https://github.com/llimllib/slask#gif)
* [google](https://github.com/llimllib/slask#google-or-search)
* [help](https://github.com/llimllib/slask#help)
* [image](https://github.com/llimllib/slask#image)
* [map](https://github.com/llimllib/slask#map)
* [stock](https://github.com/llimllib/slask#stock)
* [stockphoto](https://github.com/llimllib/slask#stockphoto)
* [weather](https://github.com/llimllib/slask#weather)
* [wiki](https://github.com/llimllib/slask#wiki)
* [youtube](https://github.com/llimllib/slask#youtube)

### calc

![](https://raw.githubusercontent.com/llimllib/slask/master/docs/calc.png)

---

### emoji

![](https://raw.githubusercontent.com/llimllib/slask/master/docs/emoji.png)

---

### flip

![](https://raw.githubusercontent.com/llimllib/slask/master/docs/flip.png)

---

### gif

![](https://raw.githubusercontent.com/llimllib/slask/master/docs/gif.png)

---

### google (or search)

![](https://raw.githubusercontent.com/llimllib/slask/master/docs/google.png)

---

### help

![](https://raw.githubusercontent.com/llimllib/slask/master/docs/help.png)

---

### image

![](https://raw.githubusercontent.com/llimllib/slask/master/docs/image.png)

---

### map

![](https://raw.githubusercontent.com/llimllib/slask/master/docs/map.png)

---

### stock

![](https://raw.githubusercontent.com/llimllib/slask/master/docs/stock.png)

---

### stockphoto

![](https://raw.githubusercontent.com/llimllib/slask/master/docs/stockphoto.png)

---

### weather

![](https://raw.githubusercontent.com/llimllib/slask/master/docs/weather.png)

---

### wiki

![](https://raw.githubusercontent.com/llimllib/slask/master/docs/wiki.png)

---

### youtube

![](https://raw.githubusercontent.com/llimllib/slask/master/docs/youtube.png)

---

## Contributors

* [@fsalum](https://github.com/fsalum)
* [@rodvodka](https://github.com/rodvodka)
* [@mattfora](https://github.com/mattfora)
* [@dguido](https://github.com/dguido)
* [@JoeGermuska](https://github.com/JoeGermuska)
