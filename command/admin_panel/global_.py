import discord
from discord.ext import commands

ALLOWED_USERS = [900017760397058098, 772470344967651378]  # Add the user IDs of the users who are allowed to use this command

def global_(bot):
    @bot.command()
    async def broadcast(ctx, *, message: str):
        if ctx.author.id not in ALLOWED_USERS:
            await ctx.send("Command not found.")
            return

        for guild in bot.guilds:
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).send_messages:
                    await channel.send(message)
                    break  # Send the message to the first channel where the bot has permission

        embed = discord.Embed(
            title="Broadcast",
            description="Message sent to all servers.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)