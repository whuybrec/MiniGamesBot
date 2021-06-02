import asyncio

from discordbot.utils.emojis import ARROW_LEFT_2, ARROW_RIGHT_2, STOP


class Pager:
    def __init__(self, bot, message, pages, timeout=60.0):
        self.bot = bot
        self.message = message
        self.pages = pages
        self.timeout = timeout
        self.current_page = 0
        self.page_msg = None

    async def show(self):
        if self.page_msg is None:
            self.page_msg = await self.message.channel.send(self.pages[self.current_page])
        else:
            await self.page_msg.edit(content=self.pages[self.current_page])
        await self.page_msg.add_reaction(ARROW_LEFT_2)
        await self.page_msg.add_reaction(ARROW_RIGHT_2)
        await self.page_msg.add_reaction(STOP)

    async def update(self, pages):
        self.pages = pages
        await self.page_msg.edit(content=self.pages[self.current_page])

    async def wait_for_user(self):

        def check(r, u):
            return u == self.message.author \
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
