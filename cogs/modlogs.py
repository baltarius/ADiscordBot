# modlogs.py
"""
Moderation logs system cog.

This cog is for logging different event to make
the moderation more efficient, easier and safer.

This system includes the creation of the categories
and channels and the functions and listeners to log
everything in those channels.

Author: Elcoyote Solitaire
"""
import random
import sqlite3
import datetime
import pytz
import discord
import emoji

from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from discord.app_commands import Choice
from database.permissions import *
from cogs.intercogs import get_server_database, is_exception


class Modlogs(commands.Cog, name="modlogs"):
    """
    Modlogs class for the logging system.

    This class contains commands, automatic functions
    and listeners used for the modlogs' system.

    Args:
        None
    """
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """
        Listener to message edition.

        This will post an embed in a specific channel
        when any message is edited. The post will 
        show the before and after the editing.

        The listener also takes in consideration when
        a channel is added to the exception's list.

        Args:
            None
        """
        if after.author.bot:
            return

        guild = after.guild
        server_id = guild.id
        conn, cur = get_server_database(server_id)
        cur.execute("SELECT id FROM setup WHERE chans = ?", ("edits",))
        row = cur.fetchone()
        author = after.author
        time_zone = pytz.timezone("US/Eastern")
        created_timestamp = before.created_at.astimezone(time_zone).strftime("%Y-%m-%d %H:%M:%S")
        edited_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        embed = discord.Embed(color=0xF1C40F, title="Message edited")
        embed.add_field(name=f"in {after.channel.mention}", value=f"\nby {after.author} \n({after.author.id})")
        embed.add_field(name=f"\nBefore: (created at {created_timestamp})", value=before.content, inline=False)
        for attachment in before.attachments:
            embed.set_image(url=attachment.url)
            embed.add_field(name="Attachment", value=attachment.url, inline=False)
        embed.add_field(name=f"\nAfter: (edited at: {edited_timestamp})", value=after.content, inline=False)
        for attachment in after.attachments:
            embed.set_image(url=attachment.url)
            embed.add_field(name="Attachment", value=attachment.url, inline=False)
        editschan = int(row[0])
        editschanname = self.bot.get_channel(editschan)
        await editschanname.send(embed=embed)
        conn.close()


    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """
        Listener to deletion.

        This will post an embed in a specific channel
        when any message is deleted. The post will 
        show the message and the author.

        The listener also takes in consideration when
        a channel is added to the exception's list.

        Args:
            None
        """
        guild = message.guild
        server_id = guild.id
        conn, cur = get_server_database(server_id)
        if not is_exception(server_id, message.channel.id, "delete"):
            cur.execute("SELECT id FROM setup WHERE chans = ?", ("edits",))
            row = cur.fetchone()
            time_zone = pytz.timezone("US/Eastern")
            created_timestamp = message.created_at.astimezone(time_zone).strftime("%Y-%m-%d %H:%M:%S")
            embed = discord.Embed(color=0xFF0000, title="Message deleted")
            embed.add_field(
                name=f"in {message.channel.mention}",
                value=f"\nfrom: {message.author} ({message.author.id})"
            )
            embed.add_field(
                name=f"\nMessage: (created at {created_timestamp})",
                value=f"{message.content}", inline=False
            )
            editschan = int(row[0])
            editschanname = self.bot.get_channel(editschan)
            await editschanname.send(embed=embed)
        conn.close()


    @commands.Cog.listener()
    async def on_bulk_message_delete(self, message):
        """
        Listener to deletion.

        This will post an embed in a specific channel
        when any message is deleted. The post will 
        show the message and the author.

        The listener also takes in consideration when
        a channel is added to the exception's list.

        Args:
            None
        """
        guild = message[0].guild
        server_id = guild.id
        conn, cur = get_server_database(server_id)
        cur.execute("SELECT id FROM setup WHERE chans = ?", ("edits",))
        row = cur.fetchone()
        async for entry in guild.audit_logs(action=discord.AuditLogAction.message_delete):
            if entry.target.id in [msg.author.id for msg in message]:
                responsible_user = entry.user
                embed = discord.Embed(color=0xF1C40F, title=f"Deleted by: {responsible_user}")
                editschan = int(row[0])
                editschanname = self.bot.get_channel(editschan)
                await editschanname.send(embed=embed)
            conn.close()


    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
        Listener to member joining the server.

        This will post an embed in a specific channel
        when someone join your server. The embed will
        include a few useful informations about the
        new member, like when the account was created
        and it's ID.

        The listener also sends a welcome message in
        a specific channel with a random message.

        Args:
            None
        """
        guild = member.guild
        server_id = guild.id
        conn, cur = get_server_database(server_id)
        cur.execute("SELECT id FROM setup WHERE chans = ?", ("joins",))
        row = cur.fetchone()

        time_zone = pytz.timezone("US/Eastern")
        created_gap = datetime.datetime.now(pytz.utc) - member.created_at
        years = created_gap.days // 365
        months = (created_gap.days % 365) // 30
        weeks = ((created_gap.days % 365) % 30) // 7
        days = ((created_gap.days % 365) % 30) % 7
        hours = created_gap.seconds // 3600
        minutes = (created_gap.seconds // 60) % 60
        seconds = created_gap.seconds % 60

        created_timestamp = member.created_at.astimezone(time_zone).strftime("%Y-%m-%d %H:%M:%S")
        embed = discord.Embed(color=0x00D100, title=member)
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(
            name="Member joined",
            value=f"{member.display_name} ({member.id}) \nCreated {created_timestamp} \n"
            f"Account created {years}y, {months}m, {weeks}w, {days}d, {hours}h, "
            f"{minutes}m and {seconds}s ago"
        )
        if created_gap.days < 7:
            warning = emoji.emojize(":warning:")
            embed.add_field(
                name="NEW ACCOUNT",
                value=f"{warning} ACCOUNT CREATED LESS THAN A WEEK AGO {warning}",
                inline=False
            )
        joinschan = int(row[0])
        joinschanname = self.bot.get_channel(joinschan)
        await joinschanname.send(embed=embed)

        welcome_msgs = [
            f"Welcome aboard **{member.display_name}**!",
            f"It is a pleasure to have you here **{member.display_name}**!",
            f"Oy! **{member.display_name}** just arrived!"
        ]
        cur.execute("SELECT id FROM setup WHERE chans = ?", ("welcome",))
        row = cur.fetchone()
        welcomechan = int(row[0])
        welcomechanname = self.bot.get_channel(welcomechan)
        await welcomechanname.send(random.choice(welcome_msgs))
        conn.close()


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """
        Listener member leaving the server.

        This will post an embed in a specific channel
        when any member leaves the server. The post
        will show informations about the user, such as
        for how long he was on the server.

        Args:
            None
        """
        server_id = member.guild.id
        user = member
        conn, cur = get_server_database(server_id)
        cur.execute("SELECT id FROM setup WHERE chans = ?", ("lefts",))
        row = cur.fetchone()

        time_zone = pytz.timezone("US/Eastern")
        joined_timestamp = member.joined_at.astimezone(time_zone).strftime("%Y-%m-%d %H:%M:%S")

        joined_gap = datetime.datetime.now(pytz.utc) - member.joined_at
        years = joined_gap.days // 365
        months = (joined_gap.days % 365) // 30
        weeks = ((joined_gap.days % 365) % 30) // 7
        days = ((joined_gap.days % 365) % 30) % 7
        hours = joined_gap.seconds // 3600
        minutes = (joined_gap.seconds // 60) % 60
        seconds = joined_gap.seconds % 60

        role_names = [role.name for role in user.roles]
        user_roles = ', '.join(role_names)

        embed = discord.Embed(color=0xFF0000, title=user)
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(
            name="Member left",
            value=f"{user.display_name} ({user.id}) \nJoined {joined_timestamp} \n"
            f"member left after {years}y, {months}m, {weeks}w, {days}d, {hours}h, "
            f"{minutes}m and {seconds}s \nRoles: {user_roles}")
        leftschan = int(row[0])
        leftschanname = self.bot.get_channel(leftschan)
        await leftschanname.send(embed=embed)
        conn.close()


    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """
        Listener to member updates.

        This will post an embed in a specific channel
        when any member update his account, which
        includes profil picture and user name.

        Args:
            None
        """
        if after.bot:
            return

        user = after
        guild = after.guild
        server_id = guild.id
        conn, cur = get_server_database(server_id)
        cur.execute("SELECT id FROM setup WHERE chans = ?", ("users",))
        row = cur.fetchone()

        if row:
            old_name = before.name
            old_discri = before.discriminator
            old_avatar = before.display_avatar
            old_nick = before.display_name
            new_name = after.name
            new_discri = after.discriminator
            new_avatar = after.display_avatar
            new_nick = after.display_name

            embed = discord.Embed(color=0x000000, title=f"USER UPDATE \n({user.id})")
            embed.set_thumbnail(url=old_avatar)
            embed.set_image(url=new_avatar)
            embed.add_field(
                name="before",
                value=f"{before.mention} \nname: {old_nick} ({old_name}#{old_discri})", inline=False
            )
            embed.add_field(
                name="after",
                value=f"{after.mention} \nname: {new_nick} ({new_name}#{new_discri})", inline=False
            )
            userschan = int(row[0])
            userschanname = self.bot.get_channel(userschan)
            await userschanname.send(embed=embed)
        conn.close()


    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        """
        Listener to channel creation.

        This will post an embed in a specific channel
        when any channel, including voice, text and
        categories, are created. If the creation is
        in a category, the embed will show that
        category.

        Args:
            None
        """
        guild = channel.guild
        server_id = guild.id
        conn, cur = get_server_database(server_id)
        cur.execute("SELECT id FROM setup WHERE chans = ?", ("audits",))
        row = cur.fetchone()

        if isinstance(channel, discord.TextChannel):
            type_created = "Channel"
        elif isinstance(channel, discord.VoiceChannel):
            type_created = "Voice channel"
        elif isinstance(channel, discord.CategoryChannel):
            type_created = "Category"
        else:
            type_created = "Other channel"

        embed = discord.Embed(color=0xffffff, title=f"{type_created} updated")
        embed.add_field(
            name=f"{type_created} created",
            value=f"{channel.category} \n╚►{channel.mention} ({channel})"
        )
        auditschan = int(row[0])
        auditschanname = self.bot.get_channel(auditschan)
        await auditschanname.send(embed=embed)
        conn.close()

    async def is_a_bot_chan(self, guild, channel):
        """
        Function that checks for database channels.

        To avoid any problem, this function will make
        sure that any deleted channel was not a part
        of it's database, such as modlogs channels.

        If the deleted channel was part of the database,
        a message will be sent to a specific channel
        letting know the mods that an important channel
        has been deleted.

        Args:
            guild
            channel
        """
        server_id = guild.id
        channel_id = channel.id
        conn, cur = get_server_database(server_id)
        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cur.fetchall()]

        for table_name in tables:
            cur.execute(f"PRAGMA table_info({table_name})")
            column_names = [row[1] for row in cur.fetchall()]

            if "id" in column_names:
                cur.execute(f"SELECT * FROM {table_name} WHERE id = ?", (channel_id,))
                row = cur.fetchone()
                if row:
                    # Found the channel ID in this table, you can now do something with the row
                    # print(f"Channel ID {channel_id} \nTable: {table_name} \nName: {row[0]} {row[1]}")
                    cur.execute(f"DELETE FROM {table_name} WHERE id = ?", (channel_id,))
                    conn.commit()
                    break
                # else:
                   # pass
                    # The channel ID was not found in any table
                    # print(f"Channel ID {channel_id} was not found in any table")
        conn.close()


    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        """
        Listener to channel deletion.

        This will post an embed in a specific channel
        when any channel, including voice, text and
        categories, are deleted. If the deletion is
        in a category, the embed will show that
        category.

        This listener is linked with the function
        is_a_bot_chan, allowing a verification if
        the channel deleted was part of the database.

        Args:
            channel
        """
        guild = channel.guild
        server_id = guild.id
        conn, cur = get_server_database(server_id)
        cur.execute("SELECT id FROM setup WHERE chans = ?", ("audits",))
        row = cur.fetchone()

        await self.is_a_bot_chan(guild, channel)

        if isinstance(channel, discord.TextChannel):
            type_deleted = "Channel"
        elif isinstance(channel, discord.VoiceChannel):
            type_deleted = "Voice channel"
        elif isinstance(channel, discord.CategoryChannel):
            type_deleted = "Category"
        else:
            type_deleted = "Other channel"

        embed = discord.Embed(color=0xffffff, title=f"{type_deleted} updated")
        embed.add_field(name=f"{type_deleted} deleted", value=f"{channel.category} \n╚►***{channel}***")
        auditschan = int(row[0])
        auditschanname = self.bot.get_channel(auditschan)
        await auditschanname.send(embed=embed)
        conn.close()


    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        """
        Listener to channel update.

        This will post an embed in a specific channel
        when any channel, including voice, text and
        categories, are updated. If the updated channel
        is in a category, the embed will show that
        category.

        Args:
            None
        """
        guild = after.guild
        server_id = guild.id
        conn, cur = get_server_database(server_id)
        cur.execute("SELECT * FROM servstats WHERE id = ?", (before.id,))
        rows = cur.fetchall()

        if isinstance(after, discord.TextChannel):
            type_updated = "Channel"
        elif isinstance(after, discord.VoiceChannel):
            type_updated = "Voice channel"
        elif isinstance(after, discord.CategoryChannel):
            type_updated = "Category"
        else:
            type_updated = "Other channel"

        if not rows:
            cur.execute("SELECT id FROM setup WHERE chans = ?", ("audits",))
            row = cur.fetchone()

            if before.name != after.name or before.category != after.category:
                embed = discord.Embed(color=0xffffff, title=f"{type_updated} updated")
                embed.add_field(name="Before", value=f"{before.category} \n╚►***{before}***")
                embed.add_field(name="After", value=f"{after.category} \n╚►***{after} ({after.mention})***")
                auditschan = int(row[0])
                auditschanname = self.bot.get_channel(auditschan)
                await auditschanname.send(embed=embed)

            # else:
                # embed = discord.Embed(color=0xffffff, title="Channel updated")
                # embed.add_field(
                #   name="changes",
                #   value=f"roles: {after.changed_roles} \n"
                #   f"Overwrites: {after.overwrites} \nSynced: {after.permissions_synced}"
                # )
                # auditschan = int(row[0])
                # auditschanname = self.bot.get_channel(auditschan)
                # await auditschanname.send(embed=embed)
        conn.close()


    @commands.hybrid_command(
        name="setchan",
        aliases=["setupchan", "setupchannel", "setchannel"],
        description="user stats"
    )
    @commands.has_permissions(administrator=True)
    @app_commands.describe(logtype="choose the log channel")
    @app_commands.choices(logtype=[
        Choice(name="audits", value=1),
        Choice(name="edits", value=2),
        Choice(name="users", value=3),
        Choice(name="joins", value=4),
        Choice(name="lefts", value=5),
        Choice(name="alerts", value=6),
        Choice(name="level", value=7),
        Choice(name="starboard", value=8),
        Choice(name="suggestion", value=9),
        Choice(name="vote", value=10),
        Choice(name="welcome", value=11),
        Choice(name="ticket", value=12),
        Choice(name="logs", value=13)
    ])
    async def setchan(self, context: Context, logtype: Choice[int], channel):
        """
        Function that setup database channels.

        This function is used to create entries in the
        database for every logs channels available.

        Args:
            context as Context
            logtype as a choice
            channel: #logchan
        """
        guild = context.message.guild
        server_id = guild.id
        conn, cur = get_server_database(server_id)

        cur.execute(
            "INSERT OR REPLACE INTO setup (chans, id) VALUES (?, ?)", (logtype, channel)
        )
        conn.commit()
        conn.close()


    @commands.hybrid_command(
        name="exception",
        description="Set exceptions for channels"
    )
    @commands.has_permissions(administrator=True)
    @app_commands.describe(exceptiontype="choose the exception type")
    @app_commands.choices(exceptiontype=[
        Choice(name="delete", value=1),
        Choice(name="exp", value=2)
    ])
    async def exception(
        self, context: Context, exceptiontype: Choice[int], channel: discord.TextChannel
    ):
        """
        Function that setup exception channels
        in the database of the server.

        This function allows to add exceptions
        channels to avoid to trigger listeners.

        example:
            /exception type #channel

        Args:
            context as Context
            exceptiontype as a choice
            channel: #exceptionchan
        """
        chan_id = channel.id
        guild = context.message.guild
        server_id = guild.id
        conn, cur = get_server_database(server_id)

        cur.execute(
            "INSERT OR REPLACE INTO exception (id, reason) VALUES (?, ?)",
            (chan_id, exceptiontype.name)
        )
        conn.commit()
        conn.close()


async def setup(bot):
    """
    Loads the cog on start.
    """
    await bot.add_cog(Modlogs(bot))
