import sqlite3
from typing import List, Dict, Union
from db.handlers.schemas import (
    get_create_table_sql,
    get_insert_spread_sql,
    get_select_all_sql,
    get_select_max_profit_sql
)

class SpreadTableHandler:
    def __init__(self, cursor: sqlite3.Cursor):
        self.cursor = cursor

    def create_table(self, table_name: str):
        self.cursor.execute(get_create_table_sql(table_name))

    def calculate_and_insert_spreads(self, table_name: str, data: List[Dict[str, Union[str, float]]]):
        insert_sql = get_insert_spread_sql(table_name)
        
        for item in data:
            try:
                # Приводим обе цены к TON
                price_portal = int(item['PricePortal']) 
                price_mrkt = int(item['PriceMRKT']) / 1e9

                spread_mrkt_to_portal = price_mrkt - price_portal
                spread_portal_to_mrkt = price_portal - price_mrkt
                spread_diff_ton = abs(spread_mrkt_to_portal)

                # Процент от меньшей цены
                spread_diff_percent = round((spread_diff_ton / min(price_portal, price_mrkt)) * 100, 3)

                # Условные комиссии
                GAS_FEE = 0.1  # условно
                MRKT_FEE = 0.10  # 10%
                PORTAL_FEE = 0.05  # 5%

                # Вычисляем прибыль в зависимости от направления
                if spread_portal_to_mrkt > spread_mrkt_to_portal:
    # Купить на MRKT, продать на Portal
                    received = price_portal - 0.1
                    cost = price_mrkt + price_mrkt * 0.10
                    total_profit = received - cost
                else:
                    # Купить на Portal, продать на MRKT
                    received = price_mrkt - price_mrkt * 0.10
                    cost = price_portal + 0.1
                    total_profit = received - cost

                self.cursor.execute(
                        insert_sql,
                        (
                            item['id'],
                            item['source'],  # 🧩 вот это — новое поле
                            item['NameColl'],
                            round(price_portal, 6),
                            round(price_mrkt, 6),
                            round(spread_mrkt_to_portal, 6),
                            round(spread_portal_to_mrkt, 6),
                            round(spread_diff_ton, 6),
                            spread_diff_percent,
                            round(total_profit, 6)
                        )
                )


            except Exception as e:
                print(f"[ERROR] Ошибка при расчёте spread для {item['NameColl']}: {e}")


    def get_all_spreads(self, table_name: str) -> List[Dict]:
        self.cursor.execute(get_select_all_sql(table_name))
        columns = [col[0] for col in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]

    def get_max_profit_opportunity(self, table_name: str) -> Dict:
        self.cursor.execute(get_select_max_profit_sql(table_name))
        columns = [col[0] for col in self.cursor.description]
        result = self.cursor.fetchone()
        return dict(zip(columns, result)) if result else None