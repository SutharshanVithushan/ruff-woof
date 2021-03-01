# RUFF WOOF DISCORD BOT

# imports
# standard library imports
import asyncio
import io
import json
import random
import re
import string
import time

# third-part imports
import discord
import nacl
import psycopg2
import requests
from discord.ext import commands
from PIL import Image, ImageDraw, ImageEnhance, ImageFont
from pretty_help import PrettyHelp


def rounded_rectangle(self: ImageDraw, xy, corner_radius, fill=None, outline=None):
    upper_left_point = xy[0]
    bottom_right_point = xy[1]
    self.rectangle(
        [
            (upper_left_point[0], upper_left_point[1] + corner_radius),
            (bottom_right_point[0], bottom_right_point[1] - corner_radius),
        ],
        fill=fill,
        outline=outline,
    )
    self.rectangle(
        [
            (upper_left_point[0] + corner_radius, upper_left_point[1]),
            (bottom_right_point[0] - corner_radius, bottom_right_point[1]),
        ],
        fill=fill,
        outline=outline,
    )
    self.pieslice(
        [
            upper_left_point,
            (
                upper_left_point[0] + corner_radius * 2,
                upper_left_point[1] + corner_radius * 2,
            ),
        ],
        180,
        270,
        fill=fill,
        outline=outline,
    )
    self.pieslice(
        [
            (
                bottom_right_point[0] - corner_radius * 2,
                bottom_right_point[1] - corner_radius * 2,
            ),
            bottom_right_point,
        ],
        0,
        90,
        fill=fill,
        outline=outline,
    )
    self.pieslice(
        [
            (upper_left_point[0], bottom_right_point[1] - corner_radius * 2),
            (upper_left_point[0] + corner_radius * 2, bottom_right_point[1]),
        ],
        90,
        180,
        fill=fill,
        outline=outline,
    )
    self.pieslice(
        [
            (bottom_right_point[0] - corner_radius * 2, upper_left_point[1]),
            (bottom_right_point[0], upper_left_point[1] + corner_radius * 2),
        ],
        270,
        360,
        fill=fill,
        outline=outline,
    )


ImageDraw.rounded_rectangle = rounded_rectangle


def draw(icon, xp, level, name, avt_size=1, avatar_x=600, avatar_y=745):
    image = (
        ImageEnhance.Brightness(
            Image.open(
                io.BytesIO(
                    requests.get(
                        # "http://picsum.photos/5000/1500?grayscale&&blur=4"
                        "https://picsum.photos/id/1045/5000/1500?blur=5"
                    ).content
                )
            )
        )
        .enhance(0.5)
        .convert("RGB")
    )
    draw = ImageDraw.Draw(image)
    draw.ellipse(
        (
            avatar_x - 445 * avt_size - 50,
            avatar_y - 445 * avt_size - 50,
            avatar_x + 445 * avt_size + 50,
            avatar_y + 445 * avt_size + 50,
        ),
        (0, 0, 0),
    )
    mask = Image.new("L", image.size)
    draw = ImageDraw.Draw(mask)
    draw.ellipse(
        (
            int(avatar_x - 445 * avt_size),
            int(avatar_y - 445 * avt_size),
            int(avatar_x + 445 * avt_size),
            int(avatar_y + 445 * avt_size),
        ),
        255,
    )
    pasted = Image.new("RGB", image.size)
    avatar = Image.open(io.BytesIO(requests.get(icon).content)).resize(
        (int(890 * avt_size), int(890 * avt_size))
    )
    pasted.paste(
        avatar, (int(avatar_x - 445 * avt_size),
                 int(avatar_y - 445 * avt_size))
    )
    composite = Image.composite(pasted, image, mask)
    draw = ImageDraw.Draw(composite)
    rounded_rectangle(draw, ((1150, 1150), (4850, 1350)), 100, (255, 255, 255))
    rounded_rectangle(
        draw, ((1200, 1200), (1300 + (4700 - 1200)
                              * xp / 100, 1300)), 50, (0, 0, 0)
    )

    try:
        draw.text(
            (1200, 100),
            name,
            font=ImageFont.truetype("Arial", 400),
            fill=(255, 255, 255),
        )
        draw.text(
            (1200, 600),
            f"lvl #{level}, {xp} xp",
            font=ImageFont.truetype("Arial", 300),
            fill=(255, 255, 255),
        )
    except OSError:
        draw.text(
            (1200, 100),
            name,
            font=ImageFont.truetype("arial.ttf", 400),
            fill=(255, 255, 255),
        )
        draw.text(
            (1200, 600),
            f"lvl #{level}, {xp} xp",
            font=ImageFont.truetype("arial.ttf", 300),
            fill=(255, 255, 255),
        )

    result = composite.resize((500, 150), Image.ANTIALIAS)

    return result


conn = psycopg2.connect(user="",
                        password="",
                        host="",
                        port="",
                        database=""
                        )

cursor = conn.cursor()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS list (server_id text, user_id text, xp integer, lvl integer)"
)


# add user
def add_user(server_id, user_id, xp, level):
    command = f"INSERT INTO list VALUES ('{server_id}','{user_id}','{xp}','{level}')"
    cursor.execute(command)
    conn.commit()
    print(
        f"Added User with id '{user_id}' from server with id '{server_id}' with {xp}xp and {level}level")


# set xp for a user
def set_xp(server_id, user_id, xp):
    command = "SELECT * FROM list"
    cursor.execute(command)

    command = f"UPDATE list SET xp = {xp} WHERE user_id = '{user_id}' AND server_id = '{server_id}'"
    cursor.execute(command)
    conn.commit()
    print(f"XP set to '{user_id}' in '{server_id}' to {xp}")


# set level for user
def set_lvl(server_id, user_id, lvl, calc_lvl):
    command = "SELECT * FROM list"
    conn.commit()
    cursor.execute(command)

    command = f"UPDATE list SET lvl = {lvl} WHERE user_id = '{user_id}' AND server_id = '{server_id}'"
    conn.commit()
    cursor.execute(command)
    conn.commit()
    print(f"Level set to {user_id} in {server_id} to {lvl}")

    if calc_lvl >= 1:
        command = f"UPDATE list SET xp = 0 WHERE user_id = '{user_id}' AND server_id = '{server_id}'"
        conn.commit()
        cursor.execute(command)
        conn.commit()
        print(f"XP set to '{user_id}' in '{server_id}' to 0")


# get info about xp for a user
def get_xp_info(server_id, user_id):
    command = f"SELECT * FROM list WHERE user_id = '{user_id}' AND server_id = '{server_id}'"
    conn.commit()
    cursor.execute(command)
    info = cursor.fetchall()
    infos = []
    for item in info:
        for i in item:
            infos.append(i)
    try:
        infos = infos[2]
    except IndexError:
        return 'e'
    print(infos)
    return infos


# get info about lvl for a user
def get_lvl_info(server_id, user_id):
    conn.commit()
    command = f"SELECT * FROM list WHERE user_id = '{user_id}' AND server_id = '{server_id}'"
    cursor.execute(command)
    info = cursor.fetchall()
    print(info)
    return info


# get all info
def get_all(server_id):
    command = f"SELECT * FROM list WHERE server_id = '{server_id}'"
    conn.commit()
    cursor.execute(command)
    info = cursor.fetchall()
    return info


# get all info no server_id
def get_all_no_server():
    command = f"SELECT * FROM list"
    conn.commit()
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
    async def unhush(self, ctx, role_name="Members"):
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
    @commands.has_permissions(manage_roles=True)
    @commands.command(name="mute", help="Disables the access of a user to send messages")
    async def mute(self, ctx, member: discord.Member, *, reason="No reason provided"):
        role_muted = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.add_roles(role_muted)

        muted_msg = discord.Embed(
            title=f"**:guide_dog: Muted {member}!**",
            description=f"**Reason: {reason}**\n**By: {ctx.author.mention}**\n**Time In Seconds: {timein}**",
            color=discord.Color.teal(),
        )

        await ctx.channel.send(embed=muted_msg)

        channel = discord.utils.get(ctx.guild.channels, name="woof-bot-log")
        channel_id = channel.id
        channel = bot.get_channel(channel_id)

        await channel.send(embed=muted_msg)

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
        user = await bot.fetch_user(id)

        unbanmsg = discord.Embed(
            title=f"**:guide_dog: Unbanned {user.name}!**",
            description=f"**By: {ctx.author.mention}**",
            colro=discord.Color.teal()
        ).set_image(
            url="https://media.tenor.com/images/76f50d3ec6888dd3552db1d074435022/tenor.gif",
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
    @ commands.command(name="lvl", help="Display your level and xp")
    async def lvl(self, ctx):
        msg = await ctx.channel.send("Retrieving info. Please wait, this might take a few seconds")
        xp = get_xp_info(ctx.guild.id, ctx.author.id)
        lvl_in = get_lvl_info(ctx.guild.id, ctx.author.id)
        lvl = []

        for i in lvl_in:
            for item in i:
                lvl.append(item)

        lvl = lvl[3]

        if xp == 'e':
            ctx.channel.send("Chat before you can get levels.")

        # embed = discord.Embed(
        #     title=f"Level and xp information about {ctx.author.display_name}"
        # )
        # value_xp_rem = ":white_large_square:" * int(10 - int((xp / 100)))
        # value_xp_emoji_in = ":blue_square:" * int((xp / 100))
        # value_xp_emoji = "*" + str(value_xp_emoji_in) + str(value_xp_rem) + "*"
        #
        # embed.add_field(name="XP", value=xp, inline=True)
        # embed.add_field(name="Level", value=f"**{lvl}**")
        # embed.add_field(name="Progress Bar", value=value_xp_emoji)

        img = draw(str(ctx.message.author.avatar_url), xp,
                   lvl, str(ctx.message.author.display_name))

        arr = io.BytesIO()
        img.save(arr, format='PNG')
        arr.seek(0)
        file = discord.File(
            arr, filename=f"rank of {ctx.message.author.display_name!r}.png")
        await ctx.channel.send(file=file)
        await msg.delete()

        # await ctx.channel.send(embed=embed)

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
    @ commands.command(name="mypfp", help="Displays your pfp")
    async def pfp(self, ctx, help_str: str):

        embed = discord.Embed(
            title=f"Avatar of {ctx.author.display_name}",
            color=discord.Color.teal()
        ).set_image(url=ctx.author.avatar_url)

        await ctx.channel.send(embed=embed)

    # help-needed-dev
    @commands.command(name="dev-help", help='Get help from an active programmer')
    async def dev_h(self, ctx):
        basic = discord.utils.get(ctx.guild.roles, name="Puppy")
        medium = discord.utils.get(ctx.guild.roles, name="Woof")
        loud = discord.utils.get(ctx.guild.roles, name="Loud Woof")
        programmer = discord.utils.get(ctx.guild.roles, name="Programmer")

        members_basic = []
        members_medium = []
        members_loud = []

        active_members_list = []

        for member in ctx.guild.members:
            if loud in member.roles:
                members_loud.append(member)

            elif basic in member.roles:
                members_basic.append(member)

            elif medium in member.roles:
                members_medium.append(member)

        for mem in members_loud:
            if programmer in mem.roles:
                active_members_list.append(mem)
        for mem in members_medium:
            if programmer in mem.roles:
                active_members_list.append(mem)

        if active_members_list == []:
            for mem in members_basic:
                if programmer in mem.roles:
                    active_members_list.append(mem)
        try:
            choosen_dev = random.choice(active_members_list)
            await ctx.channel.send(f'Hey {choosen_dev.mention} {ctx.author.mention} needs dev help!')
        except IndexError:
            await ctx.channel.send('No active members :frowning:')


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
        role = discord.utils.get(member.guild.roles, name="Members")
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

    # Roles
    # {
    basic_role = discord.utils.get(message.guild.roles, name="Puppy")

    medium_role = discord.utils.get(message.guild.roles, name="Woof")

    loud_role = discord.utils.get(message.guild.roles, name="Loud Woof")
    # }

    try:
        info = get_lvl_info(message.guild.id, message.author.id)
        lvl = []
        for i in info:
            for item in i:
                lvl.append(item)
        lvl = lvl[3]
    except:
        print("ERROR")
        pass

    info_raw = get_lvl_info(message.guild.id, message.author.id)
    print(info_raw)

    info = []

    for item in info_raw:
        for info_tuple in item:
            print(type(info_tuple))
            info.append(info_tuple)

    print("OUTPUT")
    print(info)

    if not str(message.author.id) in info:
        add_user(message.guild.id, message.author.id, 0, 0)
        await bot.process_commands(message)
        return

    choosen_number = random.randint(1, 3)
    print(choosen_number)
    choosen_xp = int(info[2] + choosen_number)
    calc_lvl = choosen_xp / 100
    choosen_lvl = float(info[3] + calc_lvl)
    print(choosen_lvl)
    choosen_lvl = int(choosen_lvl)

    if str(message.author.id) in info:
        set_xp(message.guild.id, message.author.id, choosen_xp)
        set_lvl(message.guild.id, message.author.id, choosen_lvl, calc_lvl)

        if choosen_lvl > lvl:
            await message.channel.send(f"Congratulations! {message.author.mention}, You reached level {choosen_lvl}! :tada:")

        if choosen_lvl >= 5 and choosen_lvl <= 9 and basic_role not in message.author.roles:
            message.author.add_roles(basic_role)

        if choosen_lvl >= 10 and choosen_lvl <= 24 and medium_role not in message.author.roles:
            message.author.add_roles(medium_role)

        if choosen_lvl >= 15 and loud_role not in message.author.roles:
            message.author.add_roles(loud_role)

    await bot.process_commands(message)

bot.add_cog(Moderation())
bot.add_cog(Utility())
bot.run("Your Token Here")
