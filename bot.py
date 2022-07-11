from difflib import Match
import discord
import Match_Builder
from discord.ext import commands
from pymongo import MongoClient

uri = "mongodb+srv://abhinav:sogya@cluster0.mmjoj3r.mongodb.net/discord-bot?retryWrites=true&w=majority"
token = "OTk0OTUyMTIxODMxMTQ1NTUy.GUSuq6.Pgsl6ma0FqQ2TmP4pgShJxBfAqsGDKvGWaHW_M"

cluster = MongoClient(uri)

db = cluster['discord-bot']

servers = db['servers']
participantsList = db['participantsList']
matchesList = db['matchesList']
detailToNode = db['detailToNode']
newMatchesList = db['newMatchesList']

intents = discord.Intents().all()
client = commands.Bot(command_prefix="p!", intents=intents)

botName = "Lockout Bot"

def to_match_builder(ctx):
    Match_Builder.detail_to_node = dict(detailToNode.find_one({"server": ctx.guild.id})["value"])
    Match_Builder.matchlist = list(matchesList.find_one({"server": ctx.guild.id})["value"])
    Match_Builder.newmatchlist = list(newMatchesList.find_one({"server": ctx.guild.id})["value"])

def from_match_builder(ctx):
    detailToNode.update_one({"server": ctx.guild.id}, {"$set": {"value" : str(Match_Builder.detail_to_node)}})
    matchesList.update_one({"server": ctx.guild.id}, {"$set": {"value" : str(Match_Builder.matchlist)}})
    newMatchesList.update_one({"server": ctx.guild.id}, {"$set": {"value" : str(Match_Builder.newmatchlist)}})


@client.event
async def on_message(message):
    thisServer = servers.find_one({"_id": message.guild.id})
    if(thisServer["lockout_bot"] == int(message.author.id)):

        text_channel_n = thisServer["text_channel"]
        global text_channel
        for x in message.guild.text_channels:
            if x.id == text_channel_n:
                text_channel = x

        embed = discord.Embed(
            title="hi",
            description="hello",
            color=discord.Color.gold()
        )
        embed.set_author(name=botName)
        await text_channel.send(embed=embed)
        return


@client.event
async def on_guild_join(guild):
    res = servers.find_one({"_id": guild.id})
    if res is None:
        # print(guild)
        text_channel = guild.text_channels[0]
        servers.insert_one({"_id": guild.id, "text_channel": text_channel.id, "tourney_name": "--", "lockout_bot": 0})
        embed = discord.Embed(
            title="welcome to Lockout Bot",
            description="ThankYou for adding Lockout Bot to your server",
            color=discord.Color.gold()
        )
        embed.set_author(name="Akshay Khandelwal, Harsh Raj, Abhinav Ayush")
        await text_channel.send(embed=embed)


@client.command()
@commands. has_role('Tourney Manager')
# @commands.is_owner()
async def channel(ctx, text_channel: discord.TextChannel):
    # print(ctx.guild)
    global prev_channel
    prev = servers.find_one({"_id": ctx.guild.id})["text_channel"]
    servers.update_one({"_id": ctx.guild.id}, {"$set": {"text_channel": text_channel.id}})
    for x in ctx.guild.text_channels:
        if x.id == prev:
            prev_channel = x

    servers.find_one({"_id": ctx.guild.id})["text_channel"] = text_channel.id

    if prev == text_channel.id:
        embed = discord.Embed(
            title="Channel Changed",
            description=f"I am already in that channel",
            color=discord.Color.gold()
        )
        embed.set_author(name=botName)
        await text_channel.send(embed=embed)
        return

    embed = discord.Embed(
        title="Channel Changed",
        description=f"Bot's channel changed to {text_channel.mention}",
        color=discord.Color.gold()
    )
    embed2 = discord.Embed(
        title="Channel Changed",
        description=f"Bot's channel changed to {text_channel.mention}",
        color=discord.Color.gold()
    )
    embed.set_author(name=botName)
    await text_channel.send(embed=embed)
    await prev_channel.send(embed=embed2)


async def get_person_from_id(server, id):
    for x in server.users:
        if x.id == id:
            return x

    return server.users[0]


@client.command()
@commands. has_role('Tourney Manager')
async def startRegister(ctx, tourneyName: str):
    thisServer = servers.find_one({"_id": ctx.guild.id})
    text_channel_n = thisServer["text_channel"]
    global text_channel
    for x in ctx.guild.text_channels:
        if x.id == text_channel_n:
            text_channel = x

    if thisServer["lockout_bot"] == 0:
        embed = discord.Embed(
            title="No Lockout Bot Found",
            description=f"No Lockout Bot found to start register, please first invite lockout bot and register"
                        f"it using p!registerLockoutBot @bot",
            color=discord.Color.gold()
        )
        embed.set_author(name=botName)
        await text_channel.send(embed=embed)
        return


    if thisServer["tourney_name"] == "--":
        participantsList.insert_one({"server": ctx.guild.id, "contestants": []})
        servers.update_one({"_id": ctx.guild.id}, {"$set": {"tourney_name": tourneyName}})
        embed = discord.Embed(
            title="Tournament Started",
            description=f"Please ask participants to register themselves with **p!registerMe seed** where seed is the "
                        f"parameter on which you want to order people",
            color=discord.Color.gold()
        )
        embed.set_author(name=botName)
        await text_channel.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Please first close the running tournament",
            description=f"A tournament **{thisServer['tourney_name']}** is already running on this server, please stop it first to start a new one."
                        f"\nStop using p!stopTourney",
            color=discord.Color.gold()
        )
        embed.set_author(name=botName)
        await text_channel.send(embed=embed)


@client.command()
@commands. has_role('Tourney Manager')
async def stopTourney(ctx):
    thisServer = servers.find_one({"_id": ctx.guild.id})
    text_channel_n = thisServer["text_channel"]
    global text_channel
    for x in ctx.guild.text_channels:
        if x.id == text_channel_n:
            text_channel = x

    if thisServer["tourney_name"] == "--":
        embed = discord.Embed(
            title="No Tourney running",
            description="No tourney is currently running on this server.",
            color=discord.Color.gold()
        )
        await text_channel.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Tourney stopped:(",
            description=f"The tourney **{thisServer['tourney_name']}** has been stopped.",
            color=discord.Color.red()
        )
        embed.set_author(name=botName)
        servers.update_one({"_id": ctx.guild.id}, {"$set": {"tourney_name": "--"}})
        participantsList.delete_one({"server": ctx.guild.id})
        matchesList.delete_one({"server": ctx.guild.id})
        newMatchesList.delete_one({"server": ctx.guild.id})
        detailToNode.delete_one({"server": ctx.guild.id})
        await text_channel.send(embed=embed)


@client.command()
@commands. has_role('Tourney Manager')
async def startTourney(ctx):
    thisServer = servers.find_one({"_id": ctx.guild.id})
    text_channel_n = thisServer["text_channel"]
    global text_channel
    for x in ctx.guild.text_channels:
        if x.id == text_channel_n:
            text_channel = x

    checkForStartTourney = matchesList.find_one({"server": ctx.guild.id})

    if checkForStartTourney is not None:
        embed = discord.Embed(
            title="Tournament Already Started",
            description="Tounament has already started so nothing can be changed.",
            color=discord.Color.gold()
        )
        embed.set_author(name=botName)
        await text_channel.send(embed=embed)
        return


    if thisServer["tourney_name"] == "--":
        embed = discord.Embed(
            title = "No Tourney registered",
            description = "No tourney is currently started for registration on this server. ",
            color = discord.Color.gold()
        )
        await text_channel.send(embed = embed)
    elif len(participantsList.find_one({"server": ctx.guild.id})["contestants"]) == 0:
        embed = discord.Embed(
            title = "No registrations",
            description = "No participants registered, cannot start the Tourney. Participants can register using p!registerMe",
            color = discord.Color.gold()
        )
        await text_channel.send(embed = embed)
    elif len(participantsList.find_one({"server": ctx.guild.id})["contestants"]) == 1:
        embed = discord.Embed(
            title = "Single registrant",
            description = "Cannot start a tourney with a single participant.",
            color = discord.Color.gold()
        )
        await text_channel.send(embed = embed)
    else:
        detailToNode.insert_one({"server": ctx.guild.id, "value": {}})
        matchesList.insert_one({"server": ctx.guild.id, "value": []})
        newMatchesList.insert_one({"server": ctx.guild.id, "value": []})

        to_match_builder(ctx)
        Match_Builder.func(participantsList.find_one({"server": ctx.guild.id})["contestants"])
        from_match_builder(ctx)

        embed = discord.Embed(
            title = f"Tourney started :D",
            description = f"The tourney {thisServer['tourney_name']} has been started.",
            color = discord.Color.gold()
        )
        await text_channel.send(embed = embed)

        matches_description = '\n'.join([f"<@{ele[0]['id']}> vs <@{ele[1]['id']}>" for ele in Match_Builder.matchlist])
        embed = discord.Embed(
            title = "Matches for Round 1",
            description = matches_description,
            color = discord.Color.gold()
        )
        await text_channel.send(embed = embed)


@client.command()
@commands. has_role('Tourney Manager')
async def registerLockoutBot(ctx, mention: str):
    thisServer = servers.find_one({"_id": ctx.guild.id})
    text_channel_n = thisServer["text_channel"]
    global text_channel
    for x in ctx.guild.text_channels:
        if x.id == text_channel_n:
            text_channel = x

    id = mention[2:-1]
    if (id.isnumeric() and ctx.guild.get_member(int(id)) != None):
        embed = discord.Embed(
            title="Lockout Bot Registered",
            description=f"{mention} registered successfully as Lockout Bot.",
            color=discord.Color.gold()
        )
        servers.update_one({"_id": ctx.guild.id}, {"$set": {"lockout_bot": int(id)}})
        await text_channel.send(embed=embed)
    else:
        embed = discord.Embed(
            title="Not a valid mention",
            description="Please enter a valid discord mention to set the Lockout Bot for the server.",
            color=discord.Color.gold()
        )
        embed.set_author(name=botName)
        await text_channel.send(embed=embed)


@client.command()
async def registerMe(ctx, seed: int):
    thisServer = servers.find_one({"_id": ctx.guild.id})
    text_channel_n = thisServer["text_channel"]
    global text_channel
    for x in ctx.guild.text_channels:
        if x.id == text_channel_n:
            text_channel = x

    checkForStartTourney=matchesList.find_one({"server":ctx.guild.id})

    if checkForStartTourney is not None:
        embed = discord.Embed(
            title="Tournament Already Started",
            description="Tounament has already started so nothing can be changed.",
            color=discord.Color.gold()
        )
        embed.set_author(name=botName)
        await text_channel.send(embed=embed)
        return


    if thisServer["tourney_name"] == "--":
        embed = discord.Embed(
            title="No Tourney",
            description=f"{ctx.author.mention} there is no ongoing tournament",
            color=discord.Color.gold()
        )
        embed.set_author(name=botName)
        await text_channel.send(embed=embed)
        return

    participantsListTemp = participantsList.find_one({"server": ctx.guild.id})

    # print(participantsListTemp)

    for x in participantsListTemp["contestants"]:
        # print(x)
        if x['id'] == ctx.author.id:
            embed = discord.Embed(
                title="Already Registered",
                description=f"{ctx.author.mention} you are already registered, please wait till tournament"
                            f" is started. If trying to change your"
                            f"seed then first unregister yourself then again register.",
                color=discord.Color.gold()
            )
            embed.set_author(name=botName)
            await text_channel.send(embed=embed)
            return

    participantsList.update_one({"server": ctx.guild.id},
                                {"$push": {"contestants": {"id": ctx.author.id, "seed": seed}}})

    embed = discord.Embed(
        title="You are Registered",
        description=f"{ctx.author.mention} you are now registered for the tournament.",
        color=discord.Color.gold()
    )
    embed.set_author(name=botName)
    await text_channel.send(embed=embed)


@client.command()
async def unregisterMe(ctx):
    thisServer = servers.find_one({"_id": ctx.guild.id})
    text_channel_n = thisServer["text_channel"]
    global text_channel
    for x in ctx.guild.text_channels:
        if x.id == text_channel_n:
            text_channel = x

    checkForStartTourney = matchesList.find_one({"server": ctx.guild.id})

    if checkForStartTourney is not None:
        embed = discord.Embed(
            title="Tournament Already Started",
            description="Tounament has already started so nothing can be changed.",
            color=discord.Color.gold()
        )
        embed.set_author(name=botName)
        await text_channel.send(embed=embed)
        return

    if thisServer["tourney_name"] == "--":
        embed = discord.Embed(
            title="No Tourney",
            description=f"{ctx.author.mention} there is no ongoing tournament.",
            color=discord.Color.gold()
        )
        embed.set_author(name=botName)
        await text_channel.send(embed=embed)
        return

    participantsListTemp = participantsList.find_one({"server": ctx.guild.id})

    # print(participantsListTemp["contestants"])

    found = False
    ix = 0
    for i in range(len(participantsListTemp["contestants"])):
        if participantsListTemp["contestants"][i]["id"] == ctx.author.id:
            found = True
            ix = i

    if found:
        participantsList.delete_one({"server": ctx.guild.id})
        participantsList.insert_one({"server": ctx.guild.id,
                                     "contestants": participantsListTemp["contestants"][:ix] + participantsListTemp[
                                                                                                   "contestants"][
                                                                                               ix + 1:]})
        embed = discord.Embed(
            title="Unregistered",
            description=f"{ctx.author.mention} you are now unregistered.",
            color=discord.Color.gold()
        )
        embed.set_author(name=botName)
        await text_channel.send(embed=embed)
        return

    embed = discord.Embed(
        title="Couldn't Unregister",
        description=f"{ctx.author.mention} you are not part of any tournament right now.",
        color=discord.Color.gold()
    )
    embed.set_author(name=botName)
    await text_channel.send(embed=embed)

client.run(token)