# Slask
### A [Slack](https://slack.com/) chatbot

## Installation

1. Clone the repo
2. Host the web app (a sample wsgi.py is included. See [here](http://flask.pocoo.org/docs/deploying/#deployment) for more on deployment)
3. Add the URL where you deployed the web app as an [outgoing webhook](https://my.slack.com/services/new/outgoing-webhook). Here's what my configuration looks like:
![Here's what my configuration looks like](http://i.imgur.com/k3LZrBJ.png)
4. That's it! Try typing `!gif dubstep cat` into a chat room monitored by slask

## Commands

Right now, `!gif`, `!image` and `!wiki` are the only available commands.

It's super easy to add your own commands! Just create a python file in the plugins directory with an `on_message` function that returns a string.
