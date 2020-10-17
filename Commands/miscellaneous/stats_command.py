from Commands.discord_command import DiscordCommand
from discord.member import Member
from Database.database import DataBase
import time, re
from Other.variables import Variables, convert

# DATABASE ROW:
# server_id | user_id | game_name |
# wins | losses | draws | total_time_played | min_time_played | max_time_played | first_time_played | last_time_played |

class StatsCommand(DiscordCommand):
    bot = None
    name = "stats"
    brief = "View the detailed statistics of yourself, another player or a certain minigame."
    help = "This command shows your (or the tagged user) draws, wins, losses, winrate and total time played per minigame.\n" \
            "To view statistics on a certain minigame, put the minigame's name as argument.\n" \
            "Compare the global statistics with yours for that minigame and see if you're doing better!"
    usage = "[@user] / [minigame]"
    category = "miscellaneous"

    @classmethod
    async def handler(cls, context, *args):
        if not args:
            stats = cls.get_user_stats(context.author.id)
            if stats == "":
                await context.message.channel.send("No statistics are found of this user.")
            else:
                await context.message.channel.send(stats)
        else:
            matches = re.findall('[0-9]+', args[0])
            if len(matches) == 1 and matches[0] != "4":
                stats = cls.get_user_stats(matches[0])
                if stats == "":
                    await context.message.channel.send("No statistics are found of this user.")
                else:
                    await context.message.channel.send(stats)
            else:
                if args[0].lower() not in Variables.game_names:
                    return
                await context.message.channel.send(cls.get_game_stats(context.author, args[0]))

    @classmethod
    def get_user_stats(cls, user_id: int):
        stats = ""
        rows = DataBase.run("SELECT game_name, SUM(wins), SUM(losses), SUM(draws), SUM(total_time_played), "
                            "MIN(min_time_played), MAX(max_time_played), first_time_played, last_time_played "
                            "FROM master WHERE user_id = {0} GROUP BY game_name".format(user_id))
        if len(rows) == 0:
            return stats
        stats = "```python\n"
        stats += "{0:10} {1:>4} {2:>6} {3:>5} {4:>7} {5:>15}\n".format("MiniGame", "Wins", "Losses", "Draws", "Winrate", "Time Played")
        for row in rows:
            try:
                stats += "{0:10} {1:4} {2:6} {3:5} {4:>7} {5:>15}\n".format(row[0], row[1], row[2], row[3], str(round(row[1]/(row[1]+row[2]+row[3])*100))+"%", time.strftime('%H:%M:%S', time.gmtime(row[4])))
            except ZeroDivisionError:
                stats += "{0:10} {1:4} {2:6} {3:5} {4:>7} {5:>15}\n".format(row[0], row[1], row[2], row[3], "0%", time.strftime('%H:%M:%S', time.gmtime(row[4])))
        stats += "```"
        return stats

    @classmethod
    def get_game_stats(cls, user: Member, game_name: str):
        rows_game = DataBase.select_master_row({"game_name": game_name.lower()})
        rows_user = DataBase.run("SELECT game_name, SUM(wins), SUM(losses), SUM(draws), SUM(total_time_played), "
                                 "MIN(min_time_played), MAX(max_time_played), MIN(first_time_played), MAX(last_time_played) "
                                 "FROM master WHERE user_id = {0} AND game_name = '{1}' GROUP BY game_name".format(user.id, game_name))
        wins = 0
        losses = 0
        draws = 0
        time_played = 0
        for row in rows_game:
            wins += row[3]
            losses += row[4]
            draws += row[5]
            time_played += row[6]

        stats = "```python\n{0} stats\n\n".format(game_name)
        stats += "         {0:>4} {1:>6} {2:>5} {3:>7} {4:>15}\n".format("Wins", "Losses", "Draws", "Winrate", "Time Played")
        try:
            stats += "TOTAL    {0:>4} {1:>6} {2:>5} {3:>7} {4:>15}\n".format(wins, losses, draws, str(round(wins/ (wins+draws+losses) * 100))+"%", convert(time_played))
        except ZeroDivisionError:
            stats += "TOTAL    {0:>4} {1:>6} {2:>5} {3:>7} {4:>15}\n".format(wins, losses, draws, "0%", convert(time_played))
        if len(rows_user) == 0:
            stats += "```"
            return stats
        rows_user = rows_user[0]
        stats += "\n"
        try:
            stats += "YOURS    {0:4} {1:6} {2:5} {3:>7} {4:>15}\n".format(rows_user[1], rows_user[2], rows_user[3],
                                                                 str(round(rows_user[1] / (rows_user[1] + rows_user[2] + rows_user[3]) * 100)) + "%",
                                                                 time.strftime('%H:%M:%S', time.gmtime(rows_user[4])))
        except ZeroDivisionError:
            stats += "YOURS    {0:4} {1:6} {2:5} {3:>7} {4:>15}\n".format(rows_user[1], rows_user[2], rows_user[3], "0%",
                                                                        time.strftime('%H:%M:%S', time.gmtime(rows_user[4])))
        stats += "\nFirst game: {0}".format(time.ctime(int(rows_user[7])))
        stats += "\nLatest game: {0}".format(time.ctime(int(rows_user[8])))
        stats += "```"
        return stats
