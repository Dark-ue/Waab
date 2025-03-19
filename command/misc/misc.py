import discord
from discord.ext import commands

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot  

    @commands.command()
    async def avatar(self, ctx, member: discord.Member = None):
        if member is None:
            embed = discord.Embed(
                title="Avatar Command",
                description="Please specify a user to get the avatar. Usage: `$avatar @user`",
                color=discord.Color.red()
            )
        else:
            embed = discord.Embed(
                title=f"{member.name}'s Avatar",
                color=discord.Color.blue()
            )
            embed.set_image(url=member.avatar.url)

        await ctx.send(embed=embed)

    @commands.command()
    async def uptime(self, ctx):
        embed = discord.Embed(
            title="Uptime Command",
            description=f"I have been online for {int(self.bot.uptime)} seconds.",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        embed = discord.Embed(
            title="Ping Command",
            description=f"Pong! `{int(self.bot.latency * 1000)}ms`",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Misc(bot))
