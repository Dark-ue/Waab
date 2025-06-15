import discord
from discord.ext import commands, tasks
import os
from command.moderation.database import Database

# Initialize the database connection
db_path = os.path.join(os.path.dirname(__file__), 'warnings.db')
db = Database(db_path)

class WarnCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cleanup_warnings.start()  # Start the cleanup task when the cog is loaded

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member = None, *, reason=None):
        if member is None:
            embed = discord.Embed(
                title="Warning Command",
                description="Please specify a user to warn. Usage: `$warn @user [reason]`",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        else:
            await self.issue_warning(ctx, member, reason)

    @commands.command()
    async def warn_count(self, ctx, member: discord.Member = None):
        if member is None:
            embed = discord.Embed(
                title="Warning Count Command",
                description="Please specify a user to check warnings. Usage: `$warn_count @user`",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        else:
            count = db.get_warnings(member.id)
            embed = discord.Embed(
                title="Warning Count",
                description=f'User {member.mention} has {count} warning(s).',
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def set_warn_period(self, ctx, days: int = None):
        if days is None:
            embed = discord.Embed(
                title="Set Warning Deletion Period Command",
                description="Please specify the number of days. Usage: `$set_warn_period [days]`",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        else:
            db.set_warn_deletion_period(ctx.guild.id, days)
            embed = discord.Embed(
                title="Warning Deletion Period Set",
                description=f'The warning deletion period has been set to {days} days.',
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)

    @tasks.loop(hours=24)
    async def cleanup_warnings(self):
        for guild in self.bot.guilds:
            db.delete_expired_warnings(guild.id)

    @cleanup_warnings.before_loop
    async def before_cleanup_warnings(self):
        await self.bot.wait_until_ready()

    async def issue_warning(self, ctx, member: discord.Member, reason: str = None):
        db.add_warning(member.id, ctx.guild.id)
        total_warnings = db.get_warnings(member.id)
        embed = discord.Embed(
            title="User Warned",
            description=f'User {member.mention} has been warned for: {reason}.',
            color=discord.Color.orange()
        )
        embed.add_field(name="Total Warnings", value=total_warnings, inline=False)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Cog WarnCog is ready.")

# Required setup function
async def setup(bot):
    await bot.add_cog(WarnCog(bot))

