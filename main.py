import os
import sys
import re
import datetime
import asyncio

import discord
from discord.ext import commands, tasks
import aiohttp
import asyncpg


async def _get_prefix(bot, message):
    pass  # Do something here to get prefix.

bot = commands.Bot(command_prefix=_get_prefix)


@bot.event
async def on_ready():
    print("Bot is now ONLINE.\n"
          f"Logged in as {bot.user},\n"
          f"ID: {bot.user.id}\n"
          f"UTCTime: {datetime.datetime.utcnow()}")


# Custom check for bot collaborators only.
async def is_creators(ctx):
    return ctx.author.id in (586790522157531136, 398035250648711169, 645570536138735618)


@bot.command()
@commands.check(is_creators)
async def loadcog(ctx, cogname):
    pass


bot.run("abc")
