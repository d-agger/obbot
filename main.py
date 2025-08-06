import logging
from keys import Keys
import logs
import discord
from discord.ext import commands

token = Keys().OBBOT_TOKEN
log_handler = logs.obbot_log_handler

obbot_intents = discord.Intents.default()
obbot_intents.message_content = True
obbot_intents.members = True

obbot = commands.Bot(command_prefix="ob$ ", intents=obbot_intents)

@obbot.event
async def on_ready():
    logging.debug(f"Online lol")
    
@obbot.command()
async def kys(ctx):
    await ctx.send(f"kys {ctx.author.mention}")

@obbot.command()
async def dziad(ctx):
    await ctx.send(f"https://cdn.discordapp.com/emojis/1280080611251458090.webp")


obbot.run(
    token, 
    log_handler=log_handler,
    log_level=logging.DEBUG
)