from discord.ext import commands, tasks
from discord.ext.commands import Context, Cog

class Testing(Cog):
    """Help command and some other helper commands"""
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print('Bot is online!')

    @commands.command()
    async def ping(self, ctx: Context):
        await ctx.send('Pong!')

def setup(bot):
    bot.add_cog(Testing(bot))
