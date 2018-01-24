# Limbo
### A [Slack](https://slack.com/) chatbot

![](https://travis-ci.org/llimllib/limbo.svg?branch=master)

## Installation

1. Clone the repo
2. [Create a bot user](https://my.slack.com/services/new/bot) if you don't have one yet, and copy the API Token
3. export SLACK_TOKEN="your-api-token"
4. `make run` (or `make repl` for local testing)
5. Invite Limbo into any channels you want it in, or just message it in #general. Try typing `!gif dubstep cat` to test it out

![kitten mittens](http://i.imgur.com/xhmD6QO.png)

I recommend that you always run limbo in a [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/) so that you are running in a clean environment.

## Command Arguments

* --test, -t: Enter command line mode to enter a limbo repl.
* --hook: Specify the hook to test. (Defaults to "message").
* -c: Run a single command.
* --database, -d: Where to store the limbo sqlite3 database. Defaults to limbo.sqlite3.
* --pluginpath, -pp: The path where limbo should look to find its plugins (defaults to /plugins).

## Environment Variables

* SLACK_TOKEN: Slack API token. Required.
* LIMBO_LOGLEVEL: The logging level. Defaults to INFO.
* LIMBO_LOGFILE: File to log info to. Defaults to none.
* LIMBO_LOGFORMAT: Format for log messages. Defaults to `%(asctime)s:%(levelname)s:%(name)s:%(message)s`.
* LIMBO_PLUGINS: Comma-delimited string of plugins to load. Defaults to loading all plugins in the plugins directory (which defaults to "limbo/plugins")

Note that if you are getting an error message about not seeing environment variables, you may be running limbo as `sudo`, which will clear the environment. Use a virtualenv and always run limbo as a user process!

## Commands

It's super easy to add your own commands! Just create a python file in the plugins directory with an `on_message` function that returns a string.

You can use the `!help` command to print out all available commands and a brief help message about them. `!help <plugin>` will return just the help for a particular plugin.

By default, plugins won't react to messages from other bots (just messages from humans). Define an `on_bot_message` function to handle bot messages too. See the example plugins for an easy way to define these functions.

These are the current default plugins:

* [calc](https://github.com/llimllib/limbo/wiki/Calc-Plugin)
* [emoji](https://github.com/llimllib/limbo/wiki/Emoji-Plugin)
* [flip](https://github.com/llimllib/limbo/wiki/Flip-Plugin)
* [gif](https://github.com/llimllib/limbo/wiki/Gif-Plugin)
* [google](https://github.com/llimllib/limbo/wiki/Google-Plugin)
* [help](https://github.com/llimllib/limbo/wiki/Help-Plugin)
* [image](https://github.com/llimllib/limbo/wiki/Image-Plugin)
* [map](https://github.com/llimllib/limbo/wiki/Map-Plugin)
* [poll](https://github.com/llimllib/limbo/wiki/Poll-Plugin)
* [stock](https://github.com/llimllib/limbo/wiki/Stock-Plugin)
* [stockphoto](https://github.com/llimllib/limbo/wiki/Stock-Photo-Plugin)
* [weather](https://github.com/llimllib/limbo/wiki/Weather-Plugin)
* [wiki](https://github.com/llimllib/limbo/wiki/Wiki-Plugin)
* [youtube](https://github.com/llimllib/limbo/wiki/Youtube-Plugin)

## Docker

Docker can be used as an alternative tool for building, testing, and running Limbo.  With this alternative, you only need to install Docker on your dev machine: commands for downloading Limbo's dependencies, building and testing Limbo itself, and, ultimately, running Limbo can be run inside Docker containers.

To build Limbo using Docker, simply type:

```
docker-compose build
```

(This build command -- and all the Docker commands in this section -- must be issued from the root of the Limbo source directory.)  This build command creates an image tagged as simply `limbo` in your local cache maintained by `dockerd`.  The first time you run this command, it will take quite a few minutes because Docker has to download a lot of dependencies.  Subsequent runs will be quite fast because Docker will have cached these dependencies locally.

After you've built the Limbo image, you can test Limbo using Docker by typing:

```
docker-compose run test
```

This command creates a container using the `limbo` image, binds the container's terminal to the terminal of the shell you used to run this command, and then runs the Limbo test suit, sending its output to your terminal.

Assuming the test completes successfull, you can run Limbo in a Docker container by typing:

```
docker-compose run limbo
```

Be sure to set your `SLACK_TOKEN` environment variable before running Slack.  As before, this command will create a container bound to your current terminal and start the Limbo program.  You can type control-C to break out of Limbo.

If for some reason Limbo is detatched from your terminal, you can kill it with the following command:

```
docker stop `docker ps -q --filter ancestor=limbo --format="{{.ID}}"`
```

You can pass command-line arguments to `limbo` by adding them to the command line above.  For example:

```
docker-compose run limbo --help
```

will print the Limbo help message.

The Docker Compose configuration we've provided will automatically pass `SLACK_TOKEN` plus the various `LIMBO_*` environment variables from your shell into the environment of the container used to run Limbo.  If you want to override those variables -- or set a variable not on this list -- you can use the `-e` option, for example:

```
docker-compose run -e LIMBO_LOGLEVEL=DEBUG limbo
```

**Warning to Windows users.**  Docker does no line-ending conversion when creating the build context or copying files from the context into Docker images.  Thus, if you checked-out Limbo with `autocrlf=true` -- and thus converted Unix line-endings into DOS line-endings -- the Docker image created for Limbo can break.  Thus, it's best to checkout Limbo on Windows using `autocrlf=input` (indeed, the Interwebs seem to suggest this is the best setting for all Git work on Windows).  Just be sure your editor doesn't start introducing DOS line-endings when you edit files (be especially careful for new files).


## Contributors

* [@fsalum](https://github.com/fsalum)
* [@rodvodka](https://github.com/rodvodka)
* [@mattfora](https://github.com/mattfora)
* [@dguido](https://github.com/dguido)
* [@JoeGermuska](https://github.com/JoeGermuska)
* [@MathyV](https://github.com/MathyV)
* [@stopspazzing](https://github.com/stopspazzing)
* [@noise](https://github.com/noise)
* [@drewp](https://github.com/drewp)
* [@TetraEtc](https://github.com/TetraEtc)
* [@LivingInSyn](https://github.com/LivingInSyn)
* [@reversegremlin](https://github.com/reversegremlin)
* [@adamghill](https://github.com/adamghill)
* [@PeterGrace](https://github.com/PeterGrace)
* [@SkiftCreative](https://github.com/SkiftCreative)
* [@diceone](https://github.com/diceone)
* [@rnagle](https://github.com/rnagle)
* [@topher200](https://github.com/topher200)
* [@StewPoll](https://github.com/StewPoll)
* [@eSoares](https://github.com/eSoares)
* [@sweinstein89](https://github.com/sweinstein89)
