import sqlite3
from contextlib import contextmanager
from .handlers.gifts_info import InfoTableHandler  # относительный импорт
from .handlers.spread import SpreadTableHandler   # относительный импорт

class DatabaseManager:
    def __init__(self, db_path: str):
        self.db_path = db_path

    @contextmanager
    def get_cursor(self):
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def get_info_handler(self):
        with self.get_cursor() as cursor:
            return InfoTableHandler(cursor)