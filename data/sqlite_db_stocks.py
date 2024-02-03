import sqlite3
import logging

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, path_to_db="data/stocks.db"):
        self.path_to_db = path_to_db

    @property
    def connect(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self,
                sql: str,
                parameters: tuple = None,
                fetchall=False,
                fetchone=False,
                commit=False):
        if not parameters:
            parameters = tuple()
        connection = self.connect
        connection.set_trace_callback(logger_bd)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()
        return data

    def create_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Stocks (
          id INTEGER NOT NULL,
          name VARCHAR(255) NOT NULL,
          description VARCHAR(255),
          price VARCHAR(255),
          category VARCHAR(255) NOT NULL,
          PRIMARY KEY (id)
        );"""
        self.execute(sql, commit=True)

    def add_stock(self, id: int, name: str, category: str,
                  description: str = None, price: str = None,
                  ):
        sql = "INSERT INTO Stocks (id, name, category, description, price) VALUES (?, ?, ?, ?, ?)"
        parameters = (id, name, category, description, price)
        self.execute(sql, parameters, commit=True)

    def select_all_stocks(self):
        sql = "SELECT * FROM Stocks;"
        return self.execute(sql, fetchall=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f" {item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def select_stock(self, **kwargs):
        sql = "SELECT * FROM Stocks WHERE"
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)

    def delete_stocks(self):
        self.execute("DELETE FROM Stocks WHERE TRUE")


def logger_bd(stattement):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.info(f"""
    ________________________________________
    Executing:
    {stattement}
    ________________________________________
    """)
