from data.sqlite_connect import DatabaseConnect


class DatabaseStocks(DatabaseConnect):
    def create_table_stocks(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Stocks (
          id INTEGER NOT NULL,
          name VARCHAR(255) NOT NULL,
          description VARCHAR(255),
          price VARCHAR(255),
          PRIMARY KEY (id)
        );"""
        self.execute(sql, commit=True)

    def add_stock(self, id: int, name: str, category: str,
                  description: str = None, price: str = None,
                  ):
        sql = "INSERT INTO Stocks (id, name, description, price) VALUES (?, ?, ?, ?)"
        parameters = (id, name, description, price)
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

