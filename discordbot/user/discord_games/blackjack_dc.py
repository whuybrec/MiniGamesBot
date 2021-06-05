import asyncio

from discordbot.user.discord_games.minigame_dc import MinigameDisc
from discordbot.utils.variables import TIMEOUT, WIN, LOSE, DRAW
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

    async def on_reaction(self, reaction, user):
        if reaction.emoji == ALPHABET["h"]:
            if len(self.blackjack.player_hands) == 2:
                if max(self.blackjack.player_hands[0].get_value()) > 21:
                    self.blackjack.hit(hand=1)
                else:
                    self.blackjack.hit()
            else:
                self.blackjack.hit()
            await self.session.message.remove_reaction(reaction.emoji, user)
        elif reaction.emoji == ALPHABET["s"]:
            self.stand()
        elif reaction.emoji == SPLIT:
            self.blackjack.split_hand()

        if SPLIT in self.emojis:
            await self.clear_reaction(SPLIT)

        if self.blackjack.is_player_busted():
            self.stand()
        await self.session.message.edit(content=self.get_content())

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
        if not self.playing:
            if len(self.winners) == 1:
                content += "You have won!\n"
            elif len(self.losers) == 1:
                content += "You have lost!\n"
            elif len(self.drawers) == 1:
                content += "Game ended in draw!\n"
        content += "```"
        return content

    def stand(self):
        self.blackjack.stand()
        if self.blackjack.has_ended_in_draw():
            self.drawers.append(self.players[0])
        elif self.blackjack.has_player_won():
            self.winners.append(self.players[0])
        else:
            self.losers.append(self.players[0])
        self.playing = False
