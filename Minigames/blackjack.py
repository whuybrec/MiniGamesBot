import pydealer
from Other.private import Private
from Other.variables import Variables

class BlackJack:
    def __init__(self, gamemanager, msg, playerID):
        self.gamemanager = gamemanager
        self.msg = msg
        self.playerID = playerID
        self.splitted = False
        self.splittable = False
        self.deck = pydealer.Deck()
        self.deck.shuffle()
        self.hand_player = Hand(self.deck)
        self.hand_dealer = Hand(self.deck)
        self.hand_player_2 = None
        self.bankTurn = False

    async def start_game(self):
        if self.hand_player.cards[0].value == self.hand_player.cards[1].value:
            await self.msg.add_reaction(Variables.SPLIT_EMOJI)
            self.splittable = True

        await self.msg.edit(content=self.get_board())
        await self.msg.add_reaction(Variables.INC_EMOJI1)
        await self.msg.add_reaction(Variables.STOP_EMOJI)

        points_player = self.hand_player.get_points()
        points_dealer = self.hand_dealer.get_points()
        if points_player[0] == 21 or points_player[1] == 21:
            if points_dealer[0] == 21 or points_dealer[1] == 21:
                await self.msg.channel.send("<@" + str(self.playerID) + "> drawed with the dealer!")
            else:
                await self.msg.channel.send("Congratulations! <@" + str(self.playerID) + "> got BlackJack and won the game!")
            self.bankTurn = True
            await self.msg.edit(content=self.get_board())
            await self.end_game(self.msg)
            await self.gamemanager.close_game(self.msg.id)

    async def end_game(self, message):
        await self.gamemanager.close_game(message)

    async def update_game(self, reaction, user):
        if user.id in Private.BOT_ID: return
        if not user.id == self.playerID:
            await reaction.message.remove_reaction(reaction.emoji, user)
            return

        if reaction.emoji == Variables.INC_EMOJI1:
            if not self.hand_player.busted:
                self.hand_player.get_card()

        elif reaction.emoji == Variables.INC_EMOJI2:
            if not self.hand_player_2.busted:
                self.hand_player_2.get_card()

        elif reaction.emoji == Variables.STOP_EMOJI:
            await self.dealer_plays()

        elif reaction.emoji == Variables.SPLIT_EMOJI and self.splittable:
            await self.msg.add_reaction(Variables.INC_EMOJI2)
            self.hand_player_2 = Hand(self.deck)
            self.hand_player_2.fold()
            self.hand_player_2.add_card(self.hand_player.cards[1])
            self.hand_player_2.get_card()

            self.hand_player.remove_card(1)
            self.hand_player.get_card()

            self.splitted = True
            self.splittable = False
            await reaction.message.clear_reaction(reaction.emoji)

        points_player = self.hand_player.get_points()
        if points_player[0] > 21:
            self.hand_player.busted = True

        if self.splitted:
            points_player_2 = self.hand_player_2.get_points()
            if points_player_2[0] > 21:
                self.hand_player_2.busted = True

        await reaction.message.remove_reaction(reaction.emoji, user)
        await reaction.message.edit(content=self.get_board())

        if points_player[0] == 21 or points_player[1] == 21:
            await self.dealer_plays()
            return

        if self.splitted:
            points_player_2 = self.hand_player_2.get_points()
            if points_player_2[0] == 21 or points_player_2[1] == 21:
                await self.dealer_plays()
                return

        if self.hand_player.busted and not self.splitted:
            await reaction.message.channel.send("<@" + str(self.playerID) + "> lost the game by having more than 21!")
            await self.end_game(reaction.message)
            return

        if self.splitted and self.hand_player.busted and self.hand_player_2.busted:
            await reaction.message.channel.send("<@" + str(self.playerID) + "> lost the game by having more than 21 in both hands!")
            await self.end_game(reaction.message)
            return

    async def dealer_plays(self):
        self.bankTurn = True
        await self.msg.edit(content=self.get_board())
        points_dealer = self.hand_dealer.get_points()
        while points_dealer[1] < 17:
            self.hand_dealer.get_card()
            points_dealer = self.hand_dealer.get_points()
            await self.msg.edit(content=self.get_board())

        if points_dealer[0] > 21:
            await self.msg.channel.send("Congratulations! <@" + str(self.playerID) + "> won the game, because the dealer got more than 21!")
            await self.end_game(self.msg)
            return

        dealer_max = points_dealer[1]
        all_points = self.hand_player.get_points()
        if self.splitted:
            all_points += self.hand_player_2.get_points()
        player_max = 0
        for nb in all_points:
            if player_max < nb <= 21:
                player_max = nb

        if dealer_max < player_max:
            await self.msg.channel.send("Congratulations! <@" + str(self.playerID) + "> won the game, because the dealer has less points than their hand!")
        elif dealer_max == player_max:
            await self.msg.channel.send("<@" + str(self.playerID) + "> drawed with the dealer!")
        else:
            await self.msg.channel.send(
                "<@" + str(self.playerID) + "> lost because the dealer has more points!")
        await self.end_game(self.msg)

    def get_board(self):
        player_points = self.hand_player.get_points()
        dealer_points = self.hand_dealer.get_points()
        text = "```BLACKJACK\n"
        text += "\nYour cards: "
        for card in self.hand_player.cards:
            text += card.value + " of " + card.suit + ", "
        text = text[:-2] + "\n"
        text += "Your points: {0}".format(player_points[0])
        if player_points[0] != player_points[1]:
            text += " or {0}".format(player_points[1])
        if self.hand_player.busted:
            text += " -> BUSTED"

        if self.splitted:
            player_points_ = self.hand_player_2.get_points()
            text += "\nYour 2nd hand: "
            for card in self.hand_player_2.cards:
                text += card.value + " of " + card.suit + ", "
            text = text[:-2] + "\n"
            text += "Your 2nd hand points: {0} ".format(player_points_[0])
            if player_points_[0] != player_points_[1]:
                text += " or {0}".format(player_points_[1])
            if self.hand_player_2.busted:
                text += " -> BUSTED"

        text += "\n\nDealer's cards: "
        if not self.bankTurn:
            text += self.hand_dealer.cards[0].value + " of " + self.hand_dealer.cards[0].suit + ", ? of ?"
            dealer_points = self.hand_dealer.get_card_value(self.hand_dealer.cards[0])
            text += "\n"
        else:
            for card in self.hand_dealer.cards:
                text += card.value + " of " + card.suit + ", "
            text = text[:-2] + "\n"
        text += "Dealer's points: {0}".format(dealer_points[0])
        if dealer_points[0] != dealer_points[1]:
            text += " or {0}".format(dealer_points[1])
        text += "\n"
        text += "```"
        return text

    def get_max(self):
        pass


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


