from discord.ext import commands


class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def clear(self, ctx, limit: int = 5):
        await ctx.channel.purge(limit=limit + 1)
        await ctx.send("Bye!")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, err):
        await ctx.send("An error occurred while trying to do that!")