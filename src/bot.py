import os

from discord import Intents
from discord.ext import commands

from . import consts


class Bot(commands.Bot):
    """Bot Initializer class"""

    def __init__(self):
        intents = Intents.default()
        intents.members = True

        super().__init__(command_prefix=consts.PREFIX,
                       case_insensitive=True,
                       intents=intents)
        self.load_cogs()

    def load_cogs(self):
        """Load all the cogs for the bot"""
        for cog in consts.COGS:
            self.load_extension(cog)


    def run(self):
        """Run the Bot"""
        if (consts.TOKEN is None) or (consts.TOKEN == ""):
            raise EnvironmentError("Empty Token or No Token provided in the .env config")
        super().run(consts.TOKEN)


