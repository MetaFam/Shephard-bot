from discord.ext import commands
from discord.ext.commands import Cog, Context

from src.consts import META


class Testing(Cog):
    """Help command and some other helper commands"""

    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print("Bot is online! Currently running version - v%s" % META["version"])

    @commands.command()
    async def ping(self, ctx: Context):
        await ctx.send("Pong! Running version - v%s" % META["version"])

    @commands.command()
    async def pong(self, ctx: Context):
        await ctx.send(f"{ctx.author}, {ctx.message.content}, {ctx.message.id}")


def setup(bot):
    bot.add_cog(Testing(bot))
