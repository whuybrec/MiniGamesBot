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
        self.playerCards = list()
        self.playerCards_ = list()
        self.dealersCards = list()
        self.busted = False
        self.busted_ = False
        self.bankTurn = False

    async def start_game(self):
        self.playerCards = list(self.deck.deal(2))
        self.dealersCards = list(self.deck.deal(2))
        if self.get_points([self.playerCards[0]])[0] == self.get_points([self.playerCards[1]])[0]:
            await self.msg.add_reaction(Variables.SPLIT_EMOJI)
            self.splittable = True

        await self.msg.edit(content=self.get_board())
        await self.msg.add_reaction(Variables.INC_EMOJI1)
        await self.msg.add_reaction(Variables.STOP_EMOJI)

        if self.get_points(self.playerCards)[0] == 21 or self.get_points(self.playerCards)[1] == 21:
            if self.get_points(self.dealersCards)[0] == 21 or self.get_points(self.dealersCards)[1] == 21:
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
            if not self.busted:
                tmp = list(self.deck.deal())
                self.playerCards += tmp

        elif reaction.emoji == Variables.INC_EMOJI2:
            if not self.busted_:
                tmp = list(self.deck.deal())
                self.playerCards_ += tmp

        elif reaction.emoji == Variables.STOP_EMOJI:
            await self.bank_plays(reaction)

        elif reaction.emoji == Variables.SPLIT_EMOJI and self.splittable:
            await self.msg.add_reaction(Variables.INC_EMOJI2)
            self.playerCards = [self.playerCards[0]]
            tmp = list(self.deck.deal())
            self.playerCards += tmp
            self.playerCards_ = [self.playerCards[1]]
            tmp = list(self.deck.deal())
            self.playerCards_ += tmp
            self.splitted = True
            self.splittable = False

        if self.get_points(self.playerCards)[0] > 21:
            self.busted = True

        if self.splitted and self.get_points(self.playerCards_)[0] > 21:
            self.busted_ = True

        await reaction.message.remove_reaction(reaction.emoji, user)
        await reaction.message.edit(content=self.get_board())

        playerPoints = self.get_points(self.playerCards)
        if playerPoints[0] == 21 or playerPoints[1] == 21:
            await self.bank_plays(reaction)
            return

        if self.splitted:
            playerPoints = self.get_points(self.playerCards_)
            if playerPoints[0] == 21 or playerPoints[1] == 21:
                await self.bank_plays(reaction)
                return

        if self.busted and not self.splitted:
            await reaction.message.channel.send("<@" + str(self.playerID) + "> lost the game by having more than 21!")
            await self.end_game(reaction.message)
            return

        if self.splitted and self.busted and self.busted_:
            await reaction.message.channel.send("<@" + str(self.playerID) + "> lost the game by having more than 21 in both hands!")
            await self.end_game(reaction.message)
            return

    async def bank_plays(self, reaction):
        self.bankTurn = True
        while self.get_points(self.dealersCards)[1] < 17:
            tmp = list(self.deck.deal())
            self.dealersCards += tmp
            await reaction.message.edit(content=self.get_board())
        dealer_points = self.get_points(self.dealersCards)
        if dealer_points[0] > 21:
            await reaction.message.channel.send(
                "Congratulations! <@" + str(self.playerID) + "> won the game, because the dealer got more than 21!")
            await self.end_game(reaction.message)
            return
        dealer_max = dealer_points[1]
        if self.splitted:
            if self.busted:
                player_max = self.get_points(self.playerCards_)[1]
            else:
                player_max = self.get_points(self.playerCards)[1]
        else:
            player_max = self.get_points(self.playerCards)[1]

        if dealer_max < player_max:
            await reaction.message.channel.send("Congratulations! <@" + str(self.playerID) + "> won the game, because the dealer has less points than their hand!")
        elif dealer_max == player_max:
            await reaction.message.channel.send("<@" + str(self.playerID) + "> drawed with the dealer!")
        else:
            await reaction.message.channel.send(
                "<@" + str(self.playerID) + "> lost because the dealer has more points!")
        await self.end_game(reaction.message)
        return

    def get_board(self):
        player_points = self.get_points(self.playerCards)
        dealer_points = self.get_points(self.dealersCards)
        text = "```BLACKJACK\n"
        text += "\nYour cards: "
        for card in self.playerCards:
            text += card.value + " of " + card.suit + ", "
        text = text[:-2] + "\n"
        text += "Your points: {0}".format(player_points[0])
        if player_points[0] != player_points[1]:
            text += " or {0}".format(player_points[1])
        if self.busted:
            text += " -> BUSTED"

        if self.splitted:
            player_points_ = self.get_points(self.playerCards_)
            text += "\nYour 2nd hand:"
            for card in self.playerCards_:
                text += card.value + " of " + card.suit + ", "
            text = text[:-2] + "\n"
            text += "Your 2nd hand points: {0} ".format(player_points_[0])
            if player_points_[0] != player_points_[1]:
                text += " or {0}".format(player_points_[1])
            if self.busted_:
                text += " -> BUSTED"

        text += "\n\nDealer's cards: "
        if not self.bankTurn:
            text += self.dealersCards[0].value + " of " + self.dealersCards[0].suit + ", ? of ?"
            dealer_points = self.get_points([self.dealersCards[0]])
            text += "\n"
        else:
            for card in self.dealersCards:
                text += card.value + " of " + card.suit + ", "
            text = text[:-2] + "\n"
        text += "Dealer's points: {0}".format(dealer_points[0])
        if dealer_points[0] != dealer_points[1]:
            text += " or {0}".format(dealer_points[1])
        text += "\n"
        text += "```"
        return text

    def get_points(self, cards):
        points = [0, 0]
        for i in range(len(cards)):
            if cards[i].value == "Jack" or cards[i].value == "Queen" or cards[i].value == "King":
                points[0] += 10
                points[1] += 10
            elif cards[i].value == "Ace":
                points[0] += 1
                points[1] += 11
            else:
                points[0] += int(cards[i].value)
                points[1] += int(cards[i].value)
        if points[1] > 21:
            points[1] = points[0]
        return points

    def get_max(self, lst):
        if lst[0] > lst[1]:
            return lst[0]
        else:
            return lst[1]
