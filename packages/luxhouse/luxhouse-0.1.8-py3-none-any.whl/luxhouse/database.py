from abc import abstractmethod

from luxhouse.model import House, Location, PriceDate

class Database(object):
    def __init__(self, connection_string:str) -> None:
        self.connection_string = connection_string
        with self.connect() as conn:
                cursor = conn.cursor()
                cursor.execute(Location.create_table(cursor))
                cursor.execute(House.create_table(cursor))
                cursor.execute(PriceDate.create_table(cursor))

    @abstractmethod
    def connect(self):
        pass

    def add_house(self, house:House) -> None:
        with self.connect() as conn:
            cursor = conn.cursor()
            house.insert(cursor)


class SQLite(Database):
    def __init__(self, connection_string:str) -> None:
        super().__init__(connection_string)

    def connect(self):
        import sqlite3
        return sqlite3.connect(self.connection_string)