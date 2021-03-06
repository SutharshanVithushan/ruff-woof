# Ruff Woof Discord Bot

This discord bot was created by **ACuteWoof** (ACuteWoof#7510 _on discord_, [on youtube](https://www.youtube.com/channel/UCLa0rouVotfUdDtUrlSdcug "Youtube Channel Of ACuteWoof")), with the help of **Rizerphe**#2538 and **Metastag**#2509.
Special thanks to them for their contributions in making this bot :D

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

_requirements also included in requirements.txt :D_

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
