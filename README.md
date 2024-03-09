# Limbo

### A [Slack](https://slack.com/) chatbot

## Status

At the moment, I consider limbo to be feature complete, and the project is in maintenance mode. Every once in a while I come in and update the dependencies.

Contributions will be considered and may be accepted, you may want to [email me](bill@billmill.org) because I might not notice your PR.

## Python Versions

At the moment, this software only officially supports python >=3.10, because the test fixtures fail on older versions of python due to an urllib3 inconsistency I don't understand.

It should still run on other versions of python, but for the moment they're unfortunately not tested.

## Installation

1. Clone the repo
2. [Create a bot user](https://my.slack.com/services/new/bot) if you don't have one yet, and copy the API Token
3. export SLACK_TOKEN="your-api-token"
4. `make run` (or `make repl` for local testing)
5. Invite Limbo into any channels you want it in, or just message it in #general. Try typing `!gif dubstep cat` to test it out

![kitten mittens](http://i.imgur.com/xhmD6QO.png)

I recommend that you always run limbo in a [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) so that you are running in a clean environment.

## Command Arguments

- `--test`, `-t`: Enter command line mode to enter a limbo repl.
- `--hook`: Specify the hook to test. (Defaults to "message").
- `-c`: Run a single command.
- `--database`, `-d`: Where to store the limbo sqlite3 database. Defaults to limbo.sqlite3.
- `--pluginpath`, `-pp`: The path where limbo should look to find its plugins (defaults to /plugins).
- `--version`, `-v`: Print a version number and exit

## Environment Variables

- SLACK_TOKEN: Slack API token. Required.
- LIMBO_LOGLEVEL: The logging level. Defaults to INFO.
- LIMBO_LOGFILE: File to log info to. Defaults to none.
- LIMBO_LOGFORMAT: Format for log messages. Defaults to `%(asctime)s:%(levelname)s:%(name)s:%(message)s`.
- LIMBO_PLUGINS: Comma-delimited string of plugins to load. Defaults to loading all plugins in the plugins directory (which defaults to "limbo/plugins")

Note that if you are getting an error message about not seeing environment variables, you may be running limbo as `sudo`, which will clear the environment. Use a virtualenv and always run limbo as a user process!

## Commands

It's super easy to add your own commands! Just create a python file in the plugins directory with an `on_message` function that returns a string.

You can use the `!help` command to print out all available commands and a brief help message about them. `!help <plugin>` will return just the help for a particular plugin.

By default, plugins won't react to messages from other bots (just messages from humans). Define an `on_bot_message` function to handle bot messages too. See the example plugins for an easy way to define these functions.

These are the current default plugins:

- [emoji](https://github.com/llimllib/limbo/wiki/Emoji-Plugin)
- [flip](https://github.com/llimllib/limbo/wiki/Flip-Plugin)
- [gif](https://github.com/llimllib/limbo/wiki/Gif-Plugin)
- [google](https://github.com/llimllib/limbo/wiki/Google-Plugin)
- [help](https://github.com/llimllib/limbo/wiki/Help-Plugin)
- [image](https://github.com/llimllib/limbo/wiki/Image-Plugin)
- [map](https://github.com/llimllib/limbo/wiki/Map-Plugin)
- [poll](https://github.com/llimllib/limbo/wiki/Poll-Plugin)
- [weather](https://github.com/llimllib/limbo/wiki/Weather-Plugin)
- [wiki](https://github.com/llimllib/limbo/wiki/Wiki-Plugin)

## Contributors

- [@fsalum](https://github.com/fsalum)
- [@rodvodka](https://github.com/rodvodka)
- [@mattfora](https://github.com/mattfora)
- [@dguido](https://github.com/dguido)
- [@JoeGermuska](https://github.com/JoeGermuska)
- [@MathyV](https://github.com/MathyV)
- [@stopspazzing](https://github.com/stopspazzing)
- [@noise](https://github.com/noise)
- [@drewp](https://github.com/drewp)
- [@TetraEtc](https://github.com/TetraEtc)
- [@LivingInSyn](https://github.com/LivingInSyn)
- [@reversegremlin](https://github.com/reversegremlin)
- [@adamghill](https://github.com/adamghill)
- [@PeterGrace](https://github.com/PeterGrace)
- [@SkiftCreative](https://github.com/SkiftCreative)
- [@diceone](https://github.com/diceone)
- [@rnagle](https://github.com/rnagle)
- [@topher200](https://github.com/topher200)
- [@StewPoll](https://github.com/StewPoll)
- [@eSoares](https://github.com/eSoares)
- [@sweinstein89](https://github.com/sweinstein89)
- [@fenwar](https://github.com/fenwar)
- [@rdimartino](https://github.com/rdimartino)
