from discord import Intents
from discord.ext import commands

from . import consts


class Bot(commands.Bot):
    """Bot Initializer class"""

    def __init__(self):
        intents = Intents.default()
        intents.members = True
        intents.reactions = True

        super().__init__(
            command_prefix=consts.PREFIX, case_insensitive=True, intents=intents
        )

    def load_cogs(self):
        """Load all the cogs for the bot"""
        for cog in consts.COGS:
            self.load_extension(cog)
            print(f"Loaded cog: {cog}")

    def run(self):
        """Run the Bot"""
        self.load_cogs()
        if (consts.TOKEN is None) or (consts.TOKEN == ""):
            raise EnvironmentError(
                "Empty Token or No Token provided in the .env config"
            )
        if (consts.MONGO_URI is None) or (consts.MONGO_URI == ""):
            raise EnvironmentError("No Mongo URI found. Can't connect to database.")
        if consts.TOKEN == "foo":
            print("No token loaded, cog-loading completed")
            return
        super().run(consts.TOKEN)
