# stats.py
"""
User statistics cog.

This cog is for user statistics (gather, process and display)
The stats include msgs, words, characters and emojis
but also reactions and messages edited and deleted. 

Author: Elcoyote Solitaire
"""
import random
import math
import sqlite3
import discord
import emoji

from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context
from cogs.intercogs import get_server_database


class Stats(commands.Cog, name="stats"):
    """
    Statistics class for users.

    This class contains listeners and commands used for the stats system.

    Args:
        None
    """
    def __init__(self, bot):
        self.bot = bot


    async def update_stats(self, id, msg, mots, chars, emos, react, edits, deletes, server_id):
        """
        Updates the stats of the user.

        Args:
            id: The ID of the user.
            msg: The amount of messages.
            mots: The amount of words.
            chars: The amount of characters.
            emos: The amount of emojis
            react: The amount of reactions
            edits: The amount of messages edited.
            deletes: The amount of messages deleted.
            server_id: The ID of the server.
        """
        conn, cur = get_server_database(server_id)
        cur.execute("SELECT * FROM stats WHERE id = ?", (id,))
        row = cur.fetchone()
        if row:
            # user exists already, update the stats
            messages = row[1] + msg
            words = row[2] + mots
            characters = row[3] + chars
            emojis = row[4] + emos
            reactions = row[5] + react
            edited = row[6] + edits
            deleted = row[7] + deletes

            cur.execute(
                "UPDATE stats SET messages = ?, words = ?, characters = ?, emojis = ?, "
                "reactions = ?, edited = ?, deleted = ? WHERE id = ?", 
                (messages, words, characters, emojis, reactions, edited, deleted, id)
            )
            conn.commit()
            conn.close()

        else:
            # user does not exist, add a new line
            messages = msg
            words = mots
            characters = chars
            emojis = emos
            edited = edits
            deleted = deletes

            cur.execute(
                "INSERT INTO stats (id, messages, words, characters, emojis, "
                "reactions, edited, deleted) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                (id, msg, mots, chars, emos, react, edits, deletes)
            )
            conn.commit()
            conn.close()


    async def update_level(self, id, exp, server_id):
        """
        Updates the level of the user.

        Args:
            id: the ID of the user.
            exp: the amount of exp to add.
            server_id: The ID of the server.
        """
        conn, cur = get_server_database(server_id)
        cur.execute("SELECT * FROM level WHERE id = ?", (id,))
        row = cur.fetchone()
        if row:
            # user exists already, update the stats.
            total = row[3] + exp
            exp = row[1] + exp
            level = row[2]
            if exp / 1000 > 1:
                exp -= 1000
                level += 1
                cur.execute(
                    "UPDATE level SET exp = ?, level = ?, total = ? WHERE id = ?",
                    (exp, level, total, id)
                )
                conn.commit()
                cur.execute("SELECT id FROM setup WHERE chans = ?", ("level",))
                result = cur.fetchone()
                member = f"<@{id}>"
                lvlup_msg = [
                    f"Congratulations {member} for reaching level {level}!",
                    f"{member} is on fire! and also now level {level}.",
                    f"I can't believe it! {member} made it to level {level}!"
                ]
                levelchan = int(result[0])
                levelchanname = self.bot.get_channel(levelchan)
                await levelchanname.send(random.choice(lvlup_msg))
                conn.close()

            else:
                cur.execute("UPDATE level SET exp = ?, total = ? WHERE id = ?", (exp, total, id))
                conn.commit()
                conn.close()

        else:
            # user does not exist, add a new line
            level = 0
            total = 0
            total += exp

            cur.execute(
                "INSERT INTO level (id, exp, level, total) VALUES(?, ?, ?, ?)",
                (id, exp, level, total)
            )
            conn.commit()
            conn.close()


    @commands.hybrid_command(
        name="stats",
        description="user stats"
    )
    @commands.has_permissions(send_messages=True)
    @app_commands.describe()
    async def stats(self, context: Context, user: discord.Member = None):
        """
        Stats command that displays the stats of a member.
        Can be used with or without a discord member.
        example: 
            /stats > returns the stats of the one performing the command.
            /stats @elcoyotesolitaire > returns the stats of the member @elcoyotesolitaire.

        Args:
            context as Context
            user as discord.Member (None by default)
        """
        user = user or context.author
        id = user.id
        guild = context.message.guild
        server_id = guild.id
        conn, cur = get_server_database(server_id)

        cur.execute("SELECT * FROM stats WHERE id = ?", (id,))
        result = cur.fetchone()

        if result is None:
            await context.send("This user has no stats yet.")
            conn.close()
        else:
            messages_sent = result[1]
            words_written = result[2]
            characters_written = result[3]
            emojis_used = result[4]
            reactions = result[5]
            messages_edited = result[6]
            messages_deleted = result[7]

            embed = discord.Embed(title=f"{user}'s stats", color=0x00ff00)
            embed.set_thumbnail(url=user.avatar)
            embed.add_field(name="Messages sent", value=messages_sent, inline=True)
            embed.add_field(name="Words written", value=words_written, inline=True)
            embed.add_field(name="Characters written", value=characters_written, inline=True)
            embed.add_field(name="Emojis used", value=emojis_used, inline=True)
            embed.add_field(name="Reactions", value=reactions, inline=True)
            embed.add_field(name="Messages edited", value=messages_edited, inline=True)
            embed.add_field(name="Messages deleted", value=messages_deleted, inline=True)
            await context.send(embed=embed)
            conn.close()


    @commands.hybrid_command(
        name="level",
        aliases=["lvl", "exp", "xp"],
        description="user level"
    )
    @commands.has_permissions(send_messages=True)
    @app_commands.describe()
    async def level(self, context: Context, user: discord.Member = None):
        """
        Level command that displays the level of a member.
        Can be used with or without a discord member.
        example: 
            /level > returns the level of the one performing the command.
            /level @elcoyotesolitaire > returns the level of the member @elcoyotesolitaire.

        Args:
            context as Context
            user as discord.Member (None by default)
        """
        user = user or context.author
        id = user.id
        guild = context.message.guild
        server_id = guild.id
        conn, cur = get_server_database(server_id)

        cur.execute("SELECT * FROM level WHERE id = ?", (id,))
        result = cur.fetchone()

        if result is None:
            await context.send("This user has no exp yet.")
            conn.close()
        else:
            level = result[2]
            exp = result[1]
            pcent_exp = round(exp / 10, 2)
            total = result[3]
            target_data = total

            cur.execute("SELECT total, RANK() OVER (ORDER BY total DESC) AS rank FROM level")
            rows = cur.fetchall()

            rank = next((row[1] for row in rows if row[0] == target_data), None)

            cur.execute("SELECT COUNT(*) FROM level")
            row_count = cur.fetchone()[0]

            embed = discord.Embed(title=f"{user}'s level", color=0x0000FF)
            embed.set_thumbnail(url=user.avatar)
            embed.add_field(name="Level:", value=level, inline=False)
            embed.add_field(name="Exp:", value=f"{pcent_exp}%", inline=False)
            embed.add_field(name="Rank:", value=f"#{rank}/{row_count}", inline=False)

            await context.send(embed=embed)
            conn.close()


    @commands.hybrid_command(
        name="reset",
        description="reset user level"
    )
    @commands.has_permissions(administrator=True)
    @app_commands.describe()
    async def reset(self, context: Context, user: discord.Member = None):
        """
        Reset command that reset the level of a member.
        Can be used with or without a discord member.
        example: 
            /reset > resets the level of the one performing the command.
            /reset @elcoyotesolitaire > resets the level of the member @elcoyotesolitaire.

        Args:
            context as Context
            user as discord.Member (None by default)
        """
        user = user or context.author
        id = user.id
        guild = context.message.guild
        server_id = guild.id
        conn, cur = get_server_database(server_id)

        cur.execute("UPDATE level SET exp = ?, level = ?, total = ? WHERE id = ?", (0, 0, 0, id))
        conn.commit()
        await context.send(f"{user}'s experience has been reset to 0.")
        conn.close()


    @commands.hybrid_command(
        name="addexp",
        aliases=["addxp"],
        description="reset user level"
    )
    @commands.has_permissions(administrator=True)
    @app_commands.describe()
    async def addexp(self, context: Context, user: discord.Member, exp):
        """
        Command that adds an amount of experience to a member (max 1000).
        example: 
            /addexp @elcoyotesolitaire 500 > adds 500 exp to the current experience
            of the member @elcoyotesolitaire.

        Args:
            context as Context
            user as discord.Member
            exp: the amount of exp to add (from 1 to 1000).
        """
        id = user.id
        exp = int(exp)
        guild = context.message.guild
        server_id = guild.id
        if isinstance(exp, int):
            if 1 <= exp <= 1000:
                await self.update_level(id, exp, server_id)
                await context.send(f"Added {exp} experience to {user}.")
            else:
                await context.send(f"{exp} is out of range. Must be from 1 to 1000.")
        else:
            await context.send(
                f"{exp} is a {type(exp).__name__}. It must be a number from 1 and 1000."
            )


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
        user_id = message.author.id
        words = message.content.split()
        nbr_words = len(words)
        characters = 0
        messages = 1
        emojis = 0
        for char in message.content:
            if emoji.is_emoji(char) is True:
                emojis += 1
        characters = len(''.join(words))
        characters -= emojis
        nbr_words -= emojis
        get_server_database(server_id)
        await self.update_stats(
            user_id, messages, nbr_words, characters, emojis, 0, 0, 0, server_id
        )
        exp = math.ceil(characters/10 + random.randint(3,5))
        await self.update_level(user_id, exp, server_id)


    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """
        Listener for message deletion.

        Args:
            message: The deleted message.
        """
        if message.author.bot:
            return

        user_id = message.author.id
        guild = message.guild
        server_id = guild.id
        await self.update_stats(user_id, 0, 0, 0, 0, 0, 0, 1, server_id)


    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """
        Listener for reactions.

        Args:
            reaction: The reaction.
            user: The user doing the reaction.
        """
        if user.bot:
            return

        user_id = user.id
        guild = user.guild
        server_id = guild.id
        await self.update_stats(user_id, 0, 0, 0, 0, 1, 0, 0, server_id)


    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """
        Listener for edited messages.
        
        Args:
            before: The message before the edition.
            after: The message after the edition.
        """
        if after.author.bot:
            return

        user_id = after.author.id
        guild = after.guild
        server_id = guild.id
        await self.update_stats(user_id, 0, 0, 0, 0, 0, 1, 0, server_id)


async def setup(bot):
    """
    Loads the cog on start.
    """
    await bot.add_cog(Stats(bot))
