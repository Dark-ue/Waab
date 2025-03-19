import discord
from discord.ext import commands
from datetime import timedelta

def mod_event(bot):
    @bot.command()
    @commands.has_permissions(kick_members=True)
    async def kick(ctx, member: discord.Member = None, *, reason=None):
        if member is None:
            embed = discord.Embed(
                title="Kick Command",
                description="Please specify a user to kick. Usage: `$kick @user [reason]`",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        else:
            await member.kick(reason=reason)
            embed = discord.Embed(
                title="User Kicked",
                description=f'User {member.mention} has been kicked for: {reason}.',
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)

    @bot.command()
    @commands.has_permissions(ban_members=True)
    async def ban(ctx, member: discord.Member = None, *, reason=None):
        if member is None:
            embed = discord.Embed(
                title="Ban Command",
                description="Please specify a user to ban. Usage: `$ban @user [reason]`",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        else:
            await member.ban(reason=reason)
            embed = discord.Embed(
                title="User Banned",
                description=f'User {member.mention} has been banned for: {reason}.',
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)

    @bot.command()
    @commands.has_permissions(moderate_members=True)
    async def timeout(ctx, member: discord.Member = None, duration: int = 0, *, reason=None):
        if member is None or duration <= 0:
            embed = discord.Embed(
                title="Timeout Command",
                description="Please specify a user and a valid duration (in minutes) to timeout. Usage: `$timeout @user [duration] [reason]`",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        else:
            until = discord.utils.utcnow() + timedelta(minutes=duration)
            await member.timeout(until, reason=reason)
            embed = discord.Embed(
                title="User Timed Out",
                description=f'User {member.mention} has been timed out for {duration} minutes for: {reason}.',
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)

    @bot.command()
    @commands.has_permissions(moderate_members=True)
    async def untimeout(ctx, member: discord.Member = None):
        if member is None:
            embed = discord.Embed(
                title = "Error",
                description="Please specify a user to untimeout. Usage: `$timeout @user`",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        else:
            await member.untimeout()
            embed = discord.Embed(
                title="User Untimed Out",
                description=f'User {member.mention} has been untimed out.',
                color=discord.Color.green()
            )

    @bot.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(ctx, limit: str = None):
        if limit is None:
            embed = discord.Embed(
                title="Purge Command",
                description="Please specify a valid number of messages to purge or type 'all' to clear the chat. Usage: `$purge [limit]`",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        elif limit.lower() == 'all':
            await ctx.channel.purge()
            embed = discord.Embed(
                title="Messages Purged",
                description='All messages have been purged.',
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
        else:
            try:
                limit = int(limit)
                if limit <= 0:
                    raise ValueError
                await ctx.channel.purge(limit=limit)
                embed = discord.Embed(
                    title="Messages Purged",
                    description=f'{limit} messages have been purged.',
                    color=discord.Color.orange()
                )
                await ctx.send(embed=embed)
            except ValueError:
                embed = discord.Embed(
                    title="Purge Command",
                    description="Please specify a valid number of messages to purge or type 'all' to clear the chat. Usage: `$purge [limit]`",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)

    @bot.command()
    @commands.has_permissions(administrator=True)
    async def leave(ctx):
        embed = discord.Embed(
            title="Leave Command",
            description="The bot is leaving the server.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
        await ctx.guild.leave()

#list of commands
#kick
#ban
#timeout
#purge
#leave