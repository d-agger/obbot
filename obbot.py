import logging
import os
import discord
from discord.ext import commands

obbot_intents = discord.Intents.default()
obbot_intents.message_content = True
obbot_intents.members = True

prefix = ":obT " if os.getenv("OBBOT_DEBUG") else ":ob "

obbot = commands.Bot(
    command_prefix=prefix,
    intents=obbot_intents
)

@obbot.event
async def on_ready():
    logging.info(f"Online lol")
    

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