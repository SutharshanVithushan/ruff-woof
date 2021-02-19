# RUFF WOOF DISCORD BOT

# imports
# standard library imports
import asyncio
import json
import random
import re
import string
import time
import sqlite3

# third-part imports
import discord
import nacl
from discord.ext import commands
from pretty_help import PrettyHelp


conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS list (server_id integer, user_id integer, xp integer, lvl integer)"
)


# add user
def add_user(server_id, user_id, xp, level):
    command = f"INSERT INTO list VALUES ('{server_id}','{user_id}','{xp}','{level}')"
    cursor.execute(command)
    conn.commit()
    print(
        f"Added User with id {user_id} from server with id {server_id} with {xp}xp and {level}level")


# set xp for a user
def set_xp(server_id, user_id, xp):
    command = "SELECT * FROM list"
    cursor.execute(command)

    command = f"UPDATE list SET xp = {xp} WHERE user_id = {user_id} AND server_id = {server_id}"
    cursor.execute(command)
    conn.commit()
    print(f"XP set to {user_id} in {server_id} to {xp}")


# set level for user
def set_lvl(server_id, user_id, lvl):
    command = "SELECT * FROM list"
    cursor.execute(command)

    command = f"UPDATE list SET lvl = {lvl} WHERE user_id = {user_id} AND server_id = {server_id}"
    cursor.execute(command)
    conn.commit()
    if lvl >= 1:
        command = f"UPDATE list SET xp = 0 WHERE user_id = {user_id} AND server_id = {server_id}"
        cursor.execute(command)
        conn.commit()
        print(f"Xp set to 0 for {user_id} in {server_id}")

    print(f"Level set to {user_id} in {server_id} to {lvl}")


# get info about xp for a user
def get_xp_info(server_id, user_id):
    command = f"SELECT * FROM list WHERE user_id = {user_id} AND server_id = {server_id}"
    cursor.execute(command)
    info = cursor.fetchall()
    infos = []
    for item in info:
        for i in item:
            infos.append(i)
    infos = infos[2]
    print(infos)
    return infos


# get info about lvl for a user
def get_lvl_info(server_id, user_id):
    command = f"SELECT * FROM list WHERE user_id = {user_id} AND server_id = {server_id}"
    cursor.execute(command)
    info = cursor.fetchall()
    infos = []
    for item in info:
        for i in item:
            infos.append(i)
    infos = infos[3]
    print(infos)
    return infos


# get all info
def get_all(server_id):
    command = f"SELECT * FROM list WHERE server_id = {server_id}"
    cursor.execute(command)
    info = cursor.fetchall()
    return info


# get all info no server_id
def get_all_no_server():
    command = f"SELECT * FROM list"
    cursor.execute(command)
    infos = cursor.fetchall()
    return infos


# Moderation category
class Moderation(
    commands.Cog, description="Commands for Moderation. Uses '$' as prefix."
):

    # silence channel
    # see if command author has admin perms
    @commands.has_permissions(administrator=True)
    @commands.command(name="hush", help="Silence a text channel")
    async def hush(self, ctx, role_name="Members"):
        role_members = discord.utils.get(ctx.guild.roles, name=role_name)
        await ctx.channel.set_permissions(role_members, send_messages=False)

        embed_msg = discord.Embed(
            title="Silenced Channel!",
            description=f"By: {ctx.author.mention}",
            color=discord.Color.blue(),
        )
        channel = discord.utils.get(ctx.guild.channels, name="woof-bot-log")
        channel_id = channel.id
        channel = bot.get_channel(channel_id)
        await ctx.channel.send(embed=embed_msg)
        await channel.send(embed=embed_msg)

    # unsilence channel
    # see if command author has admin perms
    @commands.has_permissions(administrator=True)
    @commands.command(name="unhush", help="Unsilence a text channel")
    async def hush(self, ctx, role_name="Members"):
        role_members = discord.utils.get(ctx.guild.roles, name=role_name)
        await ctx.channel.set_permissions(role_members, send_messages=True)

        embed_msg = discord.Embed(
            title="Unsilenced Channel!",
            description=f"By: {ctx.author.mention}",
            color=discord.Color.blue(),
        )

        channel = discord.utils.get(ctx.guild.channels, name="woof-bot-log")
        channel_id = channel.id
        channel = bot.get_channel(channel_id)
        await ctx.channel.send(embed=embed_msg)
        await channel.send(embed=embed_msg)

    # mute command
    # see if command author has kick perms
    @commands.has_permissions(kick_members=True)
    @commands.command(name="mute", help="Disables the access of a user to send messages")
    async def mute(self, ctx, member: discord.Member, *, reason="No reason provided", timein=30000):
        role_muted = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.add_roles(role_muted)

        muted_msg = discord.Embed(
            title=f"**:guide_dog: Muted {member}!**",
            description=f"**Reason: {reason}**\n**By: {ctx.author.mention}**\n**Time In Seconds: {timein}**",
            color=discord.Color.teal,
        )

        await ctx.channel.send(embed=muted_msg)

        channel = discord.utils.get(ctx.guild.channels, name="woof-bot-log")
        channel_id = channel.id
        channel = bot.get_channel(channel_id)

        await channel.send(embed=muted_msg)

        timein = int(time)
        time.sleep(timein)

        await member.remove_roles(role_muted)

        unmuted_msg = discord.Embed(
            title=f"**:guide_dog: unmted {member}!**",
            color=discord.Color.teal()
        )

        await ctx.channel.send(embed=unmuted_msg)

        channel = discord.utils.get(ctx.guild.channels, name="woof-bot-log")
        channel_id = channel.id
        channel = bot.get_channel(channel_id)

        await channel.send(embed=unmuted_msg)

    # unmute command
    @commands.has_permissions(manage_roles=True)
    @commands.command(name="unmute", help="Enables the access of a user to send messages")
    async def unmute(self, ctx, member: discord.Member):
        role_muted = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(role_muted)

        unmuted_msg = discord.Embed(
            title=f"**:guide_dog: Unmted {member}!**",
            description=f"**By: {ctx.author.mention}**",
            color=discord.Color.teal()
        )

        channel = discord.utils.get(ctx.guild.channels, name="woof-bot-log")
        channel_id = channel.id
        channel = bot.get_channel(channel_id)

        await ctx.channel.send(embed=unmuted_msg)
        await channel.send(embed=unmuted_msg)

    # kick command
    # see if command author has kick perms
    @commands.has_permissions(kick_members=True)
    @commands.command(name="kicks", help="Kicks a user from this server")
    async def kick(self, ctx, user: discord.Member, *, reason="No reason provided"):
        server_name = ctx.message.guild.name

        kickmsg = discord.Embed(
            title=f"**:guide_dog: Kicked {user.name}!**",
            description=f"**Reason: {reason}**\n**By: {ctx.author.mention}**",
            color=discord.Color.teal(),
        ).set_image(
            url="https://i.pinimg.com/originals/c0/f1/f8/c0f1f8bfb261a92525cb81501fe82903.gif",
        )

        kickdm = discord.Embed(
            title=f"You Were KICKED From {server_name}! :door:",
            color=discord.Color.green()
        ).set_thumbnail(
            url="https://img.icons8.com/ios/452/door-opened.png",
        )

        kickdm.add_field(name="\u200b", value="\u200b", inline=False)
        kickdm.add_field(name="Reason", value=reason, inline=True)
        kickdm.set_footer(
            text="Please refrain from this kind of behaviour in the future."
        )

        channel = discord.utils.get(ctx.guild.channels, name="woof-bot-log")
        channel_id = channel.id
        channel = bot.get_channel(channel_id)

        await channel.send(embed=kickmsg)
        await user.send(embed=kickdm)
        await user.kick(reason=reason)

    # ban command
    # see if command author has ban perms
    @commands.has_permissions(ban_members=True)
    @commands.command(name="ban", help="Bans a user from this server")
    async def ban(self, ctx, user: discord.Member, *, reason="No reason provided"):
        server_name = ctx.message.guild.name
        banmsg = discord.Embed(
            title=f"**:guide_dog: Banned {user.name}!**",
            description=f"**Reason: {reason}**\n**By: {ctx.author.mention}**",
            color=discord.Color.teal(),
        ).set_image(
            url="https://media.tenor.com/images/76f50d3ec6888dd3552db1d074435022/tenor.gif",
        )

        bandm = discord.Embed(
            title=f"You Were BANNED From {server_name}!",
            color=discord.Color.red(),
        ).set_thumbnail(
            url="https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Forbidden_Symbol_Transparent.svg/1200px-Forbidden_Symbol_Transparent.svg.png",
        )

        bandm.add_field(name="Reason", value=reason, inline=True)
        bandm.set_footer(
            text="Please refrain from this kind of behaviour in the future."
        )

        channel = discord.utils.get(ctx.guild.channels, name="woof-bot-log")
        channel_id = channel.id
        channel = bot.get_channel(channel_id)

        await ctx.message.delete()
        await channel.send(embed=banmsg)
        await user.send(embed=bandm)
        await user.ban(reason=reason)

    # unban command
    # see if command author has ban perms
    @commands.has_permissions(ban_members=True)
    @commands.command(name="unban", help="Unbans a user from this server")
    async def unban(self, ctx, id: int, *, reason="No reason provided"):
        server_name = ctx.message.guild.name

        user = await bot.fetch_user(id)

        unbanmsg = discord.Embed(
            title=f"**:guide_dog: Unbanned {user.name}!**",
            description=f"**By: {ctx.author.mention}**",
        ).set_image(
            url="https://media.tenor.com/images/76f50d3ec6888dd3552db1d074435022/tenor.gif",
            color=discord.Color.teal(),
        )

        await ctx.guild.unban(user)

        channel = discord.utils.get(ctx.guild.channels, name="woof-bot-log")
        channel_id = channel.id
        channel = bot.get_channel(channel_id)

        await ctx.message.delete()
        await channel.send(embed=unbanmsg)

    # clear command
    # see if command author has admin perms
    @commands.has_permissions(manage_messages=True)
    @commands.command(name="clear", help="Clears a set of messages")
    async def clear(self, ctx, amount=1):
        await ctx.channel.purge(limit=amount)

        clear_msg = discord.Embed(
            title=f":guide_dog: Cleared {amount} Messages!", color=discord.Color.teal()
        ).set_image(
            url="https://tenor.com/view/shibe-snow-shibe-shaking-shiba-inu-shiba-inu-cute-shiba-gif-19856803"
        )

        await ctx.channel.send(embed=clear_msg)

        channel = discord.utils.get(ctx.guild.channels, name="woof-bot-log")
        channel_id = channel.id
        channel = bot.get_channel(channel_id)

        await ctx.message.delete()
        await channel.send(embed=clear_msg)


# Utility Class
class Utility(commands.Cog, description="Utilities like embeds and other stuff. Uses '$' as prefix."):
    # Display level and Xp of a user in a server
    @commands.command(name="lvl", help="Display your level and xp")
    async def lvl(self, ctx):
        xp = get_xp_info(ctx.guild.id, ctx.author.id)
        lvl = get_lvl_info(ctx.guild.id, ctx.author.id)
        embed = discord.Embed(
            title=f"Level and xp information about {ctx.author.display_name}"
        )
        value_xp_rem = ":white_large_square:" * int(10 - int((xp / 10)))
        value_xp_emoji_in = ":blue_square:" * int((xp / 10))
        value_xp_emoji = "*" + str(value_xp_emoji_in) + str(value_xp_rem) + "*"

        embed.add_field(name="XP", value=xp, inline=True)
        embed.add_field(name="Level", value=f"**{lvl}**")
        embed.add_field(name="Progress Bar", value=value_xp_emoji)

        await ctx.channel.send(embed=embed)

    # Create simple react command
    @ commands.command(name="react", help="Add a reaction to a given message id if possible")
    async def react(self, ctx, message_given=0, reaction=""):
        message = await ctx.fetch_message(message_given)
        await message.add_reaction(reaction)

    # poll command
    @ commands.command(name="poll", help="Create a poll")
    async def poll(self, ctx, title: str, *, o_r_in):
        embed = discord.Embed(title=title).set_author(
            name=ctx.message.author.display_name, icon_url=ctx.message.author.avatar_url
        )

        t_l = o_r_in.split(";")

        for item in t_l:
            stuff = item.split()
            option = stuff[0]
            reaction = stuff[1]
            embed.add_field(name=option, value=f'- {reaction}')

        msg = await ctx.channel.send(embed=embed)

        for item in t_l:
            stuff = item.split()
            reaction = stuff[1]
            await msg.add_reaction(reaction)

    # server info
    @ commands.command(name="s.inf", help="Displays server info")
    async def sinf(self, ctx):
        embed = discord.Embed(title="Server Info",
                              color=discord.Color.teal())

        info_title = [
            "Server Name",
            "Server ID",
            "Server Owner",
            "Member Count",
            "Channel Count",
            "Role Count",
            "Region",
        ]

        infos = [
            str(ctx.message.guild.name),
            str(ctx.message.guild.id),
            str(ctx.guild.owner),
            str(len(ctx.message.guild.members)),
            f"{len(ctx.guild.channels)} \n _includes categories and staff channels_",
            str(len(ctx.message.guild.roles)),
            str(ctx.message.guild.region),
        ]

        i = 0
        for i in range(len(infos)):
            embed.add_field(name=info_title[i], value=infos[i])

        embed.set_thumbnail(url=ctx.guild.icon_url)

        await ctx.channel.send(embed=embed)

    # avatar
    @commands.command(name="mypfp", help="Displays your pfp")
    async def pfp(self, ctx):

        embed = discord.Embed(
            title=f"Avatar of {ctx.author.display_name}",
            color=discord.Color.teal()
        ).set_image(url=ctx.author.avatar_url)

        await ctx.channel.send(embed=embed)


bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("$"),
    intents=discord.Intents.all(),
    help_command=PrettyHelp(color=discord.Color.green()),


)


@bot.event
async def on_ready():
    activity = discord.Activity(
        type=discord.ActivityType.watching, name="The Woof Discord"
    )
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print("Bot Ready!")
    print("")
    print(get_all_no_server())


@bot.event
async def on_member_join(member):
    try:
        role = discord.utils.get(member.guild.roles, name="Not A Woof (Yet)")
        await member.add_roles(role)

    except:
        role = discord.utils.get(member.guild.roles, name="Member")
        await member.add_roles(role)


@bot.event
async def on_message(message):
    log_line = f"\n{message.channel} | {message.author} : {message.content}"
    print(log_line)

    log = open(f'{message.guild.id}_log.txt', 'a')
    log.write(str(log_line))

    if message.author == bot.user:
        return

    if message.content.startswith("$"):
        await bot.process_commands(message)
        return

    info_raw = get_all(message.guild.id)
    print(info_raw)

    info = []

    for item in info_raw:
        for info_tuple in item:
            print(type(info_tuple))
            info.append(info_tuple)

    if not message.author.id in info:
        add_user(message.guild.id, message.author.id, 0, 0)
        await bot.process_commands(message)
        return

    choosen_number = random.randint(0, 5)
    print(choosen_number)
    choosen_xp = int(info[2] + choosen_number)
    choosen_lvl = float(info[3] + int(choosen_xp / 100))
    print(choosen_lvl)
    choosen_lvl = int(choosen_lvl)

    if message.author.id in info:
        set_xp(message.guild.id, message.author.id, choosen_xp)
        set_lvl(message.guild.id, message.author.id, choosen_lvl)

    await bot.process_commands(message)

bot.add_cog(Moderation())
bot.add_cog(Utility())
bot.run("Your Token Here") # Your Bot's Token
