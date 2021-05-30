import pydealer

from discordbot.user.variables import Variables
from minigames.Minigames.minigame import MiniGame


class BlackJack(MiniGame):
    def __init__(self, bot, game_name, msg, player_id):
        super().__init__(bot, game_name, msg, player_id)
        self.deck = None
        self.hand_player_1 = None
        self.hand_player_2 = None
        self.hand_bank = None

    async def start_game(self):
        await self.init_var()

        if self.hand_player_1.has_blackjack():
            if self.hand_bank.has_blackjack():
                await self.player_drew()
                return
            await self.player_won()
            return

        await self.msg.edit(content=self.get_board())

        if self.hand_player_1.is_splittable():
            await self.msg.add_reaction(Variables.SPLIT_EMOJI)

        await self.msg.add_reaction(Variables.INC_EMOJI1)
        await self.msg.add_reaction(Variables.STOP_EMOJI)

        await self.wait_for_player()

    async def update_game(self, reaction, user):
        if self.terminated:
            return

        if reaction.emoji == Variables.INC_EMOJI1:
            self.hand_player_1.get_card()

        elif reaction.emoji == Variables.INC_EMOJI2:
            self.hand_player_2.get_card()

        elif reaction.emoji == Variables.STOP_EMOJI:
            await self.bank_plays()
            await self.has_player_won()
            return

        elif reaction.emoji == Variables.SPLIT_EMOJI:
            self.player_split()
            await self.msg.add_reaction(Variables.INC_EMOJI2)

        points_player = self.hand_player_1.get_points()
        if points_player[0] > 21:
            self.hand_player_1.busted = True
            await reaction.message.clear_reaction(Variables.INC_EMOJI1)

        if self.hand_player_2 is not None:
            points_player = self.hand_player_2.get_points()
            if points_player[0] > 21:
                self.hand_player_2.busted = True
                await reaction.message.clear_reaction(Variables.INC_EMOJI2)
        try:
            await reaction.message.clear_reaction(Variables.SPLIT_EMOJI)
        except:
            pass
        await reaction.message.remove_reaction(reaction.emoji, user)
        await reaction.message.edit(content=self.get_board())

        await self.blackjack_or_busted()

        await self.wait_for_player()

    async def bank_plays(self):
        await self.msg.edit(content=self.get_board(True))
        points = self.hand_bank.get_points()
        while points[1] < 17:
            self.hand_bank.get_card()
            points = self.hand_bank.get_points()
            await self.msg.edit(content=self.get_board(True))

        points = self.hand_bank.get_points()
        if points[0] > 21:
            self.hand_bank.busted = True
            await self.msg.edit(content=self.get_board(True))

    def get_board(self, bank_playing=False):
        text = "```BLACKJACK\n" \
               "Hand 1: "
        for card in self.hand_player_1.cards:
            text += card.value + " of " + card.suit + ", "
        text = text[:-2] + "\n"
        player_points = self.hand_player_1.get_points()
        text += "Points: {0}".format(player_points[0])
        if player_points[0] != player_points[1]:
            text += " or {0}".format(player_points[1])
        if self.hand_player_1.busted:
            text += " -> BUSTED"

        if self.hand_player_2 is not None:
            text += "\nHand 2: "
            for card in self.hand_player_2.cards:
                text += card.value + " of " + card.suit + ", "
            text = text[:-2] + "\n"
            player_points = self.hand_player_2.get_points()
            text += "Points: {0}".format(player_points[0])
            if player_points[0] != player_points[1]:
                text += " or {0}".format(player_points[1])
            if self.hand_player_2.busted:
                text += " -> BUSTED"

        text += "\n\nBank's cards:\n"
        text += "Hand: "
        if len(self.hand_bank.cards) == 2 and not bank_playing:
            text += "{0} of {1}, ? of ?\n".format(self.hand_bank.cards[0].value, self.hand_bank.cards[0].suit)
            point = self.hand_bank.get_card_value(self.hand_bank.cards[0])
            text += "Points: {0}".format(point[0])
            if point[0] != point[1]:
                text += " or {0}".format(point[1])
            if self.hand_bank.busted:
                text += " -> BUSTED"
        else:
            for card in self.hand_bank.cards:
                text += card.value + " of " + card.suit + ", "
            text = text[:-2]
            points = self.hand_bank.get_points()
            text += "\nPoints: {0}".format(points[0])
            if points[0] != points[1]:
                text += " or {0}".format(points[1])
            if self.hand_bank.busted:
                text += " -> BUSTED"
        text += "``````Wins: {0}\nLosses: {1}\nDraws: {2}\n```".format(self.wins, self.losses, self.draws)
        return text

    async def player_drew(self):
        self.draws += 1
        await self.msg.edit(content=self.get_board(True) + "<@" + str(self.player_id) + "> drew with the dealer.")
        await self.msg.clear_reactions()
        await self.restart()

    async def player_won(self):
        self.wins += 1
        await self.msg.edit(content=self.get_board(True) + "Congratulations, <@" + str(self.player_id) + "> won!")
        await self.msg.clear_reactions()
        await self.restart()

    async def player_lost(self):
        self.losses += 1
        await self.msg.edit(content=self.get_board(True) + "Too bad! <@" + str(self.player_id) + "> lost.")
        await self.msg.clear_reactions()
        await self.restart()

    def player_split(self):
        self.hand_player_2 = Hand(self.deck)
        self.hand_player_2.fold()
        self.hand_player_2.add_card(self.hand_player_1.cards[1])
        self.hand_player_2.get_card()
        self.hand_player_1.remove_card(1)
        self.hand_player_1.get_card()

    async def blackjack_or_busted(self):
        if self.hand_player_1.busted:
            if self.hand_player_2 is None or self.hand_player_2.busted:
                await self.bank_plays()
                if self.hand_bank.busted:
                    await self.player_drew()
                else:
                    await self.player_lost()
                return True

        points_player = self.hand_player_1.get_points()
        if points_player[0] == 21 or points_player[1] == 21:
            await self.bank_plays()
            if self.hand_bank.busted:
                await self.player_won()
                return True
            if self.hand_bank.has_blackjack():
                await self.player_drew()
                return True
            else:
                await self.player_won()
                return True

        if self.hand_player_2 is not None:
            points_player = self.hand_player_2.get_points()
            if points_player[0] == 21 or points_player[1] == 21:
                await self.bank_plays()
                if self.hand_bank.busted:
                    await self.player_won()
                    return True
                if self.hand_bank.has_blackjack():
                    await self.player_drew()
                    return True

        if self.hand_bank.busted:
            await self.player_won()
            return True
        return False

    async def has_player_won(self):
        if await self.blackjack_or_busted():
            return
        max_point = self.hand_player_1.get_points()[1]
        if self.hand_player_2 is not None:
            if self.hand_player_2.get_points()[1] > max_point:
                max_point = self.hand_player_2.get_points()[1]
        max_point_bank = self.hand_bank.get_points()[1]
        if max_point == max_point_bank:
            await self.player_drew()
        elif max_point > max_point_bank:
            await self.player_won()
        else:
            await self.player_lost()

    async def init_var(self):
        await self.msg.clear_reactions()
        self.terminated = False
        self.deck = pydealer.Deck()
        self.deck.shuffle()
        self.hand_player_1 = Hand(self.deck)
        self.hand_bank = Hand(self.deck)
        self.hand_player_2 = None

class Hand:
    def __init__(self, deck):
        self.deck = deck
        self.cards = list(self.deck.deal(2))
        self.busted = False

    def get_card_value(self, card):
        points = [0, 0]
        if card.value == "Jack" or card.value == "Queen" or card.value == "King":
            points[0] += 10
            points[1] += 10
        elif card.value == "Ace":
            points[0] += 1
            points[1] += 11
        else:
            points[0] += int(card.value)
            points[1] += int(card.value)
        return points

    def get_points(self):
        points = [0, 0]
        for i in range(len(self.cards)):
            if self.cards[i].value == "Jack" or self.cards[i].value == "Queen" or self.cards[i].value == "King":
                points[0] += 10
                points[1] += 10
            elif self.cards[i].value == "Ace":
                points[0] += 1
                points[1] += 11
            else:
                points[0] += int(self.cards[i].value)
                points[1] += int(self.cards[i].value)
        if points[1] > 21:
            points[1] = points[0]
        return points

    def remove_card(self, index):
        del self.cards[index]

    def add_card(self, card):
        self.cards.append(card)

    def get_card(self):
        self.cards += list(self.deck.deal())

    def fold(self):
        self.cards = list()

    def has_blackjack(self):
        points = self.get_points()
        if points[0] == 21 or points[1] == 21:
            return True
        return False

    def is_splittable(self):
        return self.cards[0].value == self.cards[1].value
