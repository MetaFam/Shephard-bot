import csv

from datetime import datetime
from typing import Union, Optional, List

from discord import Color, Embed, Member, User
from discord.ext import commands
from discord.ext.commands import Cog
from motor.motor_asyncio import AsyncIOMotorClient as MotorClient

from src.consts import GUILD_ID, MONGO_URI, ACTIVE_ROLE_ID

def get_last_active(last_active):
    date = datetime.fromtimestamp(last_active).strftime("%b-%d-%Y")
    days = (datetime.now() - last_active).days
    return f"Last active on {date} ({days} days ago...)"

def get_xp(self, member: Union[Member, User]):
    return None

class Necromancy(Cog):
    """
    Cog to parse user activity stats from the server.
    And implements tooling for the Nacromancers
    (This is a temporary implementation, and may be shifted to Jergal)
    """
    def __init__(self, bot):
        self.bot = bot
        self.DB = MotorClient(MONGO_URI).players.logs

    @commands.command()
    async def necro(self, ctx: Context, member: Union[Member, User], action: Optional[str]):
        """Command for Necromancy Utilities"""
        if no action:
            await self.get_activity(ctx, member)
        elif (action == "active"):
            await self.get_last_active(ctx, member)
        elif (action == "xp"):
            await ctx.send(
                embed=Embed(
                    description="That action is currently not available",
                    colour=Color.red()
                )
            )
        else:
            await ctx.send(
                embed=Embed(
                    description="That action does not exist(as of _yet_).",
                    color=Color.red()
                )
            )

    async def get_activity(self, ctx: Context, member: Union[Member, User]):
        record = await self.DB_find_one({
            "_id": str(member.id)
        })
        if record:
            stats = f"**Last active**: {get_last_active(record['last_active_at'])}\n\
**Total Message Count**: {record['message_count']}\n\
**XP since last purge**: {get_xp(member)}\n"
            await ctx.send(
                embed=Embed(
                    description=f"Activity stats for {member.mention}\n{stats}",
                    colour=Color.green()
                )
            )
        else:
            await ctx.send(
                embed=Embed(
                    description="There appears to be no instance of this user in the DB.",
                    colour=Color.red()
                )
            )

    async def get_last_active(self, ctx: Context, member: Union[Member, User]):
        record = await self.DB.find_one({
            "_id": str(member.id)
        })
        if record:
            await ctx.send(
                f"{member.mention} was {get_last_active(record['last_active'])}"
            )
        else:
            await ctx.send(
                embed=Embed(
                    description="There appears to be no instance of this user in the DB.",
                    colour=Color.red()
                )
            )

    async def update_status(
        self,
        member_id: str,
        created_at: datetime,
        status: List[str]):
        try:
            record = await self.DB.find_one({'_id': member_id})
            if record:
                await self.DB.update_one(
                    record,
                    {
                        "$set": {
                            "status": status
                        }
                    }
                )
            else:
                await self.DB.insert_one({
                    "_id": member_id,
                    "status": status,
                    "message_count": 0,
                    "xp": 0,
                    "last_active": created_at
                })
        except Exception as e:
            print("ERROR - {e}")



    @commands.has_role("Necromancer")
    @commands.command(aliases=["fallen"])
    async def slay(self, ctx: Context, member: Union[Member, User], *, reason: Optional[str]):
        try:
            active_role = ctx.guild.get_role(ACTIVE_ROLE_ID)
            await member.remove_roles(
                active_role,
                reason=reason,
                atomic=True
            )

            await self.update_status(
                member.id,
                ctx.guild.created_at,
                ["fallen", f"Reason- {reason}"]
            )
        except Exception as e:
            print(e)
            await ctx.send(f"Some error occured\n{e}")

    @commands.has_role("Necromancer")
    @commands.command(aliases=["chosen"])
    async def promote(self, ctx: Context, member: Union[Member, User], *, reason: Optional[str]):
        try:
            active_role = ctx.guild.get_role(ACTIVE_ROLE_ID)
            await member.add_roles(
                active_role,
                reason=reason,
                atomic=True
            )

            await self.update_status(
                member.id,
                ctx.guild.created_at,
                ["fallen", f"Reason- {reason}"]
            )
        except Exception as e:
            print(e)
            await ctx.send(f"Some error occured\n{e}")

def setup(bot):
    bot.add_cog(Necromany(bot))
