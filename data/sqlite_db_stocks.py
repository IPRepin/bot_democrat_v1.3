from data.sqlite_connect import DatabaseConnect


class DatabaseStocks(DatabaseConnect):
    def create_table_stocks(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Stocks (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          name TEXT NOT NULL,
          image TEXT,
          description TEXT,
          price TEXT
        );
        """
        self.execute(sql, commit=True)

    def add_stock(self, name: str,
                  description: str = None,
                  price: str = None,
                  image: str = None,
                  ):
        sql = "INSERT INTO Stocks ( name, description, price, image) VALUES (?, ?, ?, ?)"
        parameters = (name, description, price, image)
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

    def update_stock(self, stock_id, **kwargs):
        sql = "UPDATE Stocks SET "
        sql += ", ".join([f"{key} = ?" for key in kwargs])
        sql += f" WHERE id = {stock_id}"
        parameters = tuple(kwargs.values())
        self.execute(sql, parameters, commit=True)
