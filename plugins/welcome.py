import random

from discord.ext import commands


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        messages = [f"Welcome {member.mention} to VGHS esports!",
                    f"Greetings {member.mention}! Have a nice day!",
                    f"Beware! Glorious {member.mention} has appeared!"]
        await member.guild.text_channels[0].send(random.choice(messages))


def setup(bot):
    bot.add_cog(Welcome(bot))
