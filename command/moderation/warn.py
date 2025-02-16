import discord
from discord.ext import commands
import sqlite3
import os

# Initialize the database connection
db_path = os.path.join(os.path.dirname(__file__), 'warnings.db')
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Create the warnings table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS warnings (
                user_id INTEGER PRIMARY KEY,
                count INTEGER
            )''')
conn.commit()

def get_warnings(user_id):
    c.execute('SELECT count FROM warnings WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    return result[0] if result else 0

def add_warning(user_id):
    current_count = get_warnings(user_id)
    if current_count == 0:
        c.execute('INSERT INTO warnings (user_id, count) VALUES (?, ?)', (user_id, 1))
    else:
        c.execute('UPDATE warnings SET count = ? WHERE user_id = ?', (current_count + 1, user_id))
    conn.commit()

def warn(bot):
    @bot.command()
    @commands.has_permissions(manage_messages=True)
    async def warn(ctx, member: discord.Member = None, *, reason=None):
        if member is None:
            embed = discord.Embed(
                title="Warning Command",
                description="Please specify a user to warn. Usage: `$warn @user [reason]`",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        else:
            add_warning(member.id)
            total_warnings = get_warnings(member.id)
            embed = discord.Embed(
                title="User Warned",
                description=f'User {member.mention} has been warned for: {reason}.',
                color=discord.Color.orange()
            )
            embed.add_field(name="Total Warnings", value=total_warnings, inline=False)
            await ctx.send(embed=embed)

    @warn.error
    async def warn_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="Permission Error",
                description="You are missing Manage Messages permission(s) to run this command.",
                color=discord.Color.red()
            )
            bot_message = await ctx.send(embed=embed)
            await ctx.message.delete(delay=2)
            await bot_message.delete(delay=2)

    @bot.command()
    async def warn_count(ctx, member: discord.Member = None):
        if member is None:
            embed = discord.Embed(
                title="Warning Count Command",
                description="Please specify a user to check warnings. Usage: `$warn_count @user`",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        else:
            count = get_warnings(member.id)
            embed = discord.Embed(
                title="Warning Count",
                description=f'User {member.mention} has {count} warning(s).',
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)

