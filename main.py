import os
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv
from command.misc import ping, initial, misc
from command.moderation import warn, mod_event, roles
from command.admin_panel import global_


# Set up logging
logging.basicConfig(level=logging.INFO)

# Load the token from the .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
if TOKEN is None:
    raise ValueError("Create a .env file dumbass")

# Initialize the bot
intents = discord.Intents.all()
intents.message_content = True #NOQA (Do not touch, i will return an error otherwise
bot = commands.Bot(command_prefix='$', intents=intents)

# Load the commands
ping.ping(bot)
warn.warn(bot)
mod_event.mod_event(bot)
roles.roles(bot)
initial.initial(bot)
global_.global_(bot)
misc.misc(bot)

# this shit handles errors
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
                embed = discord.Embed(
                     title = "Error",
                     description = f"An unexpected error occured: {error}",
                     color = discord.Color.red()
                       )
                bot_message = await ctx.send(embed=embed)
    
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
                title="Permission Error",
                description="You are missing Manage Messages permission(s) to run this command.",
                color=discord.Color.red()
            )
        bot_message = await ctx.send(embed=embed)


        await ctx.message.delete(delay=2)
        await bot_message.delete(delay=2)
    else:
        embed = discord.Embed( #make sure to use correct capitalisation, my dumbahh troubleshooted this for 1 hour
            title = "Error",
            description = f"An unexpected error occured: {error}",
            color = discord.Color.red()
        )
        bot_message = await ctx.send(embed=embed)

# Run the bot
try:
    bot.run(TOKEN)
except Exception as e:
    logging.error(f"Failed to run the bot: {e}")

