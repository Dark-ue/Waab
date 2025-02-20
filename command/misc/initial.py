import discord
from discord.ext import commands

def initial(bot):
    @bot.event
    async def on_ready():
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="Listening to $help"))

    async def on_guild_join(guild):
        general = next((channel for channel in guild.text_channels if channel.permissions_for(guild.me).send_messages), None)
        if general:
            await general.send("Hello World! I am Waab!")
