import discord
import random
import time
import json
import re, string
from discord.ext import commands
from pretty_help import PrettyHelp


class Moderation(commands.Cog, description="Commands for Moderation. Prefix = $"):
    @commands.has_permissions(kick_members=True)
    @commands.command(name='kick', help='Kicks a user from this server')
    async def kick(self, ctx, user: discord.Member, *, reason="No reason provided"):
        kick = discord.Embed(title=f":guide_dog: Kicked {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}")
        kickdm = discord.Embed(title=f"You Were Kicked From ACuteWoof's Community! :door:", description=f"Reason: {reason}\nBy: {ctx.author.mention}")

        await ctx.message.delete()
        await ctx.channel.send(embed=kick)
        await user.send(embed=kickdm)
        await user.kick(reason=reason)


    @commands.has_permissions(administrator=True)
    @commands.command(name='clear', help='Clears a set of messages')
    async def clear(self, ctx, amount = 1):
        await ctx.channel.purge(limit=amount)
        embed_msg = discord.Embed(title=f":guide_dog: Cleared {amount} Messages!")

        await ctx.channel.send(embed=embed_msg)

        time.sleep(2)
        await ctx.channel.purge(limit=1)

bot = commands.Bot(command_prefix=commands.when_mentioned_or('$'), help_command=PrettyHelp())

def isolate(s):
    l = re.findall(r"[\w']+", s)
    words = [''.join(filter(lambda char: char in string.ascii_lowercase, list(word.lower()))) for word in l]
    return words


@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.watching, name='The Woof Discord')
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print("Bot Ready!")


@bot.event
async def on_message(message):
    print(str(message.author) + ": " + str(message.content))

    if message.author == bot.user:
        return

    hello_phrases = ['hello', 'hi', 'Hi', 'Hey', 'hey', 'Hello']

    if any(word in hello_phrases for word in isolate(message.content)):
        await message.channel.send('Hello! :wave:')

    await bot.process_commands(message)


bot.add_cog(Moderation())

client.run("Your Token Here") # Your Bot's Token
