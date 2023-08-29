# suggestion.py
"""
Suggestion system cog.

This cog is for the suggestion's system, which allows users to
create, from a specific channel, suggestions that will be then
displayed in another specific channel where people will be able
to vote with one reaction per user.

This system includes the possibility of adding an attachment to
the suggestion, which will be added in the vote channel.

The decision system allows the admin to approve/deny/considerate
any suggestion using the suggestion's ID number then removes all
the reaction votes from the embed message to include the stats 
in the embed itself, changes the color accordingly with the
decision and states the decision and who took it.

Note: the timestamp in the embed shows the time the suggestion
was made first, then update to when the decision was taken. To
know when the suggestion was made, refer to the embed message
time of creation in discord.

Author: Elcoyote Solitaire
"""
import asyncio
import sqlite3
import discord

from datetime import datetime
from discord import app_commands
from discord.utils import get
from discord.ext import commands
from discord.ext.commands import Context
from discord.app_commands import Choice
from database.permissions import *
from cogs.intercogs import get_server_database, time_zone, cprefix


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
    @commands.has_permissions(send_messages=True)
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
            suggestion: The suggestion text
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
                embed = discord.Embed(
                    title=f"Suggestion #{number}",
                    color=0x0000FF,
                    description=suggestion
                )
                embed.set_thumbnail(url=user.avatar)
                embed.set_footer(
                    text=f"Suggested by: {context.message.author.display_name}"
                )
                if context.message.attachments:
                    for attachment in context.message.attachments:
                        await attachment.save(attachment.filename)
                    file = discord.File(attachment.filename)
                    embed.add_field(
                        name=" ",
                        value=f"Attachment: {attachment.filename}",
                        inline=False
                    )
                    embed.set_image(url=f"attachment://{attachment.filename}")
                embed.timestamp = datetime.now(time_zone)
                suggestion_msg = await votechanname.send(file=file, embed=embed)
                await suggestion_msg.add_reaction("⬆️")
                await suggestion_msg.add_reaction("⬇️")
                cur.execute(
                    "INSERT INTO suggestion (id, authorid) VALUES (?, ?)", (suggestion_msg.id, context.message.author.id,)
                )
                conn.commit()
                confirmation = await context.send(f"Suggestion #{number} confirmed")
                await asyncio.sleep(3)
                await confirmation.delete()
                if not context.interaction:
                    await context.message.delete()

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


    @commands.hybrid_command(
        name="decision",
        description="Take a decision on a suggestion"
    )
    @commands.has_permissions(administrator=True)
    @app_commands.describe()
    @app_commands.choices(result=[
        Choice(name="approve", value=1),
        Choice(name="deny", value=2),
        Choice(name="considerate", value=3)
    ])
    async def decision(self, context: Context, sugg_id: int,
        result: Choice[int], reason: str = None):
        """
        Function to approve a suggestion.

        This will first make sure the /suggestion is used in the
        suggestion channel, then will copy the suggestion into
        the vote channel, adding a up and down reaction to allows
        people to vote, to finaly delete the suggestion from the
        suggestion channel.

        Args:
            context as Context
            sugg_id: The suggestion's number as an integer
            result: a CHOICE between approve/deny/considerate
            reason: The reason why the suggestion is approve
                as a string. None by default
        """
        guild = context.message.guild
        server_id = guild.id
        conn, cur = get_server_database(server_id)
        cur.execute("SELECT * FROM suggestion WHERE number = ?", (sugg_id,))
        suggtable = cur.fetchone()
        if suggtable:
            message_id = suggtable[1]
            author_id = suggtable[2]
            author_name = self.bot.get_user(author_id)
            cur.execute("SELECT id FROM setup WHERE chans = ?", ("vote",))
            vote_id = cur.fetchone()[0]
            vote_name = context.guild.get_channel(vote_id)
            message = await vote_name.fetch_message(message_id)
            embed = message.embeds[0]
            created_time = message.created_at.astimezone(time_zone)
            reactionup = discord.utils.get(message.reactions, emoji="⬆️")
            reactiondown = discord.utils.get(message.reactions, emoji="⬇️")
            countup = reactionup.count if reactionup else 0
            countdown = reactiondown.count if reactiondown else 0
            countup -= 1
            countdown -= 1
            embed.add_field(
                name="Votes",
                value=f"⬆️: {countup} \n️⬇️: {countdown}"
            )
            if result.name == "approve":
                embed.add_field(
                    name=" ",
                    value=f"Suggested by: {author_name.name} ({created_time.strftime('%Y-%m-%d %H:%M:%S')}) \n***APPROVED*** \nReason: {reason}",
                    inline=False
                )
                embed.color=0x008000
                embed.timestamp = datetime.now(time_zone)
            elif result.name == "deny":
                embed.add_field(
                    name=" ",
                    value=f"Suggested by: {author_name.name} ({created_time.strftime('%Y-%m-%d %H:%M:%S')}) \n***DENIED*** \nReason: {reason}",
                    inline=False
                )
                embed.color=0xFF0000
                embed.timestamp = datetime.now(time_zone)
            elif result.name == "considerate":
                embed.add_field(
                    name=" ",
                    value=f"Suggested by: {author_name.name} ({created_time.strftime('%Y-%m-%d %H:%M:%S')}) \n***CONSIDERATED*** \nReason: {reason}",
                    inline=False
                )
                embed.color=0xFCAE1E
                embed.timestamp = datetime.now(time_zone)
            else:
                await context.send(f"Invalid decision ({result}).")

            embed.set_footer(text=f"Decision made by: {context.author.display_name}")
            await message.edit(embed=embed)
            the_file = message.attachments
            await message.remove_attachments(the_file)
            await message.clear_reactions()
            print(f"{result.name}, {sugg_id}")
            cur.execute("UPDATE suggestion SET decision = ? WHERE number = ?", (result.name, sugg_id))
            conn.commit()
            conn.close()
            confirmation = await context.send(f"Embed message set as {result.name}.")
            await asyncio.sleep(3)
            await confirmation.delete()
        else:
            await context.send(f"Suggestion #{sugg_id} not found.")
            conn.close()


    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Listener for messages.

        Args:
            message: The message.
        """
        if message.author.bot:
            return
        guild = message.guild
        server_id = guild.id
        conn, cur = get_server_database(server_id)
        cur.execute("SELECT * FROM setup WHERE chans = ?", ("suggestion",))
        row = cur.fetchone()
        print(self.bot.command_prefix)
        if row:
            sugg_chan_id = row[1]
            sugg_chan = guild.get_channel(sugg_chan_id)
            if message.channel == sugg_chan:
                if not message.content.startswith(f"{cprefix}suggest"):
                    not_sugg = await message.channel.send(
                        "Only suggestions are allowed in this channel.\n"
                        f"Please try to use /suggest or {cprefix}suggest"
                    )
                    await asyncio.sleep(5)
                    await not_sugg.delete()
                    await message.delete()


async def setup(bot):
    """
    Loads the cog on start.
    """
    await bot.add_cog(Suggestion(bot))
