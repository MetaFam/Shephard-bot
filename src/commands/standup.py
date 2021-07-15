from datetime import datetime

from discord import Color, Embed, RawReactionActionEvent
from discord.ext import commands
from discord.ext.commands import Cog, Context
from motor.motor_asyncio import AsyncIOMotorClient as MotorClient

from src.consts import GUILD_ID, MONGO_URI


def formatted(ctx: Context, tasks: str):
    data = {
        "approved": False,
        "date_reported": ctx.message.created_at.timestamp(),
        "last_edited": ctx.message.created_at.timestamp(),
    }
    data["tasks"] = tasks.split("\n")
    return data


class Standup(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DB = MotorClient(MONGO_URI).players.tasks

    @Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        if payload.guild_id == GUILD_ID and payload.emoji.name == "👍":
            record = await self.DB.find_one({"message": str(payload.message_id)})
            if record:
                field = f"data.{len(record['data']) - 1}.approved"
                await self.DB.update_one(record, {"$set": {field: True}})
                channel = self.bot.get_channel(payload.channel_id)
                await channel.send("Your tasks just got verified")

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def standup(self, ctx: Context, *, content: str):
        """Standup Commands Group. Stores tasks from standup messages"""
        await self.create(ctx, tasks=content)

    @standup.command()
    async def create(self, ctx: Context, *, tasks: str):
        """Command for creating standups and storing tasks"""
        record = await self.DB.find_one({"_id": str(ctx.author.id)})

        tasks = formatted(ctx, tasks)

        if record:
            data = record["data"] + [tasks]
            await self.DB.update_one(
                record, {"$set": {"message": str(ctx.message.id), "data": data}}
            )
        else:
            self.DB.insert_one(
                {
                    "_id": str(ctx.author.id),
                    "alerts": True,
                    "message": str(ctx.message.id),
                    "data": [tasks],
                }
            )
        tasks = "\n".join(tasks["tasks"])
        await ctx.author.send(f"Successfully submitted your tasks:\n{tasks}")

    @standup.command()
    async def log(self, ctx: Context):
        """Command for showing latest standup"""
        record = await self.DB.find_one({"_id": str(ctx.author.id)})
        if record:
            data = record["data"][-1]
            tasks = "\n".join(data["tasks"])
            embed = Embed(
                title="Standup Log",
                description=f"Your latest reported tasks -\n{tasks}",
                color=Color.green(),
            )
            embed.add_field(
                name="Date Added",
                value="%s UTC"
                % datetime.fromtimestamp(data["date_reported"]).strftime(
                    "%b-%d-%Y %H:%M"
                ),
            )
            embed.add_field(
                name="Status", value="Verified" if data["approved"] else "Unapproved"
            )
        else:
            embed = Embed(
                title="It looks like there is no record of you or your tasks",
                color=Color.red(),
            )
        await ctx.send(embed=embed)

    @standup.command()
    @commands.dm_only()
    async def edit(self, ctx: Context, *, content: str = None):
        """Command for editing latest standup"""
        if not content:
            await ctx.send(
                embed=Embed(
                    description="Content not specified.\n\
Reuse the command with all the tasks that you'd like to replace the old tasks with",
                    color=Color.red(),
                )
            )
            await self.log(ctx)
        else:
            record = await self.DB.find_one({"_id": str(ctx.author.id)})
            if record:
                embed = Embed(
                    description="The relevant edits have been made to the record of your tasks",
                    color=Color.green(),
                )

                field = len(record["data"]) - 1

                await self.DB.update_one(
                    record,
                    {
                        "$set": {
                            f"data.{field}.approved": False,
                            f"data.{field}.last_edited": datetime.now().timestamp(),
                            f"data.{field}.tasks": content.split("\n"),
                        }
                    },
                )
            else:
                embed = Embed(
                    description="No previous records found. A new record with these tasks has been created.",
                    color=Color.gold(),
                )
                await ctx.create(ctx, content)
            await ctx.send(embed=embed)

    @commands.command(hidden=True, aliases=["alerts", "reminder", "reminders"])
    async def alert(self, ctx: Context, action: str = "toggle"):
        """Auxiliary Command that toggles alert status"""
        await self.alerts(ctx, action)

    @standup.command(aliases=["alert", "reminder", "reminders"])
    async def alerts(self, ctx: Context, action: str = "toggle"):
        """Command for toggling alert status"""
        record = await self.DB.find_one({"_id": str(ctx.author.id)})
        action = action.lower() if action.lower() in ["on", "off"] else "toggle"
        if record:
            if action == "toggle":
                action = "off" if record["alerts"] else "on"
            if action == "on":
                await self.DB.update_one(record, {"$set": {"alerts": True}})
            if action == "off":
                await self.DB.update_one(record, {"$set": {"alerts": False}})
            await ctx.send(f"Weekly reminders(alerts) are now `{action}`")
        else:
            await ctx.send(
                "Error: There are no records found for you\n_'Perhaps the Archives Are Incomplete'_."
            )


def setup(bot):
    bot.add_cog(Standup(bot))
