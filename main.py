import os
import sys
import re
import datetime
import asyncio
import json

import discord
from discord.ext import commands, tasks
import aiohttp
import asyncpg


async def _get_prefix(bot, message):
    return ["?", "!"]

bot = commands.Bot(command_prefix=["?", "!"])


@bot.event
async def on_ready():
    print("Bot is now ONLINE.\n"
          f"Logged in as {bot.user},\n"
          f"ID: {bot.user.id}\n"
          f"UTCTime: {datetime.datetime.utcnow()}")


# Custom check for bot collaborators only.
async def is_creators(ctx):
    return ctx.author.id in (586790522157531136, 398035250648711169, 645570536138735618)


def manage_exts(ext, mode):
    with open("data/cogs.json") as file:
        data = json.load(file)

    if mode == 1:
        data["cogs"].append(ext)

    elif mode == 2:
        data["cogs"].remove(ext)

    with open("data/cogs.json", "w") as file:
        json.dump(data, file, indent=2)


@bot.command()
@commands.check(is_creators)
async def loadcog(ctx, cogname):
    bot.load_extension(f"plugins.{cogname}")
    # manage_exts(cogname, 1)
    await ctx.message.add_reaction("\U0001f44c")


@bot.command()
@commands.check(is_creators)
async def unloadcog(ctx, cogname):
    bot.unload_extension(f"plugins.{cogname}")
    # manage_exts(cogname, 2)
    await ctx.message.add_reaction("\U0001f44c")


@bot.command()
@commands.check(is_creators)
async def reloadcog(ctx, cogname):
    bot.reload_extension(f"plugins.{cogname}")
    await ctx.message.add_reaction("\U0001f44c")


# with open("data/cogs.json") as file:
#     data = json.load(file)
#     exts_to_load = data["cogs"]
#
#     for ext in exts_to_load:
#         bot.load_extension(f"plugins.{ext}")

for ext in os.listdir("./plugins"):
    if ext.endswith(".py") and ext != "__init__.py":
        bot.load_extension(f"plugins.{ext[:-3]}")


with open("token.txt") as file:
    token = file.read()

bot.run(token)
#bot.run(os.getenv('vghsToken'))
