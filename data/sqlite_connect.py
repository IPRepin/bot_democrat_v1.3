import logging
import sqlite3

from utils.logger_settings import get_logger

logger = logging.getLogger(__name__)


class DatabaseConnect:
    def __init__(self, path_to_db="data/stocks.db"):
        self.path_to_db = path_to_db

    def execute(self,
                sql,
                parameters=None,
                fetchall=False,
                fetchone=False,
                commit=False):
        if not parameters:
            parameters = tuple()
        with sqlite3.connect(self.path_to_db) as connection:
            connection.set_trace_callback(logger_bd)
            cursor = connection.cursor()
            cursor.execute(sql, parameters)
            if commit:
                connection.commit()
            data = None
            if fetchall:
                data = cursor.fetchall()
            elif fetchone:
                data = cursor.fetchone()
            return data


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
