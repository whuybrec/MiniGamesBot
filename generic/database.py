"""
    database_old.py
        A wrapper around the sqlite3 python library.
"""

import sqlite3


class Database:
    def __init__(self, name=None):
        """
        The constructor of the Database class.
        :param name: (optional) Name of the database
        """

        self.conn = None
        self.cursor = None

        if name:
            self.open(name)

    def open(self, name):
        """
        Opens a new database connection.
        :param name: Name of the database to open
        :return:
        """

        try:
            self.conn = sqlite3.connect(name)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()

        except sqlite3.Error as e:
            print(f"Error connecting to database!: {e}")

    def close(self):
        """
        Function to close a datbase connection.
        :return:
        """

        if self.conn:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def create_table(self, table: str, columns: list, keys: list):
        """
        Function to create table in the database.
        :param table: The name of the new database's table.
        :param columns: The string of columns, comma-separated.
        :param keys: The list with primary keys
        :return:
        """

        columns = ", ".join(columns)
        keys = ", ".join(keys)
        query = "CREATE TABLE IF NOT EXISTS {0} ({1}, PRIMARY KEY ({2}));".format(table, columns, keys)
        self.cursor.execute(query)
        self.conn.commit()

    def add_column(self, table: str, attribute: str, t: str):
        try:
            query = "alter table {0} add column {1} {2}".format(table, attribute, t)
            self.cursor.execute(query)
        except sqlite3.OperationalError:
            pass
        self.conn.commit()

    def get(self, table: str, columns: list, where: dict, limit=None):
        """
        Function to fetch/query data from the database.
        :param table: The name of the database's table to query from.
        :param columns:  A list of strings representing the columns which to query.
        :param where: Dictionary to filter rows, keys are columns, values are database values.
        :param limit: (Optional) limit of items to fetch.
        :return:
        """

        where_clause = "WHERE "
        for key, value in where.items():
            where_clause += f"{key}={value} AND "
        where_clause = where_clause[:-5]

        columns = ", ".join(columns)
        if len(where) == 0:
            query = "SELECT {0} FROM ({1});".format(columns, table)
        else:
            query = "SELECT {0} FROM ({1}) {2};".format(columns, table, where_clause)
        self.cursor.execute(query)

        # fetch data
        rows = self.cursor.fetchall()
        return rows[len(rows) - limit if limit else 0:]

    def has(self, table: str, columns: list, where: dict):
        """
        Function to check if a row exists in the database.
        :param table: The database's table from which to query.
        :param columns: A list of strings representing the columns which to query.
        :param where: Dictionary to filter rows, keys are columns, values are database values.
        :return:
        """
        rows = self.get(table, columns, where)
        if rows:
            return True
        return False

    def get_last(self, table: str, columns: list):
        """
        Utilty function to get the last row of data from a database.
        :param table: The database's table from which to query.
        :param columns: The columns which to query.
        :return:
        """

        return self.get(table, columns, dict(), limit=1)[0]

    @staticmethod
    def to_csv(data, fname="output.csv"):
        """
        Utility function that converts a dataset into CSV format.
        :param data: The data, retrieved from the get() function.
        :param fname: The file name to store the data in.
        :return:
        """

        with open(fname, 'a') as file:
            file.write(",".join([str(j) for i in data for j in i]))

    def write(self, table, data, where=None):
        """
        Function to write data to the database.
        :param table: The name of the database's table to write to.
        :param data: The new data to insert, a dictionary with keys (as columns) and values
        :param where: Dictionary to filter rows, keys are columns, values are database values.
        :return:
        """

        if where is None:
            columns = ""
            values = ""
            for column, value in data.items():
                columns += f"{column}, "
                values += f"{value}, "
            columns = columns[:-2]
            values = values[:-2]

            query = "INSERT INTO {0} ({1}) VALUES ({2});".format(table, columns, values)
        else:
            columns_clause = ""
            for key, value in data.items():
                columns_clause += f"{key} = {value}, "
            columns_clause = columns_clause[:-2]

            where_clause = ""
            for key, value in where.items():
                where_clause += f"{key}={value} AND "
            where_clause = where_clause[:-5]
            query = "UPDATE {0} SET {1} WHERE {2};".format(table, columns_clause, where_clause)
        self.cursor.execute(query)
        self.conn.commit()

    def query(self, sql):
        """
        Function to query any other SQL statement.
        :param sql: A valid SQL statement in string format.
        :return:
        """

        self.cursor.execute(sql)

    @staticmethod
    def summary(rows):
        """
        Utility function that summarizes a dataset.
        :param rows: The retrieved data.
        :return:
        """

        # split the rows into columns
        cols = [[r[c] for r in rows] for c in range(len(rows[0]))]

        # the time in terms of fractions of hours of how long ago
        # the sample was assumes the sampling period is 10 minutes
        t = lambda col: "{:.1f}".format((len(rows) - col) / 6.0)

        # return a tuple, consisting of tuples of the maximum,
        # the minimum and the average for each column and their
        # respective time (how long ago, in fractions of hours)
        # average has no time, of course
        ret = []

        for c in cols:
            hi = max(c)
            hi_t = t(c.index(hi))

            lo = min(c)
            lo_t = t(c.index(lo))

            avg = sum(c) / len(rows)

            ret.append(((hi, hi_t), (lo, lo_t), avg))

        return ret
