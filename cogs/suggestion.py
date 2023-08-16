# suggestion.py
"""
Suggestion system cog.

This cog is for the suggestion's system, which allows users to
create, from a specific channel, suggestions that will be then
displayed in another specific channel where people will be able
to vote with one reaction per user.

This system includes the possibility of adding an attachment to
the suggestion, which will be added in the vote channel.

Author: Elcoyote Solitaire
"""
import asyncio
import sqlite3
import discord

from discord import app_commands
from discord.utils import get
from discord.ext import commands
from discord.ext.commands import Context
from discord.app_commands import Choice
from database.permissions import *
from cogs.intercogs import get_server_database


class Suggestion(commands.Cog, name="suggestion"):
    """
    Suggestion class for the suggestion system.

    This class contains commands, automatic functions
    and listeners used for the suggestion's system.

    Args:
        None
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="suggestion",
        description="setup suggestion system"
    )
    @commands.has_permissions(administrator=True)
    @app_commands.describe(logchan="choose the log channel")
    @app_commands.choices(logchan=[
        Choice(name="Suggestion channel", value=1),
        Choice(name="Vote channel", value=2),
    ])
    async def suggestion(
        self, context: Context, logchan: Choice[int], channel: discord.TextChannel
    ):
        """
        Suggestion/Vote channel creation.

        This command is used to select both suggestion and
        vote channels by pointing which is which.

        Example:
            /suggestion Suggestion channel #suggestion 
            /suggestion Vote channel #vote

        Args:
            context as Context.
            logchan as a choice between Suggestion and Vote.
            channel as a textchannel on the server.
        """
        guild = context.message.guild
        server_id = guild.id
        conn, cur = get_server_database(server_id)

        if logchan.value == 1:
            cur.execute(
                "INSERT OR REPLACE INTO setup (chans, id) VALUES (?, ?)", ("Suggestion", channel.id)
            )
            conn.commit()
            await context.send(f"Suggestion channel set to {channel.mention}")

        elif logchan.value == 2:
            cur.execute(
                "INSERT OR REPLACE INTO setup (chans, id) VALUES (?, ?)", ("vote", channel.id)
            )
            conn.commit()
            await context.send(f"Vote channel set to {channel.mention}")
        else:
            await context.send(f"logchan: {logchan}, channel: {channel}")
        conn.close()


    @commands.hybrid_command(
        name="suggest",
        description="suggest an idea"
    )
    @commands.has_permissions(administrator=True)
    @app_commands.describe()
    async def suggest(self, context: Context, *, suggestion: str):
        """
        Function to create a suggestion.

        This will first make sure the /suggestion is used in the
        suggestion channel, then will copy the suggestion into
        the vote channel, adding a up and down reaction to allows
        people to vote, to finaly delete the suggestion from the
        suggestion channel.

        Args:
            context as Context
            suggestion: The suggestion made by the user as a str
        """
        guild = context.message.guild
        server_id = guild.id
        user = context.message.author
        conn, cur = get_server_database(server_id)
        cur.execute("SELECT * FROM setup WHERE chans = ?", ("suggestion",))
        row = cur.fetchone()
        if row[1] == context.channel.id and suggestion:
            cur.execute("SELECT * FROM setup WHERE chans = ?", ("vote",))
            row = cur.fetchone()
            if row:
                votechan = row[1]
                votechanname = self.bot.get_channel(votechan)
                cur.execute("SELECT MAX(number) FROM suggestion")
                result = cur.fetchone()
                number = result[0] + 1 if result[0] is not None else 1
                embed = discord.Embed(title=f"Suggestion #{number}", color=0xFFFF00)
                embed.set_thumbnail(url=user.avatar)
                embed.add_field(name=f"By {context.message.author}", value=suggestion, inline=False)
                if context.message.attachments:
                    embed.add_field(
                        name="Attachment", value=context.message.attachments, inline=False
                    )
                suggestion_msg = await votechanname.send(embed=embed)
                await suggestion_msg.add_reaction("⬆️")
                await suggestion_msg.add_reaction("⬇️")
                cur.execute(
                    "INSERT INTO suggestion (id) VALUES (?)", (suggestion_msg.id,)
                )
                conn.commit()
                confirmation = await context.send(f"Suggestion #{number} confirmed")
                await asyncio.sleep(3)
                await confirmation.delete()

            else:
                await context.send("The database doesn't have the vote channel setup")
        elif row[1] != context.channel.id:
            suggestion_channel = self.bot.get_channel(row[1])
            await context.send(f"Please use the command in {suggestion_channel.mention}")
        else:
            await context.send("Please make sure the setup of the suggestion system is done")
        conn.close()


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """
        Listener to reactions.

        This will make sure users don't react with
        both arrows (up and down) on a suggestion. 

        Args:
            None
        """
        if payload.member.bot:
            return

        guild = self.bot.get_guild(payload.guild_id)
        server_id = guild.id
        channel = guild.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
        user = guild.get_member(payload.user_id)
        conn, cur = get_server_database(server_id)
        cur.execute("SELECT * FROM suggestion WHERE id = ?", (reaction.message.id,))
        row = cur.fetchone()
        if row:
            if reaction.emoji == "⬆️":
                down_reaction = discord.utils.get(reaction.message.reactions, emoji="⬇️")
                if down_reaction:
                    users = down_reaction.users()
                    async for member in users:
                        if member == user:
                            # The user has already reacted with ⬇️, so remove their reaction
                            await reaction.remove(user)
                            break
            elif reaction.emoji == "⬇️":
                up_reaction = discord.utils.get(reaction.message.reactions, emoji="⬆️")
                if up_reaction:
                    users = up_reaction.users()
                    async for member in users:
                        if member == user:
                            # The user has already reacted with ⬆️, so remove their reaction
                            await reaction.remove(user)
                            break
        conn.close()


async def setup(bot):
    """
    Loads the cog on start.
    """
    await bot.add_cog(Suggestion(bot))
