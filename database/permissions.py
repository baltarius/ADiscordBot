# permissions.py

import discord

from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context


servconfigsnone = "verification_level=VerificationLevel(0), default_notifications=NotificationLevel(0), explicit_content_filter=ContentFilter(0)"
servconfiglow = "verification_level=VerificationLevel(1), default_notifications=NotificationLevel(0), explicit_content_filter=ContentFilter(1)"
servconfighigh = "verification_level=VerificationLevel(2), default_notifications=NotificationLevel(1), explicit_content_filter=ContentFilter(2)"

embedfield = "Creating..."
fieldnameroles1 = "Creation of roles..."
fieldnameroles2 = "Roles created"
fieldnameroles3 = "Editing roles..."
fieldnameroles4 = "Roles edited"
fieldnamecats1 = "Creation of categories..."
fieldnamecats2 = "Categories created"
fieldnamechans1 = "Creation of channels..."
fieldnamechans2 = "Channels created"
fieldnamevoicechans1 = "Creation of voice channels..."
fieldnamevoicechans2 = "Voice channels created"

embeddone = "Creation completed!"

permsfalse = discord.Permissions(add_reactions=False, administrator=False, attach_files=False, ban_members=False, change_nickname=False, connect=False, create_instant_invite=False, create_private_threads=False, create_public_threads=False, deafen_members=False, embed_links=False, external_emojis=False, external_stickers=False, kick_members=False, manage_channels=False, manage_emojis=False, manage_emojis_and_stickers=False, manage_events=False, manage_guild=False, manage_messages=False, manage_nicknames=False, manage_permissions=False, manage_roles=False, manage_threads=False, manage_webhooks=False, mention_everyone=False, moderate_members=False, move_members=False, mute_members=False, priority_speaker=False, read_message_history=False, read_messages=False, request_to_speak=False, send_messages=False, send_messages_in_threads=False, send_tts_messages=False, speak=False, stream=False, use_application_commands=False, use_embedded_activities=False, use_external_emojis=False, use_external_stickers=False, use_voice_activation=False, view_audit_log=False, view_channel=False, view_guild_insights=False)

permsread = discord.Permissions(add_reactions=False, administrator=False, attach_files=False, ban_members=False, change_nickname=False, connect=False, create_instant_invite=False, create_private_threads=False, create_public_threads=False, deafen_members=False, embed_links=False, external_emojis=False, external_stickers=False, kick_members=False, manage_channels=False, manage_emojis=False, manage_emojis_and_stickers=False, manage_events=False, manage_guild=False, manage_messages=False, manage_nicknames=False, manage_permissions=False, manage_roles=False, manage_threads=False, manage_webhooks=False, mention_everyone=False, moderate_members=False, move_members=False, mute_members=False, priority_speaker=False, read_message_history=True, read_messages=True, request_to_speak=False, send_messages=False, send_messages_in_threads=False, send_tts_messages=False, speak=True, stream=False, use_application_commands=False, use_embedded_activities=False, use_external_emojis=False, use_external_stickers=False, use_voice_activation=True, view_audit_log=False, view_channel=False, view_guild_insights=False)

perms1 = discord.Permissions(add_reactions=False, administrator=False, attach_files=False, ban_members=False, change_nickname=False, connect=False, create_instant_invite=False, create_private_threads=False, create_public_threads=False, deafen_members=False, embed_links=False, external_emojis=False, external_stickers=False, kick_members=False, manage_channels=False, manage_emojis=False, manage_emojis_and_stickers=False, manage_events=False, manage_guild=False, manage_messages=False, manage_nicknames=False, manage_permissions=False, manage_roles=False, manage_threads=False, manage_webhooks=False, mention_everyone=False, moderate_members=False, move_members=False, mute_members=False, priority_speaker=False, read_message_history=True, read_messages=True, request_to_speak=False, send_messages=True, send_messages_in_threads=True, send_tts_messages=False, speak=True, stream=False, use_application_commands=False, use_embedded_activities=False, use_external_emojis=False, use_external_stickers=False, use_voice_activation=True, view_audit_log=False, view_channel=False, view_guild_insights=False)

permsver = discord.Permissions(add_reactions=True, administrator=False, attach_files=False, ban_members=False, change_nickname=True, connect=True, create_instant_invite=False, create_private_threads=False, create_public_threads=False, deafen_members=False, embed_links=True, external_emojis=True, external_stickers=True, kick_members=False, manage_channels=False, manage_emojis=False, manage_emojis_and_stickers=False, manage_events=False, manage_guild=False, manage_messages=False, manage_nicknames=False, manage_permissions=False, manage_roles=False, manage_threads=False, manage_webhooks=False, mention_everyone=False, moderate_members=False, move_members=False, mute_members=False, priority_speaker=False, read_message_history=True, read_messages=True, request_to_speak=True, send_messages=True, send_messages_in_threads=True, send_tts_messages=False, speak=True, stream=True, use_application_commands=False, use_embedded_activities=False, use_external_emojis=True, use_external_stickers=True, use_voice_activation=True, view_audit_log=False, view_channel=False, view_guild_insights=False)

permsofficer = discord.Permissions(add_reactions=True, administrator=False, attach_files=True, ban_members=False, change_nickname=True, connect=True, create_instant_invite=True, create_private_threads=True, create_public_threads=True, deafen_members=False, embed_links=True, external_emojis=True, external_stickers=True, kick_members=False, manage_channels=False, manage_emojis=False, manage_emojis_and_stickers=False, manage_events=True, manage_guild=False, manage_messages=False, manage_nicknames=False, manage_permissions=False, manage_roles=False, manage_threads=False, manage_webhooks=False, mention_everyone=True, moderate_members=False, move_members=True, mute_members=True, priority_speaker=True, read_message_history=True, read_messages=True, request_to_speak=True, send_messages=True, send_messages_in_threads=True, send_tts_messages=False, speak=True, stream=True, use_application_commands=False, use_embedded_activities=True, use_external_emojis=True, use_external_stickers=True, use_voice_activation=True, view_audit_log=False, view_channel=False, view_guild_insights=False)

permsdevs = discord.Permissions(add_reactions=True, administrator=False, attach_files=True, ban_members=False, change_nickname=True, connect=True, create_instant_invite=True, create_private_threads=True, create_public_threads=True, deafen_members=False, embed_links=True, external_emojis=True, external_stickers=True, kick_members=False, manage_channels=False, manage_emojis=False, manage_emojis_and_stickers=False, manage_events=False, manage_guild=False, manage_messages=False, manage_nicknames=False, manage_permissions=False, manage_roles=True, manage_threads=True, manage_webhooks=False, mention_everyone=True, moderate_members=True, move_members=True, mute_members=True, priority_speaker=True, read_message_history=True, read_messages=True, request_to_speak=True, send_messages=True, send_messages_in_threads=True, send_tts_messages=False, speak=True, stream=True, use_application_commands=True, use_embedded_activities=True, use_external_emojis=True, use_external_stickers=True, use_voice_activation=True, view_audit_log=False, view_channel=False, view_guild_insights=False)

permsmod = discord.Permissions(add_reactions=True, administrator=False, attach_files=True, ban_members=True, change_nickname=True, connect=True, create_instant_invite=True, create_private_threads=True, create_public_threads=True, deafen_members=True, embed_links=True, external_emojis=True, external_stickers=True, kick_members=True, manage_channels=False, manage_emojis=False, manage_emojis_and_stickers=False, manage_events=True, manage_guild=False, manage_messages=True, manage_nicknames=True, manage_permissions=False, manage_roles=True, manage_threads=True, manage_webhooks=False, mention_everyone=True, moderate_members=True, move_members=True, mute_members=True, priority_speaker=True, read_message_history=True, read_messages=True, request_to_speak=True, send_messages=True, send_messages_in_threads=True, send_tts_messages=False, speak=True, stream=True, use_application_commands=True, use_embedded_activities=True, use_external_emojis=True, use_external_stickers=True, use_voice_activation=True, view_audit_log=True, view_channel=False, view_guild_insights=False)

permsadmin = discord.Permissions(add_reactions=True, administrator=False, attach_files=True, ban_members=True, change_nickname=True, connect=True, create_instant_invite=True, create_private_threads=True, create_public_threads=True, deafen_members=True, embed_links=True, external_emojis=True, external_stickers=True, kick_members=True, manage_channels=True, manage_emojis=True, manage_emojis_and_stickers=True, manage_events=True, manage_guild=False, manage_messages=True, manage_nicknames=True, manage_permissions=True, manage_roles=True, manage_threads=True, manage_webhooks=True, mention_everyone=True, moderate_members=True, move_members=True, mute_members=True, priority_speaker=True, read_message_history=True, read_messages=True, request_to_speak=True, send_messages=True, send_messages_in_threads=True, send_tts_messages=False, speak=True, stream=True, use_application_commands=True, use_embedded_activities=True, use_external_emojis=True, use_external_stickers=True, use_voice_activation=True, view_audit_log=True, view_channel=True, view_guild_insights=True)



listcats = {
"Infos": "default",
"Lobby": "default",
"Medias": "verified",
"Voice": "verified",
"Officer": "officer",
"Moderation": "moderator",
"admin": "admin"
}

listchans = {
    "Welcome": "Infos",
    "auto-role":"Infos", 
    "Infos": "Infos",
    "tips": "Infos",
    "Lobby1": "Lobby",
    "Lobby2": "Lobby",
    "Pictures": "Medias",
    "Videos": "Medias",
    "music": "Medias",
    "mod-chat": "Moderation",
    "mod-logs": "Moderation",
    "admin-chat": "admin",
    "admin-logs": "admin",
    "test": "admin"
}

listvoicechans = {
    "Lobby1": "Voice",
    "Lobby2": "Voice",
    "Officers": "Officer",
    "Admins": "admin"
}

listroles = {
    "admin": permsadmin,
    "moderator": permsmod,
    "officer": permsofficer,
    "verified": permsver
#    "User": perms1
}


proserver = [
    {
    "_-¯ welcome ¯-_": "default",
    "_-¯ News ¯-_": "default",
    "_-¯ Support ¯-_": "verified",
    "_-¯ General ¯-_": "verified",
    "_-¯ Members corner ¯-_": "verified",
    "_-¯ Admin ¯-_": "moderator",
    "_-¯ Mod Logs ¯-_": "admin",
    "_-¯ Tickets ¯-_": "admin"
    },
    {
    "Rules": "_-¯ welcome ¯-_",
    "Boost":"_-¯ welcome ¯-_", 
    "Welcome": "_-¯ welcome ¯-_",
    "Announcement": "_-¯ News ¯-_",
    "Updates": "_-¯ News ¯-_",
    "Bug-Report": "_-¯ Support ¯-_",
    "Ticket": "_-¯ Support ¯-_",
    "Lobby": "_-¯ General ¯-_",
    "Discussion": "_-¯ General ¯-_",
    "Starboard": "_-¯ Members corner ¯-_",
    "Suggestion": "_-¯ Members corner ¯-_",
    "Vote": "_-¯ Members corner ¯-_",
    "Medias": "_-¯ Members corner ¯-_",
    "Level": "_-¯ Members corner ¯-_",
    "Admin": "_-¯ Admin ¯-_",
    "Notes": "_-¯ Admin ¯-_",
    "setups": "_-¯ Admin ¯-_",
    "Audits": "_-¯ Mod Logs ¯-_",
    "Edits": "_-¯ Mod Logs ¯-_",
    "Users": "_-¯ Mod Logs ¯-_",
    "Lefts": "_-¯ Mod Logs ¯-_",
    "Joins": "_-¯ Mod Logs ¯-_",    
    "Alerts": "_-¯ Mod Logs ¯-_",
    "Logs": "_-¯ Tickets ¯-_"
    },
    {
    "admin": permsadmin,
    "bot": permsfalse,
    "moderator": permsmod,
    "devs": permsdevs,
    "booster": permsfalse,
    "blue": permsfalse,
    "green": permsfalse,
    "orange": permsfalse,
    "purple": permsfalse
    }
]



verifiedrole = "discord.utils.get(guild.roles, name=verified)"
moderatorrole = "discord.utils.get(guild.roles, name=moderator)"
adminrole = "discord.utils.get(guild.roles, name=admin)"
officerrole = "discord.utils.get(guild.roles, name=officer)"

verifiedon = {
    "ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False, connect=False)",
    "verifiedrole: discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True, speak=True)",
    "officerrole: discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True, speak=True)",
    "moderatorrole: discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True, speak=True)"
}

moderatoron = {
    "moderatorrole: discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True, speak=True)"
}
officeron = {
    "officerrole: discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True, speak=True)",
    "moderatorrole: discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True, speak=True)"
}

setup_chans = {
    "audits",
    "edits",
    "users",
    "joins",
    "lefts",
    "alerts",
    "level",
    "starboard",
    "suggestion",
    "vote",
    "welcome",
    "ticket",
    "logs"
}

log_chans = [
    "audits",
    "edits",
    "users",
    "joins",
    "lefts",
    "alerts",
    "level",
    "starboard",
    "suggestion",
    "vote",
    "welcome",
    "ticket",
    "logs"
]