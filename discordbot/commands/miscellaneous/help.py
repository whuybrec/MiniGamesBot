import asyncio

import discord

from discordbot.categories.miscellaneous import Miscellaneous
from discordbot.commands.command import Command
from discordbot.utils.emojis import ARROW_UP, ARROW_DOWN, STOP


class HelpCommand(Command):
    bot = None
    name = "help"
    help = "Gives the help message with a list of all commands."
    brief = "Gives the help message."
    args = "*command*"
    category = Miscellaneous

    @classmethod
    async def invoke(cls, context):
        # check if user asked help for specific command
        args = context.message.content[len(cls.bot.prefix) + len(cls.name) + 1:].lstrip()
        if len(args) > 0:
            await cls.extended_help(context, args.split(" ")[0])
            return

        content = cls.get_content(context, 0)
        msg: discord.Message = await context.send(content)
        await msg.add_reaction(ARROW_UP)
        await msg.add_reaction(ARROW_DOWN)
        await msg.add_reaction(STOP)

        await cls.wait_for_reaction(context, msg)

    @classmethod
    async def extended_help(cls, context, command_name):
        if str(context.channel.guild.id) in cls.bot.prefixes.keys():
            prefix = cls.bot.prefixes[str(context.channel.guild.id)]
        else:
            prefix = cls.bot.prefix

        content = ""
        for command in cls.bot.my_commands:
            if command.name == command_name and command.category.has_permission(context.author.id):
                content += "```diff\n" \
                           f"+ {command.category.name}\n" \
                           "```"
                content += f"**{prefix}{command.name}** {command.args}\n" \
                           f"  —  {command.brief}\n" \
                           f"\n{command.help}"
                await context.send(content)
                return

    @classmethod
    async def wait_for_reaction(cls, context, help_msg, page=0):
        while True:
            def check(r, u):
                return u.id == context.message.author.id \
                       and (r.emoji == ARROW_DOWN or r.emoji == ARROW_UP or r.emoji == STOP) \
                       and r.message.id == help_msg.id

            try:
                reaction, user = await cls.bot.wait_for('reaction_add', timeout=60.0, check=check)
                if reaction.emoji == STOP:
                    await help_msg.delete()
                    break

                if reaction.emoji == ARROW_DOWN and page < (len(cls.bot.categories) - 1):
                    new_page = page + 1
                    while not cls.bot.categories[new_page].has_permission(context.author.id):
                        new_page += 1
                        if new_page > (len(cls.bot.categories) - 1):
                            new_page = page
                            break
                    page = new_page
                elif reaction.emoji == ARROW_UP and page > 0:
                    new_page = page - 1
                    while not cls.bot.categories[new_page].has_permission(context.author.id):
                        new_page -= 1
                        if new_page < 0:
                            new_page = page
                            break
                    page = new_page
                content = cls.get_content(context, page)
                await help_msg.edit(content=content)
                await help_msg.remove_reaction(reaction.emoji, user)
            except asyncio.TimeoutError:
                await help_msg.clear_reactions()
                break

    @classmethod
    def get_content(cls, context, page):
        if str(context.channel.guild.id) in cls.bot.prefixes.keys():
            prefix = cls.bot.prefixes[str(context.channel.guild.id)]
        else:
            prefix = cls.bot.prefix

        content = "**__MiniGamesBot__**\n"
        for i in range(len(cls.bot.categories)):
            if not cls.bot.categories[i].has_permission(context.author.id):
                continue
            if page == i:
                content += "```diff\n" \
                           f"+ {cls.bot.categories[i].name}\n" \
                           "```"
                for command in cls.bot.my_commands:
                    if command.category.name == cls.bot.categories[page].name:
                        content += f"**{prefix}{command.name}** {command.args}\n" \
                                   f"  —  {command.brief}\n"
            else:
                content += "```diff\n" \
                           f"- {cls.bot.categories[i].name}\n" \
                           "```"
        content += "\nArguments in *italic*  are optional." \
                   f"\nType **{prefix}help command** for more info on a command."
        return content
