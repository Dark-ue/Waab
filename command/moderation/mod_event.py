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

    @kick.error
    async def kick_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="Permission Error",
                description="You are missing Kick Members permission(s) to run this command.",
                color=discord.Color.red()
            )
            bot_message = await ctx.send(embed=embed)
            await ctx.message.delete(delay=2)
            await bot_message.delete(delay=2)

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

    @ban.error
    async def ban_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="Permission Error",
                description="You are missing Ban Members permission(s) to run this command.",
                color=discord.Color.red()
            )
            bot_message = await ctx.send(embed=embed)
            await ctx.message.delete(delay=2)
            await bot_message.delete(delay=2)

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

    @timeout.error
    async def timeout_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="Permission Error",
                description="You are missing Moderate Members permission(s) to run this command.",
                color=discord.Color.red()
            )
            bot_message = await ctx.send(embed=embed)
            await ctx.message.delete(delay=2)
            await bot_message.delete(delay=2)

#list of commands
#kick
#ban
#timeout
