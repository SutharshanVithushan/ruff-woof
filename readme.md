<h1 align="center">Ruff Woof Discord Bot</h1>

<div align='center'>[![license](https://img.shields.io/github/license/DAVFoundation/captain-n3m0.svg?style=flat-square)](https://github.com/DAVFoundation/captain-n3m0/blob/master/LICENSE)
</div>

A simple discord bot.

## Setup

### Database

```
conn = psycopg2.connect(user="",
                        password="",
                        host="",
                        port="",
                        database="")
```

replace all whitespace strings with the relevant credentials of your postgresql database that you want to use for the levels.

### Bot Token

`bot.run("Your Token")`
replace "Your Token" with your bot's token.

## Commands

### Moderation

**hush** : Silence a text channel

**unhush** : Unsilence a text channel

**mute** : Disables the access of a user to send messages

**unmute** : Enables the access of a user to send messages

**kick** : Kick a user from this server

**ban** : Ban a user from this server

**unban** : Unban a user

**clear** : Clear a set of messages

### Utility

**lvl** : Display your level and xp

**react** : Add a reaction to a given message id if possible

**poll** : Create a poll

**s.inf** : Display the server info

**mypfp** : Display your pfp

**dev-help** : Get help from an active programmer / dev

## Requirements

Install all requirements using `pip install -r requirement.txt`

### Included requirements

**discord.py**
install with pip: `pip install discord.py` or `pip install discord`

**requests**
install with pip: `pip install requests`

**discord-pretty-help**
install with pip: `pip install discord-pretty-help`

**pynacl**
install with pip: `pip install pynacl`

**psycopg2**
install with pip: `pip install psycopg2`

**pillow**
install with pip: `pip install pillow`

## Credits

to **Rizerphe** for:

- the image generator for the level system
- helping with finding a formulae to use for calculating levels
- ideas for embeds and other stuff

to **Metastag** for:

- helping with bugs
- helping with finding a formulae to use for calculating levels
- general ideas to make commands more convenient for users

to **other members of my discord server** for:

- testing the bot
- providing suggestions

to **Me** for:

- being dumb, jk
  Why would I credit myself lmao
  
