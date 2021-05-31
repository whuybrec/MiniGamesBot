import asyncio
from discordbot.user.discord_games.minigame_dc import MinigameDisc
from discordbot.user.variables import TIMEOUT, WIN, LOSE, DRAW
from discordbot.utils.emojis import STOP, ALPHABET, SPLIT
from minigames.blackjack import Blackjack


class BlackjackDisc(MinigameDisc):
    def __init__(self, session):
        super().__init__(session)
        self.blackjack = Blackjack()

    async def start(self):
        await self.session.message.edit(content=self.get_content())
        await self.add_reaction(ALPHABET["h"])
        await self.add_reaction(ALPHABET["s"])
        if self.blackjack.can_split():
            await self.add_reaction(SPLIT)
        await self.add_reaction(STOP)
        await self.wait_for_player()

    async def wait_for_player(self):
        def check(r, u):
            return r.message.id == self.session.message.id \
                   and u.id != self.session.message.author.id \
                   and u.id == self.session.context.author.id \
                   and r.emoji in self.emojis

        try:
            while True:
                reaction, user = await self.session.bot.wait_for("reaction_add", check=check, timeout=TIMEOUT)
                if reaction.emoji == STOP:
                    self.status = LOSE
                    break
                elif reaction.emoji == ALPHABET["h"]:
                    if len(self.blackjack.player_hands) == 2:
                        if max(self.blackjack.player_hands[0].get_value()) > 21:
                            self.blackjack.hit(1)
                        else:
                            self.blackjack.hit()
                    else:
                        self.blackjack.hit()
                    await self.session.message.remove_reaction(reaction.emoji, user)
                elif reaction.emoji == ALPHABET["s"]:
                    self.blackjack.stand()
                    await self.clear_reactions()
                    break
                elif reaction.emoji == SPLIT:
                    self.blackjack.split_hand()
                    await self.clear_reaction(SPLIT)
                await self.session.message.edit(content=self.get_content())

                if self.blackjack.is_player_busted():
                    self.blackjack.stand()
                    await self.clear_reactions()
                    break

        except asyncio.TimeoutError:
            self.status = LOSE

        if self.status == -1:
            result = self.blackjack.get_game_result()
            if result == "WIN":
                self.status = WIN
            elif result == "LOSE":
                self.status = LOSE
            elif result == "DRAW":
                self.status = DRAW
        await self.session.message.edit(content=self.get_content())
        await self.end_game()

    def get_content(self):
        content = "```diff\n"
        if self.blackjack.player_turn:
            content += "- Dealer's cards:\n" \
                       f"   {self.blackjack.dealer_hand.cards[0].__str__()}\n" \
                       f"   <hidden card>\n"
        else:
            a, b = self.blackjack.dealer_hand.get_value()
            if a == b:
                content += f"- Dealer's cards: value = {a}\n"
            else:
                content += f"- Dealer's cards: value = {a} or {b}\n"
            for card in self.blackjack.dealer_hand.cards:
                content += f"   {card.__str__()}\n"
        for hand in self.blackjack.player_hands:
            a, b = hand.get_value()
            if a == b:
                content += f"\n+ Player's cards: value = {a}\n"
            else:
                content += f"\n+ Player's cards: value = {a} or {b}\n"
            for card in hand.cards:
                content += f"   {card.__str__()}\n"
        content += "\n"
        if self.status == WIN:
            content += "You have won!\n"
        elif self.status == LOSE:
            content += "You have lost!\n"
        elif self.status == DRAW:
            content += "Game ended in draw!\n"
        content += "```"
        return content
