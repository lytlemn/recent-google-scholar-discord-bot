# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 09:16:17 2023

@author: maris
"""

import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD TOKEN')

client = discord.Client()

@client.event
async def on ready():
    print(f'{client.user} has connected to Discord!')

client.run(TOKEN)
