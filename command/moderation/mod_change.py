import discord
from discord.ext import commands

class Mod_Change(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def nickname(self, ctx, member: discord.Member, *, nickname):
        await member.edit(nick=nickname)
        embed = discord.Embed(
            title="Nickname Changed",
            description=f"Changed {member.mention}'s nickname to {nickname}.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Mod_Change(bot))

