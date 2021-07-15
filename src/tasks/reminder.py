from datetime import datetime

from discord import Color, Embed
from discord import Member, User
from discord import Forbidden

from discord.ext import tasks
from discord.ext.commands import Cog
from motor.motor_asyncio import AsyncIOMotorClient as MotorClient

from src.consts import MONGO_URI, GUILD_ID
from typing import Union

reminder_text = "Don't forget to report your weekly progress in `#champion-ring`.\n\
You can do so by using the `^standup` command. Usage example-\n\
```\n\
^standup\n\
I did something. It accomplished that.\n\
I also did this, and it helped us do that.```"


def is_saturday():
    return datetime.utcnow().date().weekday() == 5


# helper function to render Embed object for reminder
def reminder_embed(member: Union[Member, User]) -> Embed:
    return Embed(
        title="Reminder for weekly standup",
        description=f"Hey, {member.mention}\n{reminder_text}",
        color=Color.gold(),
        timestamp=datetime.utcnow()
    ).set_footer(text="To opt out of these alerts, use the `^standup alerts` command")


class Reminder(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.DB = MotorClient(MONGO_URI).players.tasks
        self.weekly_reminder.start()

    @tasks.loop(hours=24.0)
    async def weekly_reminder(self):
        """Sends people a weekly reminder on every Saturday, to submit standups"""
        if is_saturday():
            print('Saturday: Sending members reminder alerts')
            guild = self.bot.get_guild(GUILD_ID)
            async for member in self.DB.find({"alerts": True}, {"data": 0}):
                try:
                    member = guild.get_member(int(member['_id']))
                    await member.send(embed=reminder_embed(member))
                except Forbidden:
                    print(f"Can't DM member: {member}")

    @weekly_reminder.before_loop
    async def before_weekly_reminder(self):
        print("Setting up Weekly Reminder Task")
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(Reminder(bot))
