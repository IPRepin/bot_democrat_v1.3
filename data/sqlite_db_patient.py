from data.sqlite_connect import DatabaseConnect


class DatabasePatient(DatabaseConnect):

    def create_table_patient(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Patient (
          user_name VARCHAR(255) NOT NULL,
          user_id INTEGER NOT NULL,
          phone VARCHAR(255),
          PRIMARY KEY (user_id)
        );"""
        self.execute(sql, commit=True)

    def add_patient(self, user_id: int, user_name: str, phone: str,
                    ):
        sql = "INSERT INTO Patient (user_id, user_name, phone) VALUES (?, ?, ?)"
        parameters = (user_id, user_name, phone)
        self.execute(sql, parameters, commit=True)

    def select_all_patient(self):
        sql = "SELECT * FROM Patient;"
        return self.execute(sql, fetchall=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f" {item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def select_patient(self, **kwargs):
        sql = "SELECT * FROM Patient WHERE"
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)

    def delete_patient(self):
        self.execute("DELETE FROM Patient WHERE TRUE")

    def patient_update(self, user_id, user_name, phone):
        sql = "UPDATE Patient SET user_name = ?, phone = ? WHERE user_id = ?"
        parameters = (user_name, phone, user_id)
        self.execute(sql, parameters, commit=True)
