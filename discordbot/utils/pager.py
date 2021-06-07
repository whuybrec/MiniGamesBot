import asyncio
import re

from discordbot.utils.emojis import ARROW_LEFT_2, ARROW_RIGHT_2, STOP


class Pager:
    def __init__(self, bot, context, pages, timeout=60.0):
        self.bot = bot
        self.context = context
        self.pages = pages
        self.timeout = timeout
        self.current_page = 0
        self.page_msg = None

    async def show(self):
        max_length = 1990
        if len(self.pages[self.current_page]) > max_length:
            formatting = False
            if self.pages[self.current_page].startswith("```"):
                formatting = True
            split_contents = re.split(r"\n", self.pages[self.current_page])
            contents = [""]
            for content in split_contents:
                temp = contents[0] + content + "\n"
                if len(temp) > max_length:
                    break
                else:
                    contents[0] = temp
            if formatting:
                contents[0] += "```"
            content = contents[0]
        else:
            content = self.pages[self.current_page]

        if self.page_msg is None:
            self.page_msg = await self.context.send(content)
        else:
            await self.page_msg.edit(content=content)
        await self.page_msg.add_reaction(ARROW_LEFT_2)
        await self.page_msg.add_reaction(ARROW_RIGHT_2)
        await self.page_msg.add_reaction(STOP)

    async def update(self, pages):
        self.pages = pages
        await self.page_msg.edit(content=self.pages[self.current_page])

    async def wait_for_user(self):

        def check(r, u):
            return u == self.context.message.author \
                   and (r.emoji == ARROW_LEFT_2 or r.emoji == ARROW_RIGHT_2 or r.emoji == STOP) \
                   and r.message.id == self.page_msg.id

        while True:
            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=self.timeout, check=check)

                if reaction.emoji == ARROW_LEFT_2:
                    self.current_page -= 1
                    if self.current_page < 0:
                        self.current_page = 0

                elif reaction.emoji == ARROW_RIGHT_2:
                    self.current_page += 1
                    if self.current_page >= len(self.pages):
                        self.current_page = len(self.pages)-1
                else:
                    await self.page_msg.delete()
                    return

                await self.page_msg.remove_reaction(reaction.emoji, user)
                await self.show()
            except asyncio.TimeoutError:
                await self.page_msg.clear_reactions()
                break
