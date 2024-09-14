from abc import ABC, abstractmethod
import sqlite3

from fastapi import HTTPException, status

from schemas import NewTravel, SavedTravel


class BaseStorageTravel(ABC):
    @abstractmethod
    def create_travel(self, new_product: NewTravel):
        pass
    @abstractmethod
    def get_travel(self, _id: int):
        pass
    @abstractmethod
    def get_travel(self, limit: int = 10):
        pass
    @abstractmethod
    def update_travel_price(self, _id: int, new_price: float):
        pass
    @abstractmethod
    def delete_travel(self, _id: int):
        pass
class StorageSQLite(BaseStorageTravel):
    def _create_table(self):
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            query = f"""
                CREATE TABLE IF NOT EXISTS {self.travel_table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    description TEXT,
                    price REAL,
                    place TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP 
                )
            """
            cursor.execute(query)
    def __init__(self, database_name: str):
        self.database_name = database_name
        self.travel_table_name = 'travel'
        self._create_table()
    def create_travel(self, new_travel: NewTravel) -> SavedTravel:
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            values = (new_travel.title, new_travel.description, new_travel.price, str(new_travel.place))
            query = f"""
                INSERT INTO {self.travel_table_name} (title, description, price, place)
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(query, values)
        return self._get_latest_travel()
    def _get_latest_travel(self) -> SavedTravel:
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            query = f"""
                SELECT id, title, description, price, place, created_at
                FROM {self.travel_table_name}
                ORDER BY id DESC
                LIMIT 1
            """
            result: tuple = cursor.execute(query).fetchone()
            id, title, description, price, place, created_at = result
            saved_travel = SavedTravel(
                id=id, title=title, description=description, price=price, place=place, created_at=created_at
            )

            return saved_travel


    def get_travel(self, _id: int) -> SavedTravel:
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            query = f"""
                SELECT id, title, description, price, place, created_at
                FROM {self.travel_table_name}
                WHERE id = {_id}
            """
            result: tuple = cursor.execute(query).fetchone()
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=f'Check your id, product with {_id=} not found'
                )

            id, title, description, price, place, created_at = result
            saved_product = SavedTravel(
                id=id, title=title, description=description, price=price, place=place, created_at=created_at
            )



    def get_travel(self, limit: int = 10, q: str = '') -> list[SavedTravel]:
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            query = f"""
                SELECT id, title, description, price, place, created_at
                FROM {self.travel_table_name}
                WHERE title LIKE '%{q}%' OR description LIKE '%{q}%'
                ORDER BY id DESC
                LIMIT {limit}
            """
            data: list[tuple] = cursor.execute(query).fetchall()
        list_of_travels = []
        for result in data:
            id, title, description, price, place, created_at = result
            saved_travels = SavedTravel(

                id=id, title=title, description=description[:30], price=price, place=place, created_at=created_at
            )
            list_of_travels.append(saved_travels)
        return list_of_travels

    def update_travel_price(self, _id: int, new_price: float) -> SavedTravel:
        self.get_travel(_id)


        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            query = f"""
                        UPDATE {self.travel_table_name}
                        SET
                            price = :Price
                        WHERE id = :Id
            """
            cursor.execute(query, {'Price': new_price, 'Id': _id})

        saved_travel = self.get_travel(_id)
        return saved_travel

    def delete_travel(self, _id: int):

        self.get_travel(_id)
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            query = f"""
                        DELETE FROM {self.travel_table_name}
                        WHERE id = :Id
            """
            cursor.execute(query, {'Id': _id})


storage = StorageSQLite('db_1305.sqlite')