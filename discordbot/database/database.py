import sqlite3
from sqlite3 import Error
from discordbot.variables import Variables
from discordbot.private import Private

# DATABASE master ROW:
# server_id | user_id | game_name |
# wins | losses | draws | total_time_played | min_time_played | max_time_played | first_time_played | last_time_played |

class DataBase:
    con = None
    bot = None

    @classmethod
    def initialize(cls, bot):
        cls.bot = bot
        cls.con = sqlite3.connect(Variables.database_file)
        cls.create_tables()

    @classmethod
    def create_tables(cls):
        create_master_table = """CREATE TABLE IF NOT EXISTS master (
                                                server_id integer,
                                                user_id integer,
                                                game_name text,
                                                wins integer,
                                                losses integer,
                                                draws integer,
                                                total_time_played integer, 
                                                min_time_played integer,
                                                max_time_played integer,
                                                first_time_played integer,
                                                last_time_played integer,
                                                PRIMARY KEY (server_id, user_id, game_name)
                                            ); """

        create_daily_table = """CREATE TABLE IF NOT EXISTS daily_stats (
                                                date_ text,
                                                server_id integer,
                                                game_name text,
                                                wins integer,
                                                losses integer,
                                                draws integer,
                                                total_time_played integer, 
                                                PRIMARY KEY (date_, server_id, game_name)
                                            ); """

        create_announcements_table = """CREATE TABLE IF NOT EXISTS announcement_channels (
                                                        server_id integer,
                                                        channel_id integer,
                                                        PRIMARY KEY (server_id)
                                                    ); """

        create_commands_table = """CREATE TABLE IF NOT EXISTS commands (
                                                                date_ text,
                                                                command text,
                                                                amount integer,
                                                                PRIMARY KEY (date_, command)
                                                            ); """
        c = cls.con.cursor()
        c.execute(create_master_table)
        c.execute(create_daily_table)
        c.execute(create_announcements_table)
        c.execute(create_commands_table)

    @classmethod
    def insert_master_row(cls, values: tuple):
        sql = '''INSERT INTO master(server_id, user_id, game_name, wins, losses, draws, total_time_played,
                                     min_time_played, max_time_played, first_time_played, last_time_played)
                 VALUES (?,?,?,?,?,?,?,?,?,?,?)'''
        cur = cls.con.cursor()
        cur.execute(sql, values)
        cls.con.commit()

    @classmethod
    def insert_daily_stats_row(cls, values: tuple):
        sql = '''INSERT INTO daily_stats(date_, server_id, game_name, wins, losses, draws, total_time_played)
                     VALUES (?,?,?,?,?,?,?)'''
        cur = cls.con.cursor()
        cur.execute(sql, values)
        cls.con.commit()

    @classmethod
    def select_master_row(cls, where: dict = None):
        cur = cls.con.cursor()
        if where is None:
            sql = "SELECT * FROM master "
            cur.execute(sql)
        else:
            where_clause, t = cls.get_where_clause(where)
            sql = "SELECT * FROM master WHERE " + where_clause
            cur.execute(sql, t)
        rows = cur.fetchall()
        return rows

    @classmethod
    def delete_master_row(cls, key: tuple):
        sql = 'DELETE FROM master WHERE server_id = ? AND user_id = ? AND game_name = ?'
        cur = cls.con.cursor()
        cur.execute(sql, key)
        cls.con.commit()

    @classmethod
    def run(cls, sql):
        cur = cls.con.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        cls.con.commit()
        return rows

    @classmethod
    async def create_connection(cls):
        cls.con = None
        channel = cls.bot.get_channel(Private.LOGS_COMMANDS_CHANNELID)
        try:
            cls.con = sqlite3.connect(Variables.database_file)
            await channel.send(sqlite3.version)
        except Error as e:
            await channel.send(e)
        finally:
            if cls.con:
                cls.con.close()

    @classmethod
    def get_where_clause(cls, where: dict):
        clause = ""
        for key in where.keys():
            clause += "{0} = ? AND ".format(key)
        clause = clause[:-len(" AND ")]
        return clause, tuple(where.values())

