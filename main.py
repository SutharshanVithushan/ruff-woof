import discord
import random
import time
import json
import re, string

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

client = MyClient()


def isolate(s):
    l = re.findall(r"[\w']+", s)
    words = [''.join(filter(lambda char: char in string.ascii_lowercase, list(word.lower()))) for word in l]
    return words


@client.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.watching, name='The Woof Discord')
    await client.change_presence(status=discord.Status.online, activity=activity)
    print("Bot Ready!")

@client.event
async def on_message(message):
    print(str(message.author) + ": " + str(message.content))

    if message.author == client.user:
        return

    hello_phrases = ['hello', 'hi', 'Hi', 'Hey', 'hey', 'Hello']

    if any(word in hello_phrases for word in isolate(message.content)):
        await message.channel.send('Hello!')

client.run("Your Token Here") # Your Bot's Token
