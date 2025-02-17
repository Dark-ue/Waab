import discord
from discord.ext import commands
import time

def ping(bot):
    @bot.command()
    async def ping(ctx):
        start_time = time.time()
        message = await ctx.send('Pinging...')
        end_time = time.time()
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        await message.edit(content=f'Pong! Response time: `{response_time:.2f} ms`')

#list of commands
#ping