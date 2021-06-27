from discordbot.managers.messagemanager import MessageManager
from discordbot.discordminigames.singleplayergames.singleplayergame import SinglePlayerGame, WON, LOST, QUIT, DRAW
from discordbot.utils.emojis import STOP, ALPHABET, SPLIT
from minigames.blackjack import Blackjack


class BlackjackDiscord(SinglePlayerGame):
    def __init__(self, session):
        super().__init__(session)
        self.blackjack = Blackjack()

    async def start_game(self):
        await MessageManager.edit_message(self.message, self.get_board())

        await MessageManager.add_reaction_and_event(self.message, ALPHABET["h"], self.player.id, self.on_hit_reaction)
        await MessageManager.add_reaction_and_event(self.message, ALPHABET["s"], self.player.id, self.on_stand_reaction)

        if self.blackjack.can_split():
            await MessageManager.add_reaction_and_event(self.message, SPLIT, self.player.id, self.on_split_reaction)
        await MessageManager.add_reaction_and_event(self.message, STOP, self.player.id, self.on_quit_game)

    async def on_hit_reaction(self):
        self.on_start_move()

        if len(self.blackjack.player_hands) == 2:
            if max(self.blackjack.player_hands[0].get_value()) > 21:
                self.blackjack.hit(hand=1)
            else:
                self.blackjack.hit()
        else:
            self.blackjack.hit()

        await MessageManager.edit_message(self.message, self.get_board())
        await MessageManager.remove_reaction(self.message, ALPHABET["h"], self.player.member)
        await MessageManager.clear_reaction(self.message, SPLIT)

        if self.blackjack.is_player_busted():
            await self.stand()

    async def on_stand_reaction(self):
        self.on_start_move()
        await self.stand()

    async def on_split_reaction(self):
        self.on_start_move()

        self.blackjack.split_hand()
        await MessageManager.clear_reaction(self.message, SPLIT)
        await MessageManager.edit_message(self.message, self.get_board())

    async def stand(self):
        self.blackjack.stand()
        if self.blackjack.has_ended_in_draw():
            await self.game_draw()
        elif self.blackjack.has_player_won():
            await self.game_won()
        else:
            await self.game_lost()

    def get_board(self):
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

        if self.game_state == WON:
            content += "You have won!\n"
        elif self.game_state == DRAW:
            content += "Game ended in draw!\n"
        elif self.game_state == LOST or self.game_state == QUIT:
            content += "You have lost!\n"
        content += "```"
        return content
