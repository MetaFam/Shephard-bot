from src.consts import MONGO_URI

from discord import Embed, Color
from discord.ext import commands
from discord.ext.commands import Context, Cog, Converter

from motor.motor_asyncio import AsyncIOMotorClient as MotorClient
from datetime import datetime


class Formatter(Converter):
    async def convert(self, ctx: Context, tasks: str):
        data = {
            "approved": False,
            "date_reported": ctx.message.created_at.timestamp(),
            "last_edited": ctx.message.created_at.timestamp(),
        }
        data["tasks"] = tasks.split('\n')
        return data


class Standup(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DB = MotorClient(MONGO_URI).players.tasks

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def standup(self, ctx: Context, *, content):
        """Standup Commands Group. Stores tasks from standup messages"""
        await self.create(ctx, content)

    @standup.command()
    async def create(self, ctx: Context, *, tasks: Formatter):
        """Command for creating standups and storing tasks"""
        record = await self.DB.find_one(
            {"_id": str(ctx.author.id)}
        )

        if record:
            data = record['data'] + tasks
            await self.DB.update_one(
                record,
                {
                    "$set": {
                        "data": data
                    }
                }
            )
        else:
            self.DB.insert_one(
                {
                    "_id": str(ctx.author.id),
                    "alerts": True,
                    "data": [
                        tasks
                    ]
                }
            )
        tasks = '\n'.join(tasks['tasks'])
        await ctx.author.send(f"Successfully submitted your tasks:\n{tasks}")

    @standup.command()
    async def log(self, ctx: Context):
        """Command for showing latest standup"""
        record = await self.DB.find_one({"_id": str(ctx.author.id)})
        if record:
            data = record['data'][-1]
            tasks = '\n'.join(data['tasks'])
            embed = Embed(
                title="Standup Log",
                description=f"Your latest reported tasks -\n{tasks}",
                color=Color.green()
            )
            embed.add_field(
                name="Date Added",
                value="%s UTC" % datetime.fromtimestamp(
                    data['date_reported']).strftime("%b-%d-%Y %H:%M")
            )
            embed.add_field(
                name="Status",
                value="Verified" if data['approved'] else "Unapproved"
            )
        else:
            embed = Embed(
                title="It looks like there is no record of you or your tasks",
                color=Color.red()
            )
        await ctx.send(embed=embed)

    @standup.command()
    @commands.dm_only()
    async def edit(self, ctx: Context, *, content: str = None):
        """Command for editing latest standup"""
        if not content:
            await ctx.send(
                embed=Embed(
                    description="Content not specified. Reuse the command with all the tasks that you'd like to replace the old tasks with\n",
                    color=Color.red()
                )
            )
            await self.log(ctx)
        else:
            record = await self.DB.find_one({"_id": str(ctx.author.id)})
            if record:
                embed = Embed(
                    description="The relevant edits have been made to the record of your tasks",
                    color=Color.green())

                data = record['data']
                data[-1] = {
                    "approved": False,
                    "date_reported": data[-1]["date_reported"],
                    "last_edited": datetime.now().timestamp,
                    "tasks": content.split('\n')
                }

                await self.DB.update_one(
                    record,
                    {
                        "$set": {
                            "data": data
                        }
                    }
                )
            else:
                embed = Embed(
                    description="No previous instance or tasks were found for you. A new record has been created with the tasks mentioned.",
                    color=Color.gold())
                await ctx.create(ctx, content)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Standup(bot))
