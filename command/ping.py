import discord
from discord.ext import commands

def ping(bot):
    @bot.command()
    async def ping(ctx):
        await ctx.send(f'Pong! Latency: `{int(bot.latency * 1000)} ms`')

#list of commands
#ping