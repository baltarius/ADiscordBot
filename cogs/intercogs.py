# intercogs.py
"""
Functions use through the bot.

This file is to store every functions that are used through the entire bot.
The main function here is get_server_database.

Author: Elcoyote Solitaire
"""
import sqlite3
import json
import pytz

from discord.ext import commands


time_zone = pytz.timezone("US/Eastern")

with open("config.json", "r", encoding="utf-8") as jsonfile:
    config = json.load(jsonfile)
cprefix = config["prefix"]


def get_server_database(server_id):
    """
    Main function to obtain servers' database.
    Creates all the necessary tables if they aren't created yet.

    Args:
        server_id: The ID of the server.
    """
    db_file = f"./database/servers/{server_id}.db"
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    # Create your tables here
    cur.execute('''CREATE TABLE IF NOT EXISTS stats
        (id INTEGER PRIMARY KEY,
        messages INTEGER,
        words INTEGER,
        characters INTEGER,
        emojis INTEGER,
        reactions INTEGER,
        edited INTEGER,
        deleted INTEGER)''')
    conn.commit()

    cur.execute('''CREATE TABLE IF NOT EXISTS setup
        (chans TEXT PRIMARY KEY,
        id INTEGER)''')
    conn.commit()

    cur.execute('''CREATE TABLE IF NOT EXISTS level
        (id INTEGER PRIMARY KEY,
        exp INTEGER,
        level INTEGER,
        total INTEGER)''')
    conn.commit()

    cur.execute('''CREATE TABLE IF NOT EXISTS reaction
        (message INTEGER,
        emoji TEXT,
        type TEXT,
        role INTEGER)''')
    conn.commit()

    cur.execute('''CREATE TABLE IF NOT EXISTS servstats
        (chans TEXT PRIMARY KEY,
        id INTEGER,
        region TEXT)''')
    conn.commit()

    cur.execute('''CREATE TABLE IF NOT EXISTS suggestion
        (number INTEGER PRIMARY KEY AUTOINCREMENT,
        id INTEGER,
        authorid INTEGER,
        decision TEXT)''')
    conn.commit()

    cur.execute('''CREATE TABLE IF NOT EXISTS exception
        (id INTEGER,
        reason TEXT)''')
    conn.commit()

    return conn, cur


# exception function to update the table is in the modlogs.py
def is_exception(server_id, channel_id, reason):
    """
    Verify if the channel is in the exception's list.

    Args:
        server_id: The ID of the server.
        channel_id: The ID of the channel to verify.
        reason: The specific reason to be an exception.
    """
    conn, cur = get_server_database(server_id)
    cur.execute("SELECT * FROM exception WHERE id = ? AND reason = ?", (channel_id, reason))
    row = cur.fetchone()
    conn.close()

    return bool(row)


def is_suggestion(server_id, channel_id):
    """
    Verify if the channel is in the exception's list.

    Args:
        server_id: The ID of the server.
        channel_id: The ID of the channel to verify.
        reason: The specific reason to be an exception.
    """
    conn, cur = get_server_database(server_id)
    cur.execute("SELECT id FROM setup WHERE chans = ?", ("suggestion",))
    row = cur.fetchone()
    conn.close()
    if row:
        if channel_id == row[0]:
            return True
        else:
            return False
    else:
        return False


class Intercogs(commands.Cog, name="intercogs"):
    """
    Intercogs class for utilities.

    This class contains utility to be used through the bot's cogs.
    Empty for now.
    
    Args:
        None
    """
    def __init__(self, bot):
        self.bot = bot



async def setup(bot):
    """
    Loads the cog on start.
    """
    await bot.add_cog(Intercogs(bot))
