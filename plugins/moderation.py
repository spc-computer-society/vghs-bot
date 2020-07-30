import discord
from discord.ext import commands

import datetime

from typing import Union


MOD_LOG_CHANNEL_ID = 738293621610250241


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mod_who_did_it = None
        self.reason = None
        self.time = None

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)

        if not reason:
            reason = "..."

        embed = discord.Embed(title="A member as been kicked!",
                              description=f"{member.mention} has been kicked from the server!",
                              color=0xd6000d)

        embed.add_field(name="Reason",
                        value=reason,
                        inline=False)

        self.mod_who_did_it = ctx.author
        self.reason = reason
        self.time = datetime.datetime.utcnow()

        await ctx.send(embed=embed)
        await ctx.message.add_reaction("\U0001f44c")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)

        if not reason:
            reason = "..."

        embed = discord.Embed(title="A member as been banned!",
                              description=f"{member.mention} has been banned from the server!",
                              color=0xd6000d)

        embed.add_field(name="Reason",
                        value=reason,
                        inline=False)

        self.mod_who_did_it = ctx.author
        self.reason = reason
        self.time = datetime.datetime.utcnow()

        await ctx.send(embed=embed)
        await ctx.message.add_reaction("\U0001f44c")

    @commands.command()
    async def userinfo(self, ctx, member: Union[discord.Member, discord.User] = None):
        if isinstance(member, discord.Member):
            embed = discord.Embed(title=f"User: {member}",
                                  description=f"User in current guild: True")

            embed.set_thumbnail(url=str(member.avatar_url))

            embed.add_field(name="Username",
                            value=member.name,
                            inline=True)
            embed.add_field(name="Tag",
                            value=member.discriminator)
            embed.add_field(name="Nickname",
                            value=str(member.nick))

            embed.add_field(name="Joined the server",
                            value=member.joined_at.strftime("%Y %m %d %H:%M:%S"),
                            inline=True)
            embed.add_field(name="Created account",
                            value=member.created_at.strftime("%Y %m %d %H:%M:%S"))

            roles = member.roles.reverse()
            output_roles = []
            for index, role in enumerate(roles):
                if index > 2:
                    break
                output_roles.append(role)

            embed.add_field(name="Top roles",
                            value=", ".join([role.mention for role in output_roles]),
                            inline=True)

            embed.add_field(name="Is a bot",
                            value=str(member.bot),
                            inline=False)

            embed.add_field(name="Has nitro:",
                            value=str((await member.profile()).premium))

        elif isinstance(member, discord.User):
            embed = discord.Embed(title=f"User: {member}",
                                  description=f"User in current guild: False")

            embed.set_thumbnail(url=str(member.avatar_url))

            embed.add_field(name="Username",
                            value=member.name,
                            inline=True)
            embed.add_field(name="Tag",
                            value=member.discriminator)

            embed.add_field(name="Created account",
                            value=member.created_at.strftime("%Y %m %d %H:%M:%S"))

            embed.add_field(name="Is a bot",
                            value=str(member.bot),
                            inline=False)

            embed.add_field(name="Has nitro:",
                            value=str((await member.profile()).premium))

        else:
            return await ctx.send("User not found. Please note that the bot cannot see users that do not share a server.")

        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        embed = discord.Embed(title="Action: Ban",
                              description=f"Banned User: {user.mention}",
                              color=0x000000)

        embed.add_field(name="Mod",
                        value=self.mod_who_did_it.mention,
                        inline=True)

        embed.add_field(name="Reason",
                        value=self.reason,
                        inline=True)

        channel = self.bot.get_channel(MOD_LOG_CHANNEL_ID)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_kick(self, guild, user):
        embed = discord.Embed(title="Action: Kick",
                              description=f"Kicked User: {user.mention}",
                              color=0x000000)

        embed.add_field(name="Mod",
                        value=self.mod_who_did_it.mention,
                        inline=True)

        embed.add_field(name="Reason",
                        value=self.reason,
                        inline=True)

        embed.set_footer(text=f"{self.time.strftime('%Y %m %d %H:%M:%S')} UTC")

        channel = self.bot.get_channel(MOD_LOG_CHANNEL_ID)
        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))

