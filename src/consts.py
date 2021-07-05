import json
import os
from typing import NamedTuple

from dotenv import load_dotenv

load_dotenv()

PREFIX = os.environ["PREFIX"] or "^"
TOKEN = os.environ["DISCORD_TOKEN"]
MONGO_URI = os.environ["MONGO_URI"]

COGS = ["src.cogs.helpers", "src.cogs.standup"]
#   "src.cogs.help",
#    "src.cogs.goals"]


class Emojis(NamedTuple):
    VERIFY = ""  # TODO: put in a verification emoji(in proper format) here
    CANCEL = ""  # TODO: put in a cancelation emoji(in proper format) here


class Colo:
    purple = 0x5A32E6
    pink = 0xE839B7
    cyan = 0x79F8FB


class Verifiers:
    # temp admin variable for testing.
    # TODO: Set up a config file for getting all the IDs/Roles that can
    # validate/verify the message.
    admin = 558192816308617227


with open("meta.json") as f:
    META = json.load(f)
