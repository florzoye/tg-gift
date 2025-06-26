import sqlite3
from typing import List, Dict
from db.handlers.schemas import (
    get_info_table_sql,
    get_select_id_by_floor_price_sql,
    get_update_info_sql,
    get_insert_info_sql,
    get_select_column_sql,
    get_select_all_sql
)

class InfoTableHandler:
    def __init__(self, cursor: sqlite3.Cursor):
        self.cursor = cursor

    def create_table(self, table_name: str) -> None:
        self.cursor.execute(get_info_table_sql(table_name))

    def add_info(self, table_name: str, gift: Dict) -> None:
       
        self.cursor.execute(
            get_select_id_by_floor_price_sql(table_name), 
            (gift['FloorPrice'],)
        )
        existing = self.cursor.fetchone()
        
        if existing:
            self.cursor.execute(
                get_update_info_sql(table_name),
                gift
            )
        else:
            self.cursor.execute(
                get_insert_info_sql(table_name),
                gift
            )
            
    def get_column_data(self, table_name: str, column_name: str) -> List:
        self.cursor.execute(
            get_select_column_sql(table_name, column_name)
        )
        return [row[0] for row in self.cursor.fetchall()]
    
    def get_all(self, table_name: str) -> List[Dict]:
        self.cursor.execute(get_select_all_sql(table_name))
        columns = [col[0] for col in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]
    
    def clear_table(self, table_name):
        self.cursor.execute(f"DELETE FROM {table_name}")