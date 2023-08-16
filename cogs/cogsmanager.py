# cogsmanager.py
"""
Functions for managing cogs.

This file contains what is needed to
load, unload and reload cogs.

Author: Elcoyote Solitaire
"""
import discord

from typing import Literal, Optional
from discord import app_commands
from discord.ext import commands


class Cogsmanager(commands.Cog, name="cogsmanager"):
    """
    Cogs manager.

    This class contains commands to load, unload and
    reload cogs.
    
    Args:
        None
    """
    def __init__(self, bot):
        self.bot = bot


    @commands.hybrid_command(
        name="load",
        description="Loads a specific cog"
    )
    @commands.is_owner()
    @app_commands.describe()
    async def load(self, ctx, cog_name):
        """
        Loads a specified cog to the bot.

        Args:
            ctx (commands.Context): The context of the command.
            cog_name (str): The name of the cog to load.

        Raises:
            commands.ExtensionFailed: If loading the cog fails.
        """
        try:
            await self.bot.load_extension(f'cogs.{cog_name}')
            await ctx.send(f'{cog_name} cog has been loaded.')
        except commands.ExtensionFailed as extension_failed:
            await ctx.send(f'Error loading {cog_name} cog: {extension_failed}')


    @commands.hybrid_command(
        name="unload",
        description="Unloads a specific cog"
    )
    @commands.is_owner()
    @app_commands.describe()
    async def unload(self, ctx, cog_name):
        """
        Unloads a specified cog from the bot.

        Args:
            ctx (commands.Context): The context of the command.
            cog_name (str): The name of the cog to unload.

        Raises:
            commands.ExtensionNotLoaded: If the specified cog is not loaded.
            commands.ExtensionFailed: If unloading the cog fails.
        """
        try:
            await self.bot.unload_extension(f'cogs.{cog_name}')
            await ctx.send(f'{cog_name} cog has been unloaded.')
        except commands.ExtensionFailed as extension_failed:
            await ctx.send(f'Error unloading {cog_name} cog: {extension_failed}')


    @commands.hybrid_command(
        name="reload",
        description="Reloads a specific cog"
    )
    @commands.is_owner()
    @app_commands.describe()
    async def reload(self, ctx, cog_name):
        """
        Unloads a specified cog from the bot then loads it back.

        Args:
            ctx (commands.Context): The context of the command.
            cog_name (str): The name of the cog to unload.

        Raises:
            commands.ExtensionNotLoaded: If the specified cog is not loaded.
            commands.ExtensionFailed: If reloading the cog fails.
        """
        try:
            await self.bot.unload_extension(f'cogs.{cog_name}')
            await self.bot.load_extension(f'cogs.{cog_name}')
            await ctx.send(f'{cog_name} cog has been reloaded.')
        except commands.ExtensionFailed as extension_failed:
            await ctx.send(f'Error reloading {cog_name} cog: {extension_failed}')


    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(
        self, ctx: commands.Context, guilds: commands.Greedy[discord.Object],
        spec: Optional[Literal["~", "*", "^"]] = None) -> None:
        """
        Function to sync commands.

        Examples:
            !sync
                This takes all global commands within the CommandTree
                and sends them to Discord. (see CommandTree for more info.)
            !sync ~
                This will sync all guild commands for the current context’s guild.
            !sync *
                This command copies all global commands to the current
                guild (within the CommandTree) and syncs.
            !sync ^
                This command will remove all guild commands from the CommandTree
                and syncs, which effectively removes all commands from the guild.
            !sync 123 456 789
                This command will sync the 3 guild ids we passed: 123, 456 and 789.
                Only their guilds and guild-bound commands.

        Args:
            ctx as context
            guilds: guild(s) to sync
            spec: optional with 1 argument only
        """
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")


async def setup(bot):
    """
    Loads the cog on start.
    """
    await bot.add_cog(Cogsmanager(bot))
