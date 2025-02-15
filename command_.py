import discord
from discord.ext import commands
from dotenv import load_dotenv


def setup(bot):
    @bot.command()
    async def hello(ctx):
        await ctx.send('Hello! How can I assist you today?')

