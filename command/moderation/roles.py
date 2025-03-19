import discord
from discord.ext import commands

def roles(bot):
    @bot.command()
    @commands.has_permissions(manage_roles=True)
    async def addrole(ctx, member: discord.Member = None, role: discord.Role = None):
        if member is None or role is None:
            embed = discord.Embed(
                title="Add Role Command",
                description="Please specify a user and a role to add. Usage: `$addrole @user @role`",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        else:
            await member.add_roles(role)
            embed = discord.Embed(
                title="Role Added",
                description=f'Role {role.mention} has been added to {member.mention}.',
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)

    @bot.command()
    @commands.has_permissions(manage_roles=True)
    async def removerole(ctx, member: discord.Member = None, role: discord.Role = None):
        if member is None or role is None:
            embed = discord.Embed(
                title="Remove Role Command",
                description="Please specify a user and a role to remove. Usage: `$removerole @user @role`",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        else:
            await member.remove_roles(role)
            embed = discord.Embed(
                title="Role Removed",
                description=f'Role {role.mention} has been removed from {member.mention}.',
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)

    @bot.command()
    @commands.has_permissions(manage_roles=True)
    async def createrole(ctx, *, name: str = None):
        if name is None:
            embed = discord.Embed(
                title="Create Role Command",
                description="Please specify a name for the role. Usage: `$createrole [name]`",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        else:
            guild = ctx.guild
            await guild.create_role(name=name)
            embed = discord.Embed(
                title="Role Created",
                description=f'Role `{name}` has been created.',
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)

    @bot.command()
    @commands.has_permissions(manage_roles=True)
    async def deleterole(ctx, role: discord.Role = None):
        if role is None:
            embed = discord.Embed(
                title="Delete Role Command",
                description="Please specify a role to delete. Usage: `$deleterole @role`",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
        else:
            await role.delete()
            embed = discord.Embed(
                title="Role Deleted",
                description=f'Role {role.name} has been deleted.',
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)


#list of commands
#addrole
#removerole
#createrole
#deleterole