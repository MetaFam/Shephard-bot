import json
import os
from typing import NamedTuple

from dotenv import load_dotenv

load_dotenv()

PREFIX = os.getenv("PREFIX") or "^"
TOKEN = os.getenv("DISCORD_TOKEN") or "foo"
MONGO_URI = os.getenv("MONGO_URI") or "bar"
GUILD_ID = int(os.getenv("DISCORD_GUILD_ID") or "629411177947987986")

COGS = ["src.commands.helpers", "src.commands.standup", "src.tasks.reminder"]
#   "src.cogs.help",
#    "src.cogs.goals"]

VERIFIER_ROLES = [
    665574957094535199,
    659519940159602746,
    659519668553252864,
    659518696506785802,
    814464073386426389,
]


class Emojis(NamedTuple):
    VERIFY = "👍"  # TODO: put in a verification emoji(in proper format) here
    CANCEL = ""  # TODO: put in a cancelation emoji(in proper format) here


class Colo:
    purple = 0x5A32E6
    pink = 0xE839B7
    cyan = 0x79F8FB


with open("meta.json") as f:
    META = json.load(f)
