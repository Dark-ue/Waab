import discord
from discord.ext import commands

ALLOWED_USERS = [900017760397058098, 772470344967651378]  # TODO: SECURE THE CODE

def global_(bot):
    @bot.command()
    async def broadcast(ctx, *, message: str):
        if ctx.author.id not in ALLOWED_USERS:
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