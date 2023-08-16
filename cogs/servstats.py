# servstats.py
"""
Server statistics cog.

This cog is for server statistics (displayed as voice channel)
The stats include a clock that can show any timezone but also
how many members, users, bots, categories, channels and roles
are present on the server.

Author: Elcoyote Solitaire
"""
import datetime
import sqlite3
import pytz
import discord

from datetime import datetime
from discord import app_commands
from discord.ext import commands, tasks
from discord.ext.commands import Context
from discord.utils import get
from database.permissions import *
from cogs.intercogs import get_server_database


class Servstats(commands.Cog, name="servstats"):
    """
    Statistics class for server.

    This class contains commands, automatic functions
    and loops used for the server statistics system.

    Args:
        None
    """
    def __init__(self, bot):
        self.bot = bot
        self.clock = "clock"
        self.channel_name_updater.start()


    @commands.hybrid_command(
        name="createservstats",
        description="create server stats channels"
    )
    @commands.has_permissions(administrator=True)
    @app_commands.describe()
    async def createservstats(self, context: Context):
        """
        Automation functions for server stats.

        This will create everything necessary to display the stats,
        which includes database entries, categories and channels.

        Args:
            context as Context
        """
        guild = context.message.guild
        server_id = guild.id
        conn, cur = get_server_database(server_id)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(connect=False, view_channel=True)
        }

        #clock
        region = "America/Montreal"
        clock = "clock"
        clock_channel = await guild.create_voice_channel(
            name=f"[Local]: {datetime.now(pytz.timezone(region)).strftime('%H:%M')}",
            position=0, overwrites=overwrites)
        clock_id = clock_channel.id
        cur.execute("SELECT * FROM servstats WHERE chans = ?", (clock,))
        existing_row = cur.fetchone()
        if existing_row:
            cur.execute(
                "UPDATE servstats SET id = ?, region = ? WHERE chans = ?", (clock_id, region, clock)
            )
        else:
            cur.execute(
                "INSERT INTO servstats (chans, id, region) VALUES(?, ?, ?)",
                (clock, clock_id, region)
            )

        # stats [members, channels, roles]
        bot_count = sum(member.bot for member in guild.members)
        channel_count = len([
            channel for channel in guild.channels if not isinstance(channel, discord.CategoryChannel)
        ])
        user_count = guild.member_count - bot_count

        stats_cat = await guild.create_category(
            name="📊 Server Stats 📊", overwrites=overwrites, position=99
        )

        category_count = len([
            channel for channel in guild.channels if isinstance(channel, discord.CategoryChannel)
        ])

        members_channel = await guild.create_voice_channel(
            name=f"[Members]: {guild.member_count}", category=stats_cat, overwrites=overwrites
        )
        users_channel = await guild.create_voice_channel(
            name=f"[Users]: {user_count}", category=stats_cat, overwrites=overwrites
        )
        bots_channel = await guild.create_voice_channel(
            name=f"[Bots]: {bot_count}", category=stats_cat, overwrites=overwrites
        )
        category_channel = await guild.create_voice_channel(
            name=f"[Categories]: {category_count}", category=stats_cat, overwrites=overwrites
        )
        channels_channel = await guild.create_voice_channel(
            name=f"[Channels]: {channel_count}", category=stats_cat, overwrites=overwrites
        )
        roles_channel = await guild.create_voice_channel(
            name=f"[Roles]: {len(guild.roles)}", category=stats_cat, overwrites=overwrites
        )

        memschan = members_channel.id
        userschan = users_channel.id
        botschan = bots_channel.id
        catschan = category_channel.id
        chanschan = channels_channel.id
        roleschan = roles_channel.id

        cur.execute("SELECT * FROM servstats WHERE chans = ?", ("members",))
        existing_row = cur.fetchone()
        if existing_row:
            pass
            #cur.execute("UPDATE servstats SET id = ? WHERE chans = ?", (memschan, "members"))
            #cur.execute("UPDATE servstats SET id = ? WHERE chans = ?", (userschan, "users"))
            #cur.execute("UPDATE servstats SET id = ? WHERE chans = ?", (botschan, "bots"))
            #cur.execute("UPDATE servstats SET id = ? WHERE chans = ?", (catschan, "categories"))
            #cur.execute("UPDATE servstats SET id = ? WHERE chans = ?", (chanschan, "channels"))
            #cur.execute("UPDATE servstats SET id = ? WHERE chans = ?", (roleschan, "roles"))
        else:
            cur.execute("INSERT INTO servstats (chans, id) VALUES(?, ?)", ("members", memschan))
            cur.execute("INSERT INTO servstats (chans, id) VALUES(?, ?)", ("users", userschan))
            cur.execute("INSERT INTO servstats (chans, id) VALUES(?, ?)", ("bots", botschan))
            cur.execute("INSERT INTO servstats (chans, id) VALUES(?, ?)", ("categories", catschan))
            cur.execute("INSERT INTO servstats (chans, id) VALUES(?, ?)", ("channels", chanschan))
            cur.execute("INSERT INTO servstats (chans, id) VALUES(?, ?)", ("roles", roleschan))

        conn.commit()
        conn.close()


    @tasks.loop(minutes=1)
    async def channel_name_updater(self):
        """
        Updates the name of the channels of the stats system.

        This loops run every minute and check if the time is a multiple
        of 5 minutes for the clock and 15 minutes for the other stats.

        Args:
            None
        """
        current_minute = int(discord.utils.utcnow().strftime('%M'))
        if current_minute % 5 == 0:
            for guild in self.bot.guilds:
                server_id = guild.id
                conn, cur = get_server_database(server_id)
                clock = "clock"
                cur.execute("SELECT id FROM servstats WHERE chans = ?", (clock,))
                row = cur.fetchone()
                if row:
                    channel = int(row[0])
                    channame = self.bot.get_channel(channel)
                    local_time = datetime.now().strftime('%H:%M')
                    await channame.edit(name=f'local: {local_time}')
                conn.close

            if current_minute % 15 == 0:
                for guild in self.bot.guilds:
                    conn, cur = get_server_database(server_id)
                    cur.execute(
                        "SELECT * FROM servstats WHERE chans IN (?, ?, ?, ?, ?, ?)",
                        ("members", "users", "bots", "categories", "channels", "roles")
                    )
                    rows = cur.fetchall()
                    if len(rows) >= 6:
                        channel_ids = {row[0]: row[1] for row in rows}
                        chan_mem_id = int(channel_ids.get("members"))
                        chan_users_id = int(channel_ids.get("users"))
                        chan_bots_id = int(channel_ids.get("bots"))
                        chan_cats_id = int(channel_ids.get("categories"))
                        chan_chans_id = int(channel_ids.get("channels"))
                        chan_roles_id = int(channel_ids.get("roles"))

                        bot_count = sum(member.bot for member in guild.members)
                        user_count = guild.member_count - bot_count
                        channel_count = len([
                            channel for channel in guild.channels if not isinstance(channel, discord.CategoryChannel)
                        ])
                        category_count = len([
                            channel for channel in guild.channels if isinstance(channel, discord.CategoryChannel)
                        ])

                        chan_mem_name = self.bot.get_channel(chan_mem_id)
                        await chan_mem_name.edit(name=f'[Members]: {guild.member_count}')

                        chan_users_name = self.bot.get_channel(chan_users_id)
                        await chan_users_name.edit(name=f'[Users]: {user_count}')

                        chan_bots_name = self.bot.get_channel(chan_bots_id)
                        await chan_bots_name.edit(name=f'[Bots]: {bot_count}')

                        chan_cats_name = self.bot.get_channel(chan_cats_id)
                        await chan_cats_name.edit(name=f'[Categories]: {category_count}')

                        chan_chans_name = self.bot.get_channel(chan_chans_id)
                        await chan_chans_name.edit(name=f'[Channels]: {channel_count}')

                        chan_roles_name = self.bot.get_channel(chan_roles_id)
                        await chan_roles_name.edit(name=f'[Roles]: {len(guild.roles)}')

                    conn.close


    @channel_name_updater.before_loop
    async def before_channel_name_updater(self):
        """
        Function waiting for bot to be ready.

        Allows the bot to be ready before starting the loop.

        Args:
            None
        """
        await self.bot.wait_until_ready()



async def setup(bot):
    """
    Loads the cog on start.
    """
    await bot.add_cog(Servstats(bot))
