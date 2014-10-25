# Slask
### A [Slack](https://slack.com/) chatbot

## Installation

1. Clone the repo
2. `pip install -r requirements.txt`
3. Host the web app (a sample wsgi.py is included. See [here](http://flask.pocoo.org/docs/deploying/#deployment) for more on deployment)
4. Add the URL where you deployed the web app as an [outgoing webhook](https://my.slack.com/services/new/outgoing-webhook). Here's what my configuration looks like:
![Here's what my configuration looks like](http://i.imgur.com/k3LZrBJ.png)
5. That's it! Try typing `!gif dubstep cat` into a chat room monitored by slask

![kitten mittens](http://i.imgur.com/xhmD6QO.png)

## Heroku

You can host for free on [Heroku](http://heroku.com). Sign up and follow the steps below to deploy the app.

```bash
heroku create
git push heroku master
heroku ps:scale web=1
heroku ps
heroku logs
```

## Commands

Right now, `!gif`, `!image`, `!youtube`, `!weather`, and `!wiki` are the some of the available commands.

It's super easy to add your own commands! Just create a python file in the plugins directory with an `on_message` function that returns a string.

You can use the `!help` command to print out all available commands and a brief help message about them. `!help <plugin>` will return just the help for a particular plugin.

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

* @fsalum
* @rodvodka
