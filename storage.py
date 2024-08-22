from abc import ABC, abstractmethod
import sqlite3

from schemas import NewProduct


class BaseStorageProduct(ABC):
    @abstractmethod
    def create_product(self, new_product: NewProduct):
        pass

    @abstractmethod
    def get_product(self, _id: int):
        pass

    @abstractmethod
    def get_products(self, limit: int):
        pass

    @abstractmethod
    def update_product_price(self, _id: int, new_price: float):
        pass

    @abstractmethod
    def delete_product(self, _id: int):
        pass


class StorageSQLite(BaseStorageProduct):

    def _create_table(self):
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            query = f"""
                CREATE TABLE IF NOT EXISTS {self.product_table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    description TEXT,
                    price REAL,
                    cover TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP 
                )
            """
            cursor.execute(query)

    def __init__(self, database_name: str):
        self.database_name = database_name
        self.product_table_name = 'products'
        self._create_table()

    def create_product(self, new_product: NewProduct):
        pass

    def get_product(self, _id: int):
        pass

    def get_products(self, limit: int):
        pass

    def update_product_price(self, _id: int, new_price: float):
        pass

    def delete_product(self, _id: int):
        pass


storage = StorageSQLite('db_1305.sqlite')