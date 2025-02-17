import discord
from discord.ext import commands, tasks
import sqlite3
import os
import datetime

# Initialize the database connection
db_path = os.path.join(os.path.dirname(__file__), 'warnings.db')
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Drop the warnings table if it exists (for schema update)
c.execute('''DROP TABLE IF EXISTS warnings''')

# Create the warnings table with the correct schema
c.execute('''CREATE TABLE IF NOT EXISTS warnings (
                user_id INTEGER,
                count INTEGER,
                timestamp DATETIME,
                guild_id INTEGER,
                PRIMARY KEY (user_id, timestamp)
            )''')

# Create the settings table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS settings (
                guild_id INTEGER PRIMARY KEY,
                warn_deletion_period INTEGER DEFAULT 10
            )''')
conn.commit()

def get_warnings(user_id):
    c.execute('SELECT count FROM warnings WHERE user_id = ?', (user_id,))
    result = c.fetchall()
    return sum([row[0] for row in result])

def add_warning(user_id, guild_id):
    timestamp = datetime.datetime.now()
    c.execute('INSERT INTO warnings (user_id, count, timestamp, guild_id) VALUES (?, ?, ?, ?)', (user_id, 1, timestamp, guild_id))
    conn.commit()

def delete_expired_warnings(guild_id):
    c.execute('SELECT warn_deletion_period FROM settings WHERE guild_id = ?', (guild_id,))
    result = c.fetchone()
    if result:
        expiration_days = result[0]
    else:
        expiration_days = 10  # Default to 10 days if no setting is found
    expiration_date = datetime.datetime.now() - datetime.timedelta(days=expiration_days)
    c.execute('DELETE FROM warnings WHERE timestamp < ? AND guild_id = ?', (expiration_date, guild_id))
    conn.commit()

def set_warn_deletion_period(guild_id, days):
    c.execute('INSERT OR REPLACE INTO settings (guild_id, warn_deletion_period) VALUES (?, ?)', (guild_id, days))
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
            add_warning(member.id, ctx.guild.id)
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

    @bot.command()
    @commands.has_permissions(administrator=True)
    async def set_warn_period(ctx, days: int = None):
        if days is None:
            embed = discord.Embed(
                title="Set Warning Deletion Period Command",
                description="Please specify the number of days. Usage: `$set_warn_period [days]`",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        else:
            set_warn_deletion_period(ctx.guild.id, days)
            embed = discord.Embed(
                title="Warning Deletion Period Set",
                description=f'The warning deletion period has been set to {days} days.',
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)

    @tasks.loop(hours=24)
    async def cleanup_warnings():
        for guild in bot.guilds:
            delete_expired_warnings(guild.id)

    @bot.event
    async def on_ready():
        cleanup_warnings.start()

#list of commands
# $warn @user [reason] - Warn a user
# $warn_count @user - Check the number of warnings for a user
# $set_warn_period [days] - Set the warning deletion period in days