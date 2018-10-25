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

BOT_PREFIX = ("Dobby ", "dobby")
TOKEN = os.environ['TOKEN']

client = Bot(command_prefix=BOT_PREFIX)

@client.command(name='8ball',
                description="Answers a yes/no question.",
                brief="Answers from the beyond.",
                aliases=['eight_ball', 'eightball', '8-ball'],
                pass_context=True)
async def eight_ball(context):
    possible_responses = [
        'That is a resounding no',
        'It is not looking likely',
        'Too hard to tell',
        'It is quite possible',
        'Definitely',
    ]
    await client.say(random.choice(possible_responses) + ", " + context.message.author.mention)

@client.command(name='spell',
                description="Provides a random Harry Potter Spell.",
                brief="Spellbook.",
                aliases=['spells', 'spellbook', 'charm', 'curse'],
                pass_context=True)
async def spell(context):
    url = "https://www.potterapi.com/v1/spells?key=$2a$10$g9SDctxKs5Gs81icb7fFTu9W2Yxb9va6Q1Ir9KQITekxFwm5vRHPq"
    response = requests.get(url)
    value = random.choice(response.json())
    msg = "A good " + value["type"].lower() + " might be... " + value["spell"] + ". It " + value["effect"] + "."
    await client.send_message(context.message.channel, msg)


@client.command(name='sorting',
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


@client.command(name='trivia',
                description="Begins Harry Potter Trivia",
                brief="HP Trivia.",
                aliases=['HP-Trivia'],
                pass_context=True)
async def trivia(context):
	msg = "Time for Harry Potter Trivia. Dobby loves Trivia..."
	await client.send_message(context.message.channel, msg)
	triviaStart()


async def trivaStart():


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    await client.process_commands(message)
    if message.author == client.user:
    	return

    if message.content.lower().startswith('dobby help list'):
    	msg = 'Dobby is a good house elf. Dobby likes to be helpful!'.format(message)
    	await client.send_message(message.channel, msg)
    	msg = "Dobby can give spell suggestions. Ask 'Dobby give me a spell' and Dobby give you a spell!"
    	await client.send_message(message.channel, msg)
    	msg = "Dobby can try to name famous characters? Just ask 'Dobby tell me about someone' and Dobby do it! Sometimes..."
    	await client.send_message(message.channel, msg)

    if message.content.lower().startswith('hi dobby'):
        msg = 'Hello {0.author.mention}. Ask Dobby for the "Dobby help list" if you want info on Dobby.'.format(message)
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
    if message.content.lower().startswith('_gives dobby a sock_'):
    	msg = 'THANK YOU, {0.author.mention}! DOBBY IS FREE ELF!'.format(message)
    	await client.send_message(message.channel, msg)


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