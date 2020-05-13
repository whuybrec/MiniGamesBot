import re
from Minigames.connect4 import Connect4
from Minigames.hangman import HangMan
from Minigames.scramble import Scramble
from Minigames.guessword import GuessWord
from Minigames.blackjack import BlackJack
from Other.variables import Variables, toggle_wordguess_id, toggle_hangman_id


# BLACKJACK
async def blackjack_game(context):
    await increment_game("bj")
    msg = await context.channel.send("Starting a game of blackjack...")
    Variables.games_blackjack[msg.id] = BlackJack(context.author.id, msg)
    await Variables.games_blackjack[msg.id].start_blackjack_game()
    Variables.scheduler.add(Variables.DEADLINE, close_blackjack_game, context, msg.id)

async def close_blackjack_game(context, msg_id):
    if msg_id in Variables.games_blackjack.keys():
        msg = await context.message.channel.fetch_message(msg_id)
        await msg.edit(content="```Game closed, deadline reached.```")
        del Variables.games_blackjack[int(msg_id)]
        await msg.clear_reactions()


# GUESSWORD
async def start_guessword_game(context):
    msg = await context.channel.send("Starting a game of guessword...")
    Variables.games_guessword[msg.id] = GuessWord(msg)
    Variables.games_guessword_index[Variables.games_guessword[msg.id].index] = msg.id
    text = Variables.games_guessword[msg.id].start_guessword_game()
    if text == "__FALSE__":
        await msg.edit(content="```Maximum of 200 games of guessword at a time allowed.```")
        del Variables.games_guessword_index[Variables.games_guessword[msg.id].index]
        del Variables.games_guessword[msg.id]
    else:
        await increment_game("gw")
        Variables.scheduler.add(Variables.DEADLINE, close_wordguess_game, context, msg.id)
        await msg.edit(content=text)

async def guessword_update(context, ID, word):
    try:
        msg_id = Variables.games_guessword_index[int(ID)]
        msg = await context.message.channel.fetch_message(msg_id)
        end = Variables.games_guessword[msg.id].update_game(word)
        if end:
            del Variables.games_guessword_index[Variables.games_guessword[msg.id].id]
            del Variables.games_guessword[msg.id]
            toggle_wordguess_id(int(ID))
            await context.channel.send("Congratulations, <@" + str(context.author.id) + "> won the guessword game!\nThe word was '"+str(word)+"'.")
    except:
        pass

async def close_wordguess_game(context, msg_id):
    if msg_id in Variables.games_guessword.keys():
        msg = await context.message.channel.fetch_message(msg_id)
        await msg.edit(content="```Game closed, deadline reached.```")
        del Variables.games_guessword[int(msg_id)]
        await msg.clear_reactions()


# SCRAMBLE
async def start_scramble_game(context):
    await increment_game("sc")
    msg = await context.channel.send("Starting a game of scramble for <@" + str(context.author.id) + ">")
    Variables.games_scramble[msg.id] = Scramble(context.author.id, msg)
    await Variables.games_scramble[msg.id].start_scramble_game()
    Variables.scheduler.add(Variables.DEADLINE*2, close_scramble_game, context, msg.id)

async def close_scramble_game(context, msg_id):
    if msg_id in Variables.games_scramble.keys():
        msg = await context.message.channel.fetch_message(msg_id)
        await msg.edit(content="```Game closed, deadline reached.```")
        del Variables.games_scramble[int(msg_id)]
        await msg.clear_reactions()


# CONNECT4
async def start_connect4_game(context, player1, player2):
    await increment_game("c4")
    msg = await context.channel.send("Starting a game of connect4 with " + str(player1) + " and " + str(player2))
    try:
        temp = re.findall(r'\d+', player1)
        p1id = int(list(map(int, temp))[0])
        temp = re.findall(r'\d+', player2)
        p2id = int(list(map(int, temp))[0])
        Variables.games_connect4[msg.id] = Connect4(p1id, p2id, msg)
    except:
        await context.channel.send("Invalid command to start connect4 game, try: ?connect4 [@player1] [@player2]")
        return
    await msg.edit(content=Variables.games_connect4[msg.id].updateBoard())
    for emo in Variables.REACTIONS_CONNECT4:
        await msg.add_reaction(emo)
    Variables.scheduler.add(Variables.DEADLINE, close_connect4_game, context, msg.id)


async def close_connect4_game(context, msg_id):
    if msg_id in Variables.games_connect4.keys():
        msg = await context.message.channel.fetch_message(msg_id)
        await msg.edit(content="```Game closed, deadline reached.```")
        await msg.clear_reactions()
        del Variables.games_connect4[int(msg_id)]


async def start_hangman_game(context):
    msg = await context.channel.send("Starting a game of hangman...")
    Variables.games_hangman[msg.id] = HangMan(msg)
    Variables.games_hangman_index[Variables.games_hangman[msg.id].id] = msg.id
    text = Variables.games_hangman[msg.id].start_hangman_game()
    if text == "__FALSE__":
        await msg.edit(content="```Maximum of 200 games of hangman at a time allowed.```")
        del Variables.games_hangman_index[Variables.games_hangman[msg.id].id]
        del Variables.games_hangman[msg.id]
    else:
        await increment_game("hm")
        Variables.scheduler.add(Variables.DEADLINE, close_hangman_game, context, msg.id)
        await msg.edit(content=text)

async def hangman_update(context, ID, letter):
    try:
        msg_id = Variables.games_hangman_index[int(ID)]
        msg = await context.message.channel.fetch_message(msg_id)
        text, end = Variables.games_hangman[msg.id].update_game(letter.lower())
        if end:
            del Variables.games_hangman_index[Variables.games_hangman[msg.id].id]
            del Variables.games_hangman[msg.id]
            toggle_hangman_id(int(ID))
        await msg.edit(content=text)
    except:
        pass

async def close_hangman_game(context, msg_id):
    if msg_id in Variables.games_hangman.keys():
        msg = await context.message.channel.fetch_message(msg_id)
        await msg.edit(content="```Game closed, deadline reached.```")
        del Variables.games_hangman_index[Variables.games_hangman[msg_id].id]
        toggle_hangman_id(int(Variables.games_hangman[msg_id].id))
        del Variables.games_hangman[msg_id]

async def increment_game(game):
    Variables.amtPlayedGames[game] = int(Variables.amtPlayedGames[game]) + 1
