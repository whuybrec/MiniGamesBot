# MiniGamesBot

A Python Discord bot with different kinds of minigames and keeps statistics per minigame and player.


## Discord Bot Commands

### Miscellaneous

**?help** *command*  
  —  Gives the help message.  
**?info**  
  —  Shows some information about this bot.  
**?rules** minigame  
  —  Shows the rules for the given minigame.
**?stats** *@player*  
  —  Shows stats for all minigames for yourself or for the tagged player.  
**?set_prefix** new prefix  
  —  Set a new prefix for this bot.  
**?bug** bug description  
  —  Report a bug with a description as argument.  

### Minigames

**?hangman**  
  —  Start a game of hangman.  
**?scramble**   
  —  Start a game of scramble.  
**?connect4**  @player2  
  —  Start a game of connect4.  
**?quiz**   
  —  Start a quiz.  
**?blackjack**   
  —  Start a game of blackjack.  
**?chess** @player2  
  —  Start a game of chess.

Arguments in italic  are optional.  
There are 5 categories in the quiz minigame: General knowledge, Sports, Video Games, Music, Films.

This bot keeps statistics for players and minigames. 
It uploads the database file to a discord channel every once in a while as a backup. (same for prefixes.json file)

## Requirements

Check requirements.txt for a list of all the libraries that you need.  
To install them all:

> pip install -r requirements.txt

Additionally, you need to install 'svgexport' from https://www.npmjs.com/package/svgexport.
This is necessary to convert the svg (given by chess library) to a PNG, so it can be uploaded to Discord.


## How to use?

You are allowed to use this code. A donation is appreciated but not necessary in that case. (link below)
1. Create a Discord bot on the discord developers webpage.
2. Clone this repository.
3. Adjust the variables in 'discordbot.utils.private.py': enter the bot's token, your discord ID, your bot's discord ID and some channel IDs.
4. Run 'main.py'


## About me

My name is Wouter Huybrechts. I study computer science at the KU Leuven in Belgium.
My hobbies are: coding, gaming, cycling, badminton, watching series & movies.
If you wish to make a donation, you can buy me a coffee here: https://www.buymeacoffee.com/whuybrec

