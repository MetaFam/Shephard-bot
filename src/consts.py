import os
import json

from dotenv import load_dotenv
from typing import NamedTuple

load_dotenv()

PREFIX = os.environ['PREFIX'] or '^'
TOKEN = os.environ['DISCORD_TOKEN']
MONGO_URI = os.environ['MONGO_URI']

COGS = [
    "src.cogs.hello_world",
    "src.cogs.standup"]
#   "src.cogs.help",
#    "src.cogs.goals"]


class Emojis(NamedTuple):
    VERIFY = ""  # TODO: put in a verification emoji(in proper format) here
    CANCEL = ""  # TODO: put in a cancelation emoji(in proper format) here


class Colo:
    purple = 0x5a32e6
    pink = 0xe839b7
    cyan = 0x79f8fb


class Verifiers:
    # temp admin variable for testing.
    # TODO: Set up a config file for getting all the IDs/Roles that can
    # validate/verify the message.
    admin = 558192816308617227


with open("meta.json") as f:
    META = json.load(f)
