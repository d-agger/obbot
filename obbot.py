import logging
import os
import re

import discord
from discord.ext import commands

from keys import ObKeys
from strings import ObStrings

obbot_intents = discord.Intents.default()
obbot_intents.message_content = True
obbot_intents.members = True

IS_DEV = os.getenv("OBBOT_DEV")
prefix = ":od " if IS_DEV else ":ob "

obbot = commands.Bot(
    command_prefix=prefix,
    intents=obbot_intents
)

"""
------------------------------------------------------------------------------------------------------------------------
Checks
"""

@obbot.check
async def restrict_guilds(ctx):
    if ctx.guild is None:
        return False
    return ctx.guild.id in ObKeys().ALLOWED_GUILDS["dev" if IS_DEV else "prod"]

"""
------------------------------------------------------------------------------------------------------------------------
Events
"""

@obbot.event
async def on_ready():
    logging.info(f"Online lol")

@obbot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send(ObStrings().ERROR_GUILD_NOT_ALLOWED())


"""
------------------------------------------------------------------------------------------------------------------------
General commands
"""
    
@obbot.command()
async def kys(ctx):
    logging.info(f"Kys check")
    await ctx.send(f"kys {ctx.author.mention}")

@obbot.command()
async def dziad(ctx):
    await ctx.send(f"https://cdn.discordapp.com/emojis/1280080611251458090.webp")