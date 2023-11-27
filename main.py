# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 09:16:17 2023

@author: maris
"""

import os

import discord
from dotenv import load_dotenv
from discord import app_commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
tree = app_commands.CommandTree(client)

client = discord.Client()

@tree.command(name = "tester", description = "My first application Command", guild=discord.Object(id=GUILD)) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def first_command(interaction):
    await interaction.response.send_message("Hello!")


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=Your guild id))
    print("Ready!")

client.run(TOKEN)
