# creating.py
"""
¤¤¤¤¤¤¤¤¤¤¤¤¤¤ W A R N I N G ¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤
¤ THIS COG CONTAINS COMMAND THAT ALLOWS YOU TO DELETE         ¤
¤ EVERYTHING ON YOUR SERVER. PLEASE USE CAREFULLY.            ¤
¤                                                             ¤
¤ DISCLAIMER:                                                 ¤
¤ I AM NOT RESPONSIBLE FOR ANY MISUSE OF THIS COG AND         ¤
¤ YOU SHOULD BE CAREFUL WHO YOU ALLOW TO HAVE ADMIN'S         ¤
¤ PERMISSIONS. READ CAREFULLY THE DOCUMENTATION IN THIS FILE. ¤
¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤¤

Creation system cog.

This cog uses pre-made templates to create servers fully
automatic. It takes care of creating roles, categories, 
channels, databases and setup the configuration of the 
server in the best way possible.

It also has a function to delete everything on the server,
which includes all roles, categories and channels, leaving
only roles above the bot's role and creating a single
"general" channel so you don't have an empty server.

Author: Elcoyote Solitaire
"""
import sqlite3
import discord

from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from database.permissions import *
from cogs.intercogs import get_server_database


class Creating(commands.Cog, name="creating"):
    """
    Creating class for the automatic server creation.

    This class contains commands, automatic functions
    and listeners used for the suggestion's system.

    Args:
        None
    """
    def __init__(self, bot):
        self.bot = bot


    @commands.hybrid_command(
        name="rdef",
        description="Delete channels"
    )
    @commands.has_permissions(manage_channels=True, manage_roles=True)
    @app_commands.describe()
    async def rdef(self, context: Context):
        """
        Dummy command to test.

        This is used to change the @everyone role's
        permissions so the view channel is False

        Args:
            context as Context
        """
        guild = context.message.guild
        roledefault = context.guild.default_role
        await roledefault.edit(permissions=discord.Permissions(view_channel=False))


    @commands.hybrid_command(
        name="getget",
        description="get get get get"
    )
    @commands.has_permissions(manage_channels=True, manage_roles=True)
    @app_commands.describe()
    async def getget(self, context: Context):
        """
        Dummy command to test.

        This is used to get the id of the channel
        "audits" then print it in the console.

        Args:
            context as Context
        """
        guild = context.message.guild
        audit = discord.utils.get(guild.channels, name="audits")
        print(audit.id)


    @commands.hybrid_command(
        name="delchans",
        description="delete server's channels and roles"
    )
    @commands.has_permissions(administrator=True)
    @app_commands.describe()
    async def delchans(self, context: Context):
        """
        W A R N I N G
        
        THIS FUNCTION WILL DELETE EVERY ROLES, CATEGORIES
        AND CHANNELS ON YOUR SERVER. DON'T USE UNLESS
        YOU REALLY WANT TO LOSE EVERYTHING. 

        Args:
            context as Context
        """
        guild = context.message.guild
        permsgen = {
            guild.default_role: discord.PermissionOverwrite(
            read_messages=True,
            read_message_history=True,
            add_reactions=True,
            send_messages=True,
            view_channel=True)
        }
        for role in context.guild.roles:
            try:
                await role.delete()
            except:
                await context.send(f"Cannot delete {role.name}")
        for chan in context.guild.channels:
            await chan.delete()
        await guild.create_text_channel(name="general", overwrites=permsgen)


    @commands.hybrid_command(
        name="procreatelist1",
        description="create server's categories, channels and roles"
    )
    @commands.has_permissions(administrator=True)
    @app_commands.describe()
    async def procreatelist1(self, context: Context):
        """
        Main creation function.

        This will setup everything automatically, from the roles 
        to the database, including channels and permissions 

        Args:
            context as Context
        """
        guild = context.message.guild
        roledefault = context.guild.default_role
        embed = discord.Embed(title="Creation of template:")
        embedcreating = "Creating . . ."
        embed.add_field(name=fieldnameroles1, value=embedcreating)
        embed.set_field_at(0, name=fieldnameroles1, value=embedcreating)
        embedcreation = await context.send(embed=embed)
        embedfield = " "

        for roleroles in proserver[2]:
            embedfield += f"{roleroles}\n"
            embed.set_field_at(0, name=fieldnameroles1, value=embedfield)
            await embedcreation.edit(embed=embed)
            await guild.create_role(name=roleroles, permissions=proserver[2][roleroles])

        embedfield += "\nRoles created"
        embed.set_field_at(0, name=fieldnameroles1, value=embedfield)
        await embedcreation.edit(embed=embed)

        embed.add_field(name=fieldnamecats1, value=embedcreating)
        embed.set_field_at(1, name=fieldnamecats1, value=embedcreating)
        embedfield = " "

        for catcats in proserver[0]:
            embedfield += f"{catcats}\n"
            embed.set_field_at(1, name=fieldnamecats1, value=embedfield)
            await embedcreation.edit(embed=embed)
            cattochange = await guild.create_category(name=catcats)

            if proserver[0][catcats] == "default":
                overwriteit = {
                    roledefault: discord.PermissionOverwrite(read_messages=True, connect=True)
                }
                await cattochange.edit(overwrites=overwriteit)

            elif proserver[0][catcats] == "verified":
                overwriteit = { roledefault: discord.PermissionOverwrite(
                    read_messages=True,
                    send_messages=True,
                    connect=True)
                }
                await cattochange.edit(overwrites=overwriteit)

            elif proserver[0][catcats] == "officer":
                overwriteit = {
                    discord.utils.get(guild.roles, name="officer"): discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True, speak=True),
                    discord.utils.get(guild.roles, name="moderator"): discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True, speak=True)
                }
                await cattochange.edit(overwrites=overwriteit)

            elif proserver[0][catcats] == "moderator":
                overwriteit = {
                    discord.utils.get(guild.roles, name="moderator"): discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True, speak=True)
                }
                await cattochange.edit(overwrites=overwriteit)

        embedfield += "\nCategories created"
        embed.set_field_at(1, name=fieldnamecats1, value=embedfield)
        await embedcreation.edit(embed=embed)

        embed.add_field(name=fieldnamechans1, value=embedcreating)
        embed.set_field_at(2, name=fieldnamechans1, value=embedcreating)
        await embedcreation.edit(embed=embed)
        embedfield = " "

        for chanchans in proserver[1]:
            embedfield += f"{chanchans}\n"
            embed.set_field_at(2, name=fieldnamechans1, value=embedfield)
            await embedcreation.edit(embed=embed)
            await guild.create_text_channel(
                name=chanchans, category=discord.utils.get(guild.categories, name=proserver[1][chanchans])
            )

        embedfield += "\nChannels created"
        embed.set_field_at(2, name=fieldnamechans1, value=embedfield)
        await embedcreation.edit(embed=embed)

        embed.add_field(name=fieldnameroles3, value="Editing roles . . .")
        embed.set_field_at(3, name=fieldnameroles3, value=f"Editing {roledefault}...")
        await embedcreation.edit(embed=embed)
        await roledefault.edit(permissions=permsfalse)

        embedfield = f"\n{roledefault} edited\n\n{fieldnameroles4}"
        embed.set_field_at(3, name=fieldnameroles3, value=embedfield)
        await embedcreation.edit(embed=embed)

        embed.add_field(name="Database update", value="Database update . . .")
        embed.set_field_at(4, name="Database update", value="Updating setup database...")
        await embedcreation.edit(embed=embed)

        server_id = guild.id
        conn, cur = get_server_database(server_id)
        cur.execute('''CREATE TABLE IF NOT EXISTS setup
            (chans TEXT PRIMARY KEY,
            id INTEGER)''')
        row = cur.fetchone()

        for setchans in setup_chans:
            setchans_name = discord.utils.get(guild.channels, name=setchans)
            setchans_id = setchans_name.id
            if row:
                cur.execute(
                    "UPDATE setup SET id = ? WHERE chans = ?", (setchans_id, setchans)
                )
                conn.commit()
                conn.close()
            else:
                cur.execute(
                    "INSERT INTO setup (chans, id) VALUES(?, ?)", (setchans, setchans_id)
                )
                conn.commit()
                conn.close()

        embedfield = "\nSetup table edited\n\n Database updated"
        embed.set_field_at(4, name="Database update", value=embedfield)
        await embedcreation.edit(embed=embed)

        embed.add_field(name="Completed", value="Template created successfuly!")
        embed.set_field_at(5,
            name="Creation of template completed successfully",
            value=f"Template created by request of {context.author} (ID: {context.author.id})"
        )
        await embedcreation.edit(embed=embed)


    @commands.hybrid_command(
        name="helptest",
        description="quick test command"
    )
    @commands.has_permissions(administrator=True)
    @app_commands.describe()
    async def helptest(self, context: Context):
        """
        Dummy function to test.

        This will print lists/dictionnaries from permissions

        Args:
            context as Context
        """
        guild = context.message.guild
        for setchans in setup_chans:
            print(f"setchans: {setchans}")
            setchans_name = discord.utils.get(guild.channels, name=setchans)
            print(f"setchans_name: {setchans_name}")
            setchans_id = setchans_name.id
            print(f"setchans_id: {setchans_id}")



async def setup(bot):
    """
    Loads the cog on start.
    """
    await bot.add_cog(Creating(bot))
