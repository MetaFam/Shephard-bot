from discord import Embed
from discord.ext import commands
from discord.ext.commands import Cog, Context

from src.consts import META, Colo


def HelpEmbed(title="Help", description="\u200b"):
    return Embed(title=title, description=description, color=Colo.purple)


class CustomHelpCommand(commands.HelpCommand):
    def get_cmd_usage(self, command):
        cmd = "%s%s %s" % (self.clean_prefix, command.qualified_name, command.signature)
        return f"`{cmd.strip()}`"

    def get_help_text(self, command):
        usage = self.get_cmd_usage(command)
        return usage, command.short_doc

    async def send_bot_help(self, mapping):
        embed = HelpEmbed()
        for cog, cmds in mapping.items():
            filtered_cmds = await self.filter_commands(cmds, sort=True)
            cmd_data = [self.get_cmd_usage(cmd) for cmd in filtered_cmds]
            if cmd_data:
                cog_name = getattr(cog, "qualified_name", "No Category")
                cmd_data = "\n".join(cmd_data)
                embed.add_field(
                    name=cog_name, value=f"{cog.description}\n{cmd_data}", inline=False
                )
        await self.context.send(embed=embed)

    async def send_command_help(self, command):
        embed = HelpEmbed(title=self.get_cmd_usage(command))
        embed.add_field(name="Help for `{command.name}`", value=command.short_doc)
        aliases = command.aliases
        if aliases:
            embed.add_field(name="Aliases", value=", ".join(aliases), inline=False)
        await self.context.send(embed=embed)

    async def send_group_help(self, group):
        embed = HelpEmbed()
        await self.context.send(embed=embed)

    async def send_cog_help(self, cog):
        cog_name = getattr(cog, "qualified_name", "No Category")
        embed = HelpEmbed(
            f"Help for Category: `{cog_name}`",
            f"Use `^help command` for more info on a command\n\n{cog.description}",
        )
        cmds = [
            self.get_help_text(c)
            for c in await self.filter_commands(cog.walk_commands(), sort=True)
        ]
        if cmds:
            for cmd in cmds:
                embed.add_field(
                    name=cmd[0], value=f"{cog.description}{cmd[1]}", inline=False
                )
        await self.context.send(embed=embed)


class Helpers(Cog):
    """Help command and some other helper commands"""

    def __init__(self, bot):
        bot._default_help_command = bot.help_command
        bot.help_command = CustomHelpCommand()
        bot.help_command.cog = self
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        print("Bot is online! Currently running version - v%s" % META["version"])

    @commands.command()
    async def ping(self, ctx: Context):
        await ctx.send("Pong! Running version - v%s" % META["version"])


def setup(bot):
    bot.add_cog(Helpers(bot))
