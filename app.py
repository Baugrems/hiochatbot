import random
from discord import Game
from discord.ext.commands import Bot
import requests
import asyncio
import os
from discord import Channel
from discord import Role
from discord import Server
import discord
import boto
from tatsumaki.wrapper import ApiWrapper
import time


BOT_PREFIX = "."

TOKEN = (os.environ['TOKEN'])

client = Bot(command_prefix=BOT_PREFIX)

@client.command(name="TatLeaders",
                description="Grab tatsumaki rank leaders when used.",
                brief="Tatsumanki Rank Leaderboard",
                aliases=["tleaders", "tatleaders"],
                pass_context=True)
async def checkTatRank(context):
    msg = "Give Dobby a moment to grab list..."
    await client.send_message(context.message.channel, msg)
    await client.send_typing(context.message.channel)
    wrapper = ApiWrapper("b9ff5b5da7b223a3251cd98a68329b18-10d056d2a47b9-75b8b43ff968bb3cea8fdfb4821815d9")
    response = await wrapper.leaderboard(context.message.server.id, 10)
    msg = "```"
    for user in response:
        if context.message.server.get_member(user["user_id"]):
            msg += "\nRank " + str(user["rank"]) + ": " + context.message.server.get_member(user["user_id"]).nick + " with " + user["score"] + " points."
        else:
            msg += "\nRank " + str(user["rank"]) + ": Unknown User with " + user["score"] + " points."
    time.sleep(2)
    response = await wrapper.leaderboard(context.message.server.id, 20)
    for user in response:
        if context.message.server.get_member(user["user_id"]):
            msg += "\nRank " + str(user["rank"]) + ": " + context.message.server.get_member(user["user_id"]).nick + " with " + user["score"] + " points."
        else:
            msg += "\nRank " + str(user["rank"]) + ": Unknown User with " + user["score"] + " points."
    msg += "```"
    await client.send_message(context.message.channel, msg)

# DOBBY COMMANDS
# If no command given, sends random Dobby GIF
# Dobby help to get list of dobby commands
@client.group(pass_context=True)
async def dobby(ctx):
    if ctx.invoked_subcommand is None:
    	availablegifs = [
    		"images/dobbydie.gif",
    		"images/dobbyfree.gif",
    		"images/dobbyheadhit.gif",
    		"images/dobbyhitself.gif",
    		"images/dobbymagic.gif",
    		"images/dobbysmug.gif",
    		"images/dobbytwitch.gif"
    	]
    	await client.send_file(ctx.message.channel, random.choice(availablegifs))

@dobby.command(name='Random Spell',
                description="Provides a random Harry Potter Spell.",
                brief="Spellbook.",
                aliases=['spells', 'spellbook', 'charm', 'curse', "spell"],
                pass_context=True)
async def spell(context):
    url = "https://www.potterapi.com/v1/spells?key=$2a$10$g9SDctxKs5Gs81icb7fFTu9W2Yxb9va6Q1Ir9KQITekxFwm5vRHPq"
    response = requests.get(url)
    value = random.choice(response.json())
    msg = "A good " + value["type"].lower() + " might be " + value["spell"] + ". It " + value["effect"] + "."
    await client.send_message(context.message.channel, msg)

@dobby.command(name="Cat Facts",
               description="Provides a random cat fact.",
               brief="Cat Facts",
               aliases=["cf", "catfact", "catfacts"],
               pass_context=True)
async def catfacts(context):
    url = "https://cat-fact.herokuapp.com/facts/random?animal=cat&amount=1"
    response = requests.get(url)
    value = response.json()
    msg = value["text"]
    await client.send_message(context.message.channel, msg)

@dobby.command(name="Dog Photo",
                description="Random Doggo",
                brief="random dooooogggooo",
                aliases=["dog", "dp","doggo","pupper"],
                pass_context=True)
async def dogphoto(context):
    url = "https://dog.ceo/api/breeds/image/random"
    response = requests.get(url)
    value = response()
    msg = value["message"]
    await client.send_message(context.message.channel, msg)

@dobby.command(name='sorting',
                description="Picks a random house to display.",
                brief="Choose a random house.",
                aliases=['sort', 'bestHouse'],
                pass_context=True)
async def bestHouse(context):
    url = "https://www.potterapi.com/v1/sortinghat"
    response = requests.get(url)
    value = response.json()
    msg = "" + value + " is best Dobby thinks."
    await client.send_message(context.message.channel, msg)

@dobby.command(name="Dobby Timer",
               description="Set a timer with Dobby",
               brief="Set a timer",
               aliases=["timer"],
               pass_context=True)
async def dobbyTimer(context, time, text):
    msg = "Dobby will alert you in {0} second(s) when time up.".format(time)
    await client.send_message(context.message.channel, msg)
    await asyncio.sleep(float(time))
    msg = "{0.message.author.mention} time up for {1}".format(context, text)
    await client.send_message(context.message.channel, msg)

@dobby.command(name="Dobby Help",
			   description="Gives a list of available commands.",
			   brief="Dobby Help.",
			   aliases=['help', 'halp'],
			   pass_context=True)
async def dobbyhelp(context):
	msg = '''```Dobby Commands:
		.dobby spell            - Provides a random Harry Potter Spell.
		.dobby sort             - Picks a random house to display.
		.dobby character "name" - Finds a character by that name from HP.
        .dobby d20              - Rolls a visual 20 sided die.
        .dobby timer x mention  - Sets a timer for x seconds and @mentions.

Other Commands:
        .tleaders               - Shows named list of Tatsumaki High Score.

		Contact Sebastián Cazarez <@Baugrems1234> for Technical Support.```'''
	await client.send_message(context.message.channel, msg)

@dobby.command(name="D20 Roller",
               description="Roll a D20 and get an image back with results.",
               brief="Roll a D20.",
               aliases=["d20", "D20", "roll20"],
               pass_context=True)
async def roll20(context):
    img = "images/D20_" + str(random.randint(1,20)) + ".png"
    await client.send_file(context.message.channel, img)

#TODO: Find a better way to do this...
@dobby.command(name="Character finder",
			   description="Finds Harry Potter Characters by name",
			   brief="Finds characters",
			   aliases=["character", "find", "search"],
			   pass_context=True)
async def character(context, findName = None):
    if findName is None:
        url = 'https://www.potterapi.com/v1/characters?key=$2a$10$g9SDctxKs5Gs81icb7fFTu9W2Yxb9va6Q1Ir9KQITekxFwm5vRHPq'
        response = requests.get(url)
        value = random.choice(response.json())
    else:
        payload = {'name': findName, 'key': '$2a$10$g9SDctxKs5Gs81icb7fFTu9W2Yxb9va6Q1Ir9KQITekxFwm5vRHPq'}
        response = requests.get('https://www.potterapi.com/v1/characters', params=payload)
        value = response.json()
        value = value[0]
    if not value:
        msg = "Dobby cannot find that character... Dobby deserves punishment!!!"
        await client.send_message(context.message.channel, msg)
        await client.send_file(context.message.channel, "images/dobbyhitself.gif")
    else:
        msg = value["name"] + " "
        if value.get('role', False):
            msg += ":: " + value["role"] + " "
        if value.get("school", False):
            msg = msg + ":: " + value["school"] + " "
        if value.get('house', False):
            msg = msg + ":: " + value["house"] + " house "
        if value.get("deathEater", False):
            msg = msg + ":: Death Eater "
        if value.get("dumbledoresArmy", False):
            msg = msg + ":: Member of Dumbledores Army "
        if value.get("orderOfThePhoenix", False):
            msg = msg + ":: Member of the Order of the Phoenix "
        if value.get("ministryOfMagic", False):
            msg = msg + ":: Member of the Ministry of Magic "
        if value.get("species", False):
            msg += "::Species - " + value["species"] + " "
        if value.get("bloodStatus", False):
            msg += ":: Blood-Status - " + value["bloodStatus"]
        print(response.url)
        await client.send_message(context.message.channel, msg)

# @dobby.command(name='trivia',
#                 description="Begins Harry Potter Trivia",
#                 brief="HP Trivia.",
#                 aliases=['HP-Trivia, trivia'],
#                 pass_context=True)
# async def trivia(context):
# 	msg = "Time for Harry Potter Trivia. Dobby loves Trivia..."
# 	await client.send_message(context.message.channel, msg)
# 	value = random.choice(possible_questions)
# 	await client.send_message(context.message.channel, msg)



#These trigger on any message. Not just commands.
@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    # We also want to make sure it checks for commands first
    await client.process_commands(message)
    if message.author == client.user:
    	return
    mcont = message.content.lower()
    if mcont.startswith('hi dobby'):
        msg = 'Hello {0.author.mention}. Type ".dobby help" if want help on Dobby!'.format(message)
        await client.send_message(message.channel, msg)

    if mcont.startswith('validate me please'):
    	if message.channel == client.get_channel('450870668435914752'):
    		msg = 'Hello @everyone! {0.author.mention} needs to be checked in!'.format(message)
    		await client.send_message(client.get_channel('450870668435914752'), msg)
    	else:
        	msg = "You seem to be validated already, {0.author.mention}!".format(message)
        	await client.send_message(message.channel, msg)

    if mcont.startswith('.clear'):
    #Clears channel history, but only if someone does it inside the arrival room
    	if message.channel.id == '450870668435914752':
    		tmp = await client.send_message(message.channel, 'Clearing messages...')
    		async for msg in client.logs_from(message.channel):
    			await client.delete_message(msg)

#PotterAPI KEY $2a$10$g9SDctxKs5Gs81icb7fFTu9W2Yxb9va6Q1Ir9KQITekxFwm5vRHPq/
    if mcont.startswith('dobby give me a spell'):
    	url = "https://www.potterapi.com/v1/spells?key=$2a$10$g9SDctxKs5Gs81icb7fFTu9W2Yxb9va6Q1Ir9KQITekxFwm5vRHPq"
    	response = requests.get(url)
    	value = random.choice(response.json())
    	msg = "A good " + value["type"].lower() + " might be " + value["spell"] + ". It " + value["effect"] + "."
    	await client.send_message(message.channel, msg)

    if mcont.startswith('dobby what house is best?'):
    	url = "https://www.potterapi.com/v1/sortinghat"
    	response = requests.get(url)
    	value = response.json()
    	msg = "" + value + " is best Dobby thinks."
    	await client.send_message(message.channel, msg)

    if mcont.startswith('dobby hug'):
        await client.send_file(message.channel, "images/pepehug.png")

    # if message.content.lower().startswith('dobby tell me about someone'):
    # 	url = 'https://www.potterapi.com/v1/characters?key=$2a$10$g9SDctxKs5Gs81icb7fFTu9W2Yxb9va6Q1Ir9KQITekxFwm5vRHPq'
    # 	response = requests.get(url)
    # 	value = random.choice(response.json())
    # 	msg = "How about " + value["name"] + " a " + value["role"] + " from " + value["school"] + ". " + value["name"] + " is also a " + value["species"] + " " + value["bloodStatus"]
    # 	await client.send_message(message.channel, msg)

#More Random Stuff
    if 'dobby a sock' in mcont:
    	await client.send_file(message.channel, "images/dobbysock.gif")
    elif 'sock' in mcont:
    	msg = "Did someone say Sock?"
    	await client.send_message(message.channel, msg)
    if 'leviosa' in mcont:
        await client.send_file(message.channel, "images/leviosa.jpg")
    if 'pokemon' in mcont:
        await client.send_file(message.channel, "images/pokemon.jpeg")
    if 'kaelena' in mcont:
        await client.send_file(message.channel, "images/cruiseship.gif")
    if 'milex' in mcont:
        await client.send_file(message.channel, "images/cruiseship.gif")




@client.event
async def on_member_join(member):
	msg = 'Welcome, {0.mention}! Please set your discord name to match your Hogwarts.io name. '.format(member)
	await client.send_message(client.get_channel('450870668435914752'), msg)
	msg = 'Also be sure to post your discord name and # number at https://www.hogwarts.io/viewtopic.php?f=44&t=2233'
	await client.send_message(client.get_channel('450870668435914752'), msg)
	msg = 'Say "Validate me please" when you are done with both tasks.'
	await client.send_message(client.get_channel('450870668435914752'), msg)

# 450870668435914752 Arrival channel ID




@client.event
async def on_ready():
	await client.change_presence(game=Game(name="with a sock"))
	print("Logged in as " + client.user.name)
	for server in client.servers:
		for channel in server.channels:
			print(channel.id + " " + channel.name)
		print(Server.roles)
		for server in client.servers:
			for role in server.roles:
				print(role.id + " " + role.name)

client.run(TOKEN)