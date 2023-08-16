# templates.py

import platform
import aiohttp
import discord

from discord import app_commands
from discord import Embed
from discord.ext import commands
from discord.ext.commands import Context
from helpers import checks
from database.permissions import *
from discord.utils import get


async def delchans1(self, context: Context):
    guild = context.message.guild
    for role in context.guild.roles:  
        try:  
            await role.delete()
        except:
            await context.send(f"Cannot delete {role.name}")
    for c in context.guild.channels:
        await c.delete()
    await guild.create_text_channel("general")

    
async def testcreatelist1(self, context: Context):
    guild = context.message.guild
    roledefault = context.guild.default_role
    embed = discord.Embed(title="Creation of template:")
    embedcreating = "Creating . . ."
    embed.add_field(name=fieldnameroles1, value=embedcreating)
    embed.set_field_at(0, name=fieldnameroles1, value=embedcreating)
    embedcreation = await context.send(embed=embed)
    embedfield = " "
    
    for roleroles in listroles:
        embedfield += f"{roleroles}\n"
        embed.set_field_at(0, name=fieldnameroles1, value=embedfield)
        await embedcreation.edit(embed=embed)
        await guild.create_role(name=roleroles, permissions=listroles[roleroles])
    
    embedfield += "\nRoles created"
    embed.set_field_at(0, name=fieldnameroles1, value=embedfield)
    await embedcreation.edit(embed=embed)
    
    embed.add_field(name=fieldnamecats1, value=embedcreating)
    embed.set_field_at(1, name=fieldnamecats1, value=embedcreating)
    embedfield = " "
        
    for catcats in listcats:
        embedfield += f"{catcats}\n"
        embed.set_field_at(1, name=fieldnamecats1, value=embedfield)
        await embedcreation.edit(embed=embed)
        cattochange = await guild.create_category(name=catcats)
        
        if listcats[catcats] == "default":
            overwriteit = { roledefault: discord.PermissionOverwrite(read_messages=True, connect=True)}
            await cattochange.edit(overwrites=overwriteit)
            #print(f"{roledefault} and cattochange:{cattochange}, {verifiedon}")

        elif listcats[catcats] == "verified":
            overwriteit = { roledefault: discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)}
            await cattochange.edit(overwrites=overwriteit)
        
        elif listcats[catcats] == "officer":
            overwriteit = {
                discord.utils.get(guild.roles, name="officer"): discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True, speak=True),
                discord.utils.get(guild.roles, name="moderator"): discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True, speak=True)
            }
            await cattochange.edit(overwrites=overwriteit)
        
        elif listcats[catcats] == "moderator":
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
    
    for chanchans in listchans:
        embedfield += f"{chanchans}\n"
        embed.set_field_at(2, name=fieldnamechans1, value=embedfield)
        await embedcreation.edit(embed=embed)  
        await guild.create_text_channel(name=chanchans, category=discord.utils.get(guild.categories, name=listchans[chanchans]))
    
    embedfield += "\nChannels created"
    embed.set_field_at(2, name=fieldnamechans1, value=embedfield)
    await embedcreation.edit(embed=embed)
    
    embed.add_field(name=fieldnamechans1, value=embedcreating)
    embed.set_field_at(3, name=fieldnamechans1, value=embedcreating)
    await embedcreation.edit(embed=embed)
    embedfield = " "
    
    for voicechans in listvoicechans:
        embedfield += f"{voicechans}\n"
        embed.set_field_at(3, name=fieldnamevoicechans1, value=embedfield)
        await embedcreation.edit(embed=embed)
        await guild.create_voice_channel(name=voicechans, category=discord.utils.get(guild.categories, name=listvoicechans[voicechans]))
  
    embedfield += f"\n{fieldnamevoicechans2}"
    embed.set_field_at(3, name=fieldnamevoicechans1, value=embedfield)
    await embedcreation.edit(embed=embed)
    
    embed.add_field(name=fieldnameroles3, value="Editing roles . . .")
    embed.set_field_at(4, name=fieldnameroles3, value=f"Editing {roledefault}...")
    await embedcreation.edit(embed=embed)
    await roledefault.edit(permissions=discord.Permissions(view_channel=False))
    
    embedfield = f"\n{roledefault} edited\n\n{fieldnameroles4}"
    embed.set_field_at(4, name=fieldnameroles3, value=embedfield)
    await embedcreation.edit(embed=embed)
    
    embed.add_field(name="Completed", value="Template created successfuly!")
    embed.set_field_at(5, name="Creation of template completed successfully", value=f"Template created by request of {context.author} (ID: {context.author.id})")
    await embedcreation.edit(embed=embed)


async def embedtest2(self, context: Context):
    guild = context.message.guild
    roledefault = context.guild.default_role
    await roledefault.edit(permissions=discord.Permissions(view_channel=False))







async def procreatelist1(self, context: Context):
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
            overwriteit = { roledefault: discord.PermissionOverwrite(read_messages=True, connect=True)}
            await cattochange.edit(overwrites=overwriteit)
            #print(f"{roledefault} and cattochange:{cattochange}, {verifiedon}")

        elif proserver[0][catcats] == "verified":
            overwriteit = { roledefault: discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True)}
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
        await guild.create_text_channel(name=chanchans, category=discord.utils.get(guild.categories, name=proserver[1][chanchans]))
    
    embedfield += "\nChannels created"
    embed.set_field_at(2, name=fieldnamechans1, value=embedfield)
    await embedcreation.edit(embed=embed)
    

    
    embed.add_field(name=fieldnameroles3, value="Editing roles . . .")
    embed.set_field_at(3, name=fieldnameroles3, value=f"Editing {roledefault}...")
    await embedcreation.edit(embed=embed)
    await roledefault.edit(permissions=discord.Permissions(view_channel=False))
    
    embedfield = f"\n{roledefault} edited\n\n{fieldnameroles4}"
    embed.set_field_at(3, name=fieldnameroles3, value=embedfield)
    await embedcreation.edit(embed=embed)
    
    embed.add_field(name="Completed", value="Template created successfuly!")
    embed.set_field_at(4, name="Creation of template completed successfully", value=f"Template created by request of {context.author} (ID: {context.author.id})")
    await embedcreation.edit(embed=embed)