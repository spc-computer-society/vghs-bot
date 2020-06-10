from discord.ext import commands


class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, limit: int = 5):
        await ctx.channel.purge(limit=limit + 1)
        await ctx.send("Bye!", delete_after=2)

    @clear.error
    async def clear_error(self, ctx, err):
        if isinstance(err, commands.BadArgument):
            await ctx.send("Limit must be an integer!")
        elif isinstance(err, commands.MissingPermissions):
            await ctx.send("Sorry, permission denied!")
        else:
            await ctx.send("An error occurred while trying to do that!\n"
                           f"{err}")


def setup(bot):
    bot.add_cog(Clear(bot))
