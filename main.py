# RUFF WOOF DISCORD BOT

# imports
# standard library imports
import asyncio
import json
import random
import re
import string
import time
import nacl

# third-part imports
import discord
from discord.ext import commands
from pretty_help import PrettyHelp

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
        description=f'By: {ctx.author.mention}',
        color=discord.Color.blue()
        )
        channel = discord.utils.get(ctx.guild.channels, name="woof-bot-log")
        channel_id = channel.id
        channel = bot.get_channel(channel_id)
        await ctx.channel.send(embed=embed_msg)
        await channel.send(embed=embed_msg)


    #unsilence channel
    @commands.has_permissions(administrator=True) # see if command author has admin perms
    @commands.command(name='unhush', help='Unsilence a text channel')
    async def hush(self, ctx, role_name='Members'):
        role_members = discord.utils.get(ctx.guild.roles, name=role_name)
        await ctx.channel.set_permissions(role_members, send_messages=True)
        
        embed_msg = discord.Embed(
        title='Unsilenced Channel!',
        description=f'By: {ctx.author.mention}',
        color=discord.Color.blue()
        )
        channel = discord.utils.get(ctx.guild.channels, name="woof-bot-log")
        channel_id = channel.id
        channel = bot.get_channel(channel_id)
        await ctx.channel.send(embed=embed_msg)
        await channel.send(embed=embed_msg)


    #mute command
    @commands.has_permissions(kick_members=True) # see if command author has kick perms
    @commands.command(name='mute', help="Disables the access of a user to send messages")
    async def mute(self, ctx, member: discord.Member, *, reason="No reason provided", timein = 30000):
        role_muted = discord.utils.get(ctx.guild.roles, name='Muted')
        await member.add_roles(role_muted)

        muted_msg = discord.Embed(title=f"**:guide_dog: Muted {member}!**", description=f"**Reason: {reason}**\n**By: {ctx.author.mention}**\n**Time In Seconds: {timein}**", color=discord.Color.teal)
        await ctx.channel.send(embed=muted_msg)
        channel = discord.utils.get(ctx.guild.channels, name="woof-bot-log")
        channel_id = channel.id
        channel = bot.get_channel(channel_id)
        await channel.send(embed=muted_msg)

        timein = int(time)
        time.sleep(timein)
        await member.remove_roles(role_muted)

        unmuted_msg = discord.Embed(title=f"**:guide_dog: unmted {member}!**", color=discord.Color.teal())
        await ctx.channel.send(embed=unmuted_msg)
        channel = discord.utils.get(ctx.guild.channels, name="woof-bot-log")
        channel_id = channel.id
        channel = bot.get_channel(channel_id)
        await channel.send(embed=unmuted_msg)


    #unmute command
    @commands.has_permissions(manage_roles=True)
    @commands.command(name='unmute', help="Enables the access of a user to send messages")
    async def unmute(self, ctx, member: discord.Member):
        role_muted = discord.utils.get(ctx.guild.roles, name='Muted')
        await member.remove_roles(role_muted)

        unmuted_msg = discord.Embed(title=f"**:guide_dog: Unmted {member}!**", description=f"**By: {ctx.author.mention}**", color=discord.Color.teal())
        channel = discord.utils.get(ctx.guild.channels, name="woof-bot-log")
        channel_id = channel.id
        channel = bot.get_channel(channel_id)
        await ctx.channel.send(embed=unmuted_msg)
        await channel.send(embed=unmuted_msg)

    #kick command
    @commands.has_permissions(kick_members=True) # see if command author has kick perms
    @commands.command(name='kicks', help='Kicks a user from this server')
    async def kick(self, ctx, user: discord.Member, *, reason="No reason provided"):
        server_name = ctx.message.guild.name
        kickmsg = discord.Embed(title=f"**:guide_dog: Kicked {user.name}!**", description=f"**Reason: {reason}**\n**By: {ctx.author.mention}**").set_image(url="https://i.pinimg.com/originals/c0/f1/f8/c0f1f8bfb261a92525cb81501fe82903.gif", color=discord.Color.teal())
        kickdm = discord.Embed(title=f"You Were KICKED From {server_name}! :door:").set_thumbnail(url="https://img.icons8.com/ios/452/door-opened.png", color=discord.Color.orange())
        kickdm.add_field(name=' ', value='\u200b', inline=False)
        kickdm.add_field(name='Reason', value=reason, inline=True)
        kickdm.set_footer(text='Please refrain from this kind of behaviour in the future.')

        channel = discord.utils.get(ctx.guild.channels, name="woof-bot-log")
        channel_id = channel.id
        channel = bot.get_channel(channel_id)
        await channel.send(embed=kickmsg)
        await user.send(embed=kickdm)
        await user.kick(reason=reason)


    #ban command
    @commands.has_permissions(ban_members=True) # see if command author has ban perms
    @commands.command(name='ban', help='Bans a user from this server')
    async def ban(self, ctx, user: discord.Member, *, reason="No reason provided"):
        server_name = ctx.message.guild.name
        banmsg = discord.Embed(title=f"**:guide_dog: Banned {user.name}!**", description=f"**Reason: {reason}**\n**By: {ctx.author.mention}**").set_image(url="https://media.tenor.com/images/76f50d3ec6888dd3552db1d074435022/tenor.gif", color=discord.Color.teal())
        bandm = discord.Embed(title=f"You Were BANNED From {server_name}!").set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Forbidden_Symbol_Transparent.svg/1200px-Forbidden_Symbol_Transparent.svg.png", color=discord.Color.red())
        bandm.add_field(name='Reason', value=reason, inline=True)
        bandm.set_footer(text='Please refrain from this kind of behaviour in the future.')

        channel = discord.utils.get(ctx.guild.channels, name="woof-bot-log")
        channel_id = channel.id
        channel = bot.get_channel(channel_id)
        await ctx.message.delete()
        await channel.send(embed=banmsg)
        await user.send(embed=bandm)
        await user.ban(reason=reason)


    #unban command
    @commands.has_permissions(ban_members=True) # see if command author has ban perms
    @commands.command(name='unban', help='Unbans a user from this server')
    async def unban(self, ctx, id: int, *, reason="No reason provided"):
        server_name = ctx.message.guild.name

        user = await bot.fetch_user(id)

        unbanmsg = discord.Embed(title=f"**:guide_dog: Unbanned {user.name}!**", description=f"**By: {ctx.author.mention}**").set_image(url="https://media.tenor.com/images/76f50d3ec6888dd3552db1d074435022/tenor.gif", color=discord.Color.teal())

        await ctx.guild.unban(user)

        channel = discord.utils.get(ctx.guild.channels, name="woof-bot-log")
        channel_id = channel.id
        channel = bot.get_channel(channel_id)
        await ctx.message.delete()
        await channel.send(embed=unbanmsg)


    #clear command
    @commands.has_permissions(manage_messages=True) # see if command author has admin perms
    @commands.command(name='clear', help='Clears a set of messages')
    async def clear(self, ctx, amount = 1):
        await ctx.channel.purge(limit=amount)
        clear_msg = discord.Embed(title=f":guide_dog: Cleared {amount} Messages!", color=discord.Color.teal()).set_image(url="https://tenor.com/view/shibe-snow-shibe-shaking-shiba-inu-shiba-inu-cute-shiba-gif-19856803")

        await ctx.channel.send(embed=clear_msg)
        channel = discord.utils.get(ctx.guild.channels, name="woof-bot-log")
        channel_id = channel.id
        channel = bot.get_channel(channel_id)
        await ctx.message.delete()
        await channel.send(embed=clear_msg)

# Utility Class
class Utility(commands.Cog, description="Utilities like embeds and other stuff. Uses '$' as prefix."):
   
    #Create simple react command
    @commands.command(name='react', help='add a reaction to a given message id if possible')
    async def react(self, ctx, message_given=0, reaction=''):
        message = await ctx.fetch_message(message_given)
        await message.add_reaction(reaction)                    

    
    #server info
    @commands.command(name='s.inf', help='Displays server info')
    async def sinf(self, ctx):
        embed = discord.Embed(title='Server Info', color = discord.Color.teal())
        info_title = ['Server Name', 'Server ID', 'Server Owner', 'Member Count', 'Channel Count', 'Role Count', 'Region']
        infos = [str(ctx.message.guild.name), str(ctx.message.guild.id), str(ctx.guild.owner), str(len(ctx.message.guild.members)), str(len(ctx.message.guild.channels)), str(len(ctx.message.guild.roles)), str(ctx.message.guild.region)]
        i = 0
        for i in range(len(infos)):
            embed.add_field(name=info_title[i], value=infos[i])
            i += 1

        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.channel.send(embed=embed)
    

    #Create simple embed command
    @commands.command(name='embed', help='Creates an embed with a given title, description, thumbnail, and fields')
    async def embed(self, ctx, given_id=0, title="", description="", thumbnail="", field_name="", field_value="", image=""):

        if given_id != 0:
            channel = bot.get_channel(int(given_id))
            embed_msg = discord.Embed(title=title, description=description, color=discord.Color.green())
            embed_msg.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            embed_msg.set_thumbnail(url=thumbnail)
            embed_msg.add_field(name=field_name, value=field_value)

            if image == "":
                await channel.send(embed=embed_msg)

            elif image != "":
                embed_msg.set_image(url=image)
        
        if given_id == 0:
            embed_msg = discord.Embed(title=title, description=description, color=discord.Color.green())
            embed_msg.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            embed_msg.set_thumbnail(url=thumbnail)
            embed_msg.add_field(name=field_name, value=field_value)

            await ctx.channel.send(embed=embed_msg)


#Music Class
class Audio(commands.Cog, description="Play music from youtube"):
    #join music channel
    @commands.command(name="join", help='Join a voice channel')
    async def join(self, ctx):
        try:
            channel=ctx.message.author.voice.channel
            await channel.connect()
        except:
            embed=discord.Embed(title="Join a voice channel before calling me in.", color=discord.Color.teal())
            await ctx.channel.send(embed=embed)

    #leave music channel
    @commands.command(name="leave", help='Leave a voice channel')
    async def leave(self, ctx):
        if (ctx.voice_client): 
            await ctx.guild.voice_client.disconnect()
        else:
            embed=discord.Embed(title="I'm not in a voice channel, use the join command to make me join", color=discord.Color.teal())
            await ctx.channel.send(embed=embed)


bot = commands.Bot(command_prefix=commands.when_mentioned_or('$'),intents=discord.Intents.all() ,help_command=PrettyHelp(color=discord.Color.green()))

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
    try:
        role = discord.utils.get(member.guild.roles, name='Not A Woof (Yet)')
        await member.add_roles(role)
    except:
        role = discord.utils.get(member.guild.roles, name='Member')
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
bot.add_cog(Audio())
bot.run("Your Token Here") # Your Bot's Token
