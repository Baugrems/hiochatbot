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

BOT_PREFIX = "."

TOKEN = (os.environ['TOKEN'])

client = Bot(command_prefix=BOT_PREFIX)

# @client.command(name='8ball',
#                 description="Answers a yes/no question.",
#                 brief="Answers from the beyond.",
#                 aliases=['eight_ball', 'eightball', '8-ball'],
#                 pass_context=True)
# async def eight_ball(context):
#     possible_responses = [
#         'That is a resounding no',
#         'It is not looking likely',
#         'Too hard to tell',
#         'It is quite possible',
#         'Definitely',
#     ]
#     await client.say(random.choice(possible_responses) + ", " + context.message.author.mention)

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

		Contact Sebastián Cazarez <@Baugrems1234> for Technical Support.```'''
	await client.send_message(context.message.channel, msg)

@dobby.command(name="D20 Roller",
               description="Roll a D20 and get an image back with results.",
               brief="Roll a D20.",
               aliases=["d20", "D20", "roll20"],
               pass_context=True)
async def roll20(context):
    # switcher = {
    #     1: "images/D20_1.png",
    #     2: "images/D20_2.png",
    #     3: "images/D20_3.png",
    #     4: "images/D20_4.png",
    #     5: "images/D20_5.png",
    #     6: "images/D20_6.png",
    #     7: "images/D20_7.png",
    #     8: "images/D20_8.png",
    #     9: "images/D20_9.png",
    #     10: "images/D20_10.png",
    #     11: "images/D20_11.png",
    #     12: "images/D20_12.png",
    #     13: "images/D20_13.png",
    #     14: "images/D20_14.png",
    #     15: "images/D20_15.png",
    #     16: "images/D20_16.png",
    #     17: "images/D20_17.png",
    #     18: "images/D20_18.png",
    #     19: "images/D20_19.png",
    #     20: "images/D20_20.png"
    # }
    # img = switcher.get(random.randint(1,20), False)
    img = "images/D20_" + str(random.randint(1,20)) + ".png"
    await client.send_file(context.message.channel, img)


@dobby.command(name="Character finder",
			   description="Finds Harry Potter Characters by name",
			   brief="Finds characters",
			   aliases=["character", "find", "search"],
			   pass_context=True)
async def character(context, findName):
	payload = {'name': findName, 'key': '$2a$10$g9SDctxKs5Gs81icb7fFTu9W2Yxb9va6Q1Ir9KQITekxFwm5vRHPq'}
	response = requests.get('https://www.potterapi.com/v1/characters', params=payload)
	# url = 'https://www.potterapi.com/v1/characters?key=$2a$10$g9SDctxKs5Gs81icb7fFTu9W2Yxb9va6Q1Ir9KQITekxFwm5vRHPq'
	# response = requests.get(url)
	value = response.json()
	if not value:
		msg = "Dobby cannot find that character... Dobby deserves punishment!!!"
		await client.send_message(context.message.channel, msg)
		await client.send_file(context.message.channel, "images/dobbyhitself.gif")
	else:
		value = value[0]
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
	# msg = "" + value["name"] + " is a " + value["role"] + " from " + value["school"] + ". " + value["name"] + " is also a " + value["species"] + " " + value["bloodStatus"]
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


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    await client.process_commands(message)
    if message.author == client.user:
    	return

    if message.content.lower().startswith('hi dobby'):
        msg = 'Hello {0.author.mention}. Type ".dobby help" if want help on Dobby!'.format(message)
        await client.send_message(message.channel, msg)

    if message.content.lower().startswith('validate me please'):
    	if message.channel == client.get_channel('450870668435914752'):
    		msg = 'Hello @everyone! {0.author.mention} needs to be checked in!'.format(message)
    		await client.send_message(client.get_channel('450870668435914752'), msg)
    	else:
        	msg = "You seem to be validated already, {0.author.mention}!".format(message)
        	await client.send_message(message.channel, msg)

    if message.content.lower().startswith('.clear'):
    #Clears channel history, but only if professor does command inside the arrival room
    	if message.channel.id == '450870668435914752':
    		tmp = await client.send_message(message.channel, 'Clearing messages...')
    		async for msg in client.logs_from(message.channel):
    			await client.delete_message(msg)

#PotterAPI KEY $2a$10$g9SDctxKs5Gs81icb7fFTu9W2Yxb9va6Q1Ir9KQITekxFwm5vRHPq/
    if message.content.lower().startswith('dobby give me a spell'):
    	url = "https://www.potterapi.com/v1/spells?key=$2a$10$g9SDctxKs5Gs81icb7fFTu9W2Yxb9va6Q1Ir9KQITekxFwm5vRHPq"
    	response = requests.get(url)
    	value = random.choice(response.json())
    	msg = "A good " + value["type"].lower() + " might be " + value["spell"] + ". It " + value["effect"] + "."
    	await client.send_message(message.channel, msg)

    if message.content.lower().startswith('dobby what house is best?'):
    	url = "https://www.potterapi.com/v1/sortinghat"
    	response = requests.get(url)
    	value = response.json()
    	msg = "" + value + " is best Dobby thinks."
    	await client.send_message(message.channel, msg)

    # if message.content.lower().startswith('dobby tell me about someone'):
    # 	url = 'https://www.potterapi.com/v1/characters?key=$2a$10$g9SDctxKs5Gs81icb7fFTu9W2Yxb9va6Q1Ir9KQITekxFwm5vRHPq'
    # 	response = requests.get(url)
    # 	value = random.choice(response.json())
    # 	msg = "How about " + value["name"] + " a " + value["role"] + " from " + value["school"] + ". " + value["name"] + " is also a " + value["species"] + " " + value["bloodStatus"]
    # 	await client.send_message(message.channel, msg)

#More Random Stuff
    if 'dobby a sock' in message.content.lower():
    	await client.send_file(message.channel, "images/dobbysock.gif")
    elif 'sock' in message.content.lower():
    	msg = "Did someone say Sock?"
    	await client.send_message(message.channel, msg)
    if 'leviosa' in message.content.lower():
        await client.send_file(message.channel, "images/leviosa.jpg")
    if 'pokemon' in message.content.lower():
        await client.send_file(message.channel, "images/pokemon.jpeg")



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