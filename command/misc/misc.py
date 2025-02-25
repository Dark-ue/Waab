import discord
from discord.ext import commands

def misc(bot):
    @bot.command()
    async def avatar(ctx, member: discord.Member = None):
        if member is None:
            embed = discord.Embed(
                title="Avatar Command",
                description="Please specify a user to get the avatar. Usage: `$avatar @user`",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title=f"{member.name}'s Avatar",
                color=discord.Color.blue()
            )
            embed.set_image(url=member.avatar.url)
            await ctx.send(embed=embed)

