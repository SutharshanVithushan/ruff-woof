# RUFF WOOF DISCORD BOT

# imports
# standard library imports
import asyncio
import random
import re
import string
import time

# third-part imports
import discord
from discord.ext import commands
from pretty_help import PrettyHelp

#intents
intents = discord.Intents(messages=True, guilds=True)
intents.reactions = True # to be able to manage reactions
intents.members = True # to be able to interact with member updates
intents.typing = False # to disable typing
intents.presences = False #to disable presences


# Moderation category
class Moderation(commands.Cog, description="Commands for Moderation. Uses '$' as prefix."):

    #silence channel
    @commands.has_permissions(administrator=True) # see if command author has admin perms
    @commands.command(name='hush', help='Silence a text channel')
    async def hush(self, ctx, role_name='Members'):
        role_members = discord.utils.get(ctx.guild.roles, name=role_name)
        await ctx.channel.set_permissions(role_members, send_messages=False)
        
        embed_msg = discord.Embed(
        title='Silenced Channel!',
        description=f'By: {ctx.author.mention}'
        )

        await ctx.channel.send(embed=embed_msg)


    #mute command
    @commands.has_permissions(kick_members=True) # see if command author has kick perms
    @commands.command(name='mute', help="Disables the access of a user to send messages")
    async def mute(self, ctx, member: discord.Member, *, reason="No reason provided", timein = 30000):
        role_muted = discord.utils.get(ctx.guild.roles, name='Muted')
        await member.add_roles(role_muted)

        muted_msg = discord.Embed(title=f"**:guide_dog: Muted {member}!**", description=f"**Reason: {reason}**\n**By: {ctx.author.mention}**\n**Time In Seconds: {timein}**")
        await ctx.channel.send(embed=muted_msg)

        timein = int(time)
        time.sleep(timein)
        await member.remove_roles(role_muted)

        unmuted_msg = discord.Embed(title=f"**:guide_dog: unmted {member}!**")
        await ctx.channel.send(embed=unmuted_msg)


    #unmute command
    @commands.has_permissions(kick_members=True) # see if command author has kick perms
    @commands.command(name='unmute', help="Enables the access of a user to send messages")
    async def unmute(self, ctx, member: discord.Member):
        role_muted = discord.utils.get(ctx.guild.roles, name='Muted')
        await member.remove_roles(role_muted)

        unmuted_msg = discord.Embed(title=f"**:guide_dog: Unmted {member}!**", description=f"**By: {ctx.author.mention}**")
        await ctx.channel.send(embed=unmuted_msg)


    #server name check
    @commands.command(name='snc', help="Tells the name of the server/guild")
    async def snc(self, ctx):
        server_name = ctx.message.guild.name
        await ctx.channel.send(discord.Embed(title=f"You Are In {server_name}"))


    #kick command
    @commands.has_permissions(kick_members=True) # see if command author has kick perms
    @commands.command(name='kick', help='Kicks a user from this server')
    async def kick(self, ctx, user: discord.Member, *, reason="No reason provided"):
        server_name = ctx.message.guild.name
        kickmsg = discord.Embed(title=f"**:guide_dog: Kicked {user.name}!**", description=f"**Reason: {reason}**\n**By: {ctx.author.mention}**").set_image(url="https://i.pinimg.com/originals/c0/f1/f8/c0f1f8bfb261a92525cb81501fe82903.gif")
        kickdm = discord.Embed(title=f"You Were Kicked From {server_name}! :door:", description=f"Reason: {reason}\nBy: {ctx.author.mention}").set_image(url="https://emoji.gg/assets/emoji/7886_jimmy.png")

        await ctx.channel.send(embed=kickmsg)
        await user.send(embed=kickdm)
        await user.kick(reason=reason)


    #ban command
    @commands.has_permissions(ban_members=True) # see if command author has ban perms
    @commands.command(name='ban', help='Bans a user from this server')
    async def ban(self, ctx, user: discord.Member, *, reason="No reason provided"):
        server_name = ctx.message.guild.name
        banmsg = discord.Embed(title=f"**:guide_dog: Banned {user.name}!**", description=f"**Reason: {reason}**\n**By: {ctx.author.mention}**").set_image(url="https://media.tenor.com/images/76f50d3ec6888dd3552db1d074435022/tenor.gif")
        bandm = discord.Embed(title=f"You Were Banned From {server_name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}").set_image(url="https://emoji.gg/assets/emoji/7886_jimmy.png")

        await ctx.message.delete()
        await ctx.channel.send(embed=banmsg)
        await user.send(embed=bandm)
        await user.ban(reason=reason)


    #clear command
    @commands.has_permissions(administrator=True) # see if command author has admin perms
    @commands.command(name='clear', help='Clears a set of messages')
    async def clear(self, ctx, amount = 1):
        await ctx.channel.purge(limit=amount+1)
        clear_msg = discord.Embed(title=f":guide_dog: Cleared {amount} Messages!").set_image(url="https://tenor.com/view/shibe-snow-shibe-shaking-shiba-inu-shiba-inu-cute-shiba-gif-19856803")

        await ctx.channel.send(embed=clear_msg)

        time.sleep(5)
        await ctx.channel.purge(limit=1)

# Utility Class
class Utility(commands.Cog, description="Utilities like embeds and other stuff. Uses '$' as prefix."):
    
    #Create embed command
    @commands.command(name='embed', help='Creates an embed with a given title and description.')
    async def embed(self, ctx, title, description):
        embed_msg = discord.Embed(
        title=title,
        description=description
        )

        await ctx.channel.send(embed=embed_msg)


bot = commands.Bot(command_prefix=commands.when_mentioned_or('$'),intents=intents ,help_command=PrettyHelp(color=discord.Color.green()))


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
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name='Not A Woof (Yet)')
    await member.add_roles(role)


@bot.event
async def on_message(message):

    print(str(message.author) + ": " + str(message.content))

    if message.author == bot.user:
        return

    hello_phrases = ['hello', 'hi', 'Hi', 'Hey', 'hey', 'Hello']

    if any(word in hello_phrases for word in isolate(message.content)):
        await message.channel.send('Hello! :wave:')

    if 'konichiwa' in isolate(message.content):
        await message.channel.send('Konichiwa! :wave:')

    if message.content == "ping" or message.content == "ping":
        await message.channel.send("Pong :ping_pong:")

    await bot.process_commands(message)


bot.add_cog(Moderation())
bot.add_cog(Utility())
bot.run("Your Token Here") # Your Bot's Token
