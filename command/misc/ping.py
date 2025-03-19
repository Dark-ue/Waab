
from discord.ext import commands

def ping(bot):
    @bot.command(name="ping", help="Check the bot's latency.")
    async def ping(ctx):
        await ctx.send(f'Pong! Latency: `{int(bot.latency * 1000)} ms`')