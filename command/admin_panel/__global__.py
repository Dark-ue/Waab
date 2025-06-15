import discord
from dotenv import load_dotenv
import os
from discord.ext import commands

load_dotenv()
ALLOWED_USERS = os.getenv('ALLOWED_USERS') 

class Global(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def broadcast(self, ctx, *, message: str):
        if str(ctx.author.id) not in ALLOWED_USERS:
            await ctx.send("Command not found.") #this creates an illusion for the user that the command does not exist
            return

        for guild in self.bot.guilds:
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

    @commands.command()
    async def leave_guild(self, ctx, guild_id: int):
        if str(ctx.author.id) not in ALLOWED_USERS:
            await ctx.send("Command not found.")
            return
        else:
            guild = self.bot.get_guild(guild_id)
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


async def setup(bot):
    await bot.add_cog(Global(bot))
   