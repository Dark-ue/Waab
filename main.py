#import modules
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import random 
import command_

#load the token from the .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
print(TOKEN)

#initialize the bot
intents = discord.Intents.all()
intents.message_content = True #NOQA
bot = commands.Bot(command_prefix='$', intents=intents)

#load the command
command_.setup(bot)



bot.run(TOKEN)