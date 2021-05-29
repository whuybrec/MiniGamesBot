import asyncio
import discord
from ..command import Command
from discordbot.categories.miscellaneous import Miscellaneous
from discordbot.emojis import *


class HelpCommand(Command):
    bot = None
    name = "help"
    help = "Displays the help message with a list of all commands."
    brief = "Gives this message."
    args = ""
    category = Miscellaneous

    @classmethod
    async def handler(cls, context, *args):
        # check if user asked help for specific command
        if args:
            await cls.extended_help(context, args[0])
            return

        content = cls.get_content(context, 0)
        msg: discord.Message = await context.message.channel.send(content)
        await msg.add_reaction(ARROW_UP)
        await msg.add_reaction(ARROW_DOWN)

        await cls.wait_for_reaction(context, msg)

    @classmethod
    async def extended_help(cls, context, command_name):
        content = ""
        for command in cls.bot.my_commands:
            if command.name == command_name and command.category.has_permission(context.author.id):
                content += "```diff\n" \
                           f"+ {command.category.name}\n" \
                           "```"
                content += f"**{cls.bot.prefix}{command.name}** {command.args}\n" \
                           f"  —  {command.brief}\n" \
                           f"\n{command.help}"
                await context.message.channel.send(content)
                return

    @classmethod
    async def wait_for_reaction(cls, context, help_msg, page=0):
        while True:
            def check(r, u):
                return u == context.message.author and (r.emoji == ARROW_DOWN or r.emoji == ARROW_UP)
            try:
                reaction, user = await cls.bot.wait_for('reaction_add', timeout=60.0, check=check)

                if reaction.emoji == ARROW_DOWN and page < (len(cls.bot.categories)-1):
                    new_page = page + 1
                    while not cls.bot.categories[new_page].has_permission(context.author.id):
                        new_page += 1
                        if new_page > (len(cls.bot.categories)-1):
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
                await help_msg.clear_reaction(ARROW_UP)
                await help_msg.clear_reaction(ARROW_DOWN)
                break

    @classmethod
    def get_content(cls, context, page):
        content = "```fix\nMiniGamesBot```"
        for i in range(len(cls.bot.categories)):
            if not cls.bot.categories[i].has_permission(context.author.id):
                continue
            if page == i:
                content += "```diff\n" \
                           f"+ {cls.bot.categories[i].name}\n" \
                           "```"
                for command in cls.bot.my_commands:
                    if command.category.name == cls.bot.categories[page].name:
                        content += f"**{cls.bot.prefix}{command.name}** {command.args}\n" \
                                   f"  —  {command.brief}\n"
            else:
                content += "```diff\n" \
                           f"- {cls.bot.categories[i].name}\n" \
                           "```"
        return content
