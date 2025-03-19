import discord
from dotenv import load_dotenv
import os
from discord.ext import commands

load_dotenv()
ALLOWED_USERS = os.getenv('ALLOWED_USERS') 

def __global__(bot):
    @bot.command()
    async def broadcast(ctx, *, message: str):
        if str(ctx.author.id) not in ALLOWED_USERS:
            await ctx.send("Command not found.") #this creates an illusion for the user that the command does not exist
            return

        for guild in bot.guilds:
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).send_messages:
                    await channel.send(message)
                    break  # removing this will send messages in ALL the channels

        embed = discord.Embed(
            title="Broadcast",
            description="Message sent to all servers.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @bot.command()
    async def leave_guild(ctx, guild_id: int):
        if str(ctx.author.id) not in ALLOWED_USERS:
            await ctx.send("Command not found.")
            return
        else:
            guild = bot.get_guild(guild_id)
            if guild is None:
                embed = discord.Embed(
                    title="Leave Guild",
                    description="Guild not found.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
            else:
                await guild.leave()
                embed = discord.Embed(
                    title="Leave Guild",
                    description="Left the guild.",
                    color=discord.Color.green()
                )
                await ctx.send(embed=embed)