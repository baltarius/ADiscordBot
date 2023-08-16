# reactionrole.py
"""
Reaction role upgraded to buttons.

This file contains everything needed to create a
message with buttons for self roles on a server.

Author: Elcoyote Solitaire
"""
import discord
import sqlite3
import datetime
import pytz
import emoji

from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from database.permissions import *
from discord.app_commands import Choice
from cogs.intercogs import get_server_database


class Reactionrole(commands.Cog, name="reactionrole"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="rr",
        description="reaction role"
    )
    @commands.has_permissions(administrator=True)
    @app_commands.describe()
    @app_commands.choices(rrset=[
        Choice(name="set", value=1),
        Choice(name="create", value=2),
        ],
        rrtype=[
        Choice(name="normal", value=1),
        Choice(name="unique", value=2),
        Choice(name="verify", value=3),
        Choice(name="reverse", value=4),
    ])
    async def rr(self, context: Context, rrset: Choice[int], rrtype: Choice[int]):
        guild = context.message.guild
        server_id = guild.id
        conn, cur = get_server_database(server_id)


class PersistentView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label='Green', style=discord.ButtonStyle.green, custom_id='persistent_view:green')
    async def green(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('This is green.', ephemeral=True)

    @discord.ui.button(label='Red', style=discord.ButtonStyle.red, custom_id='persistent_view:red')
    async def red(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('This is red.', ephemeral=True)

    @discord.ui.button(label='Grey', style=discord.ButtonStyle.grey, custom_id='persistent_view:grey')
    async def grey(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('This is grey.', ephemeral=True)



async def setup(bot):
    await bot.add_cog(Reactionrole(bot))