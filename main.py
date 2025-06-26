import time
from loguru import logger
from tqdm import tqdm
from tabulate import tabulate


from db.manager import DatabaseManager
from db.handlers import InfoTableHandler, SpreadTableHandler

from src.portal.headler.collections_analyze import PortalCollectionAnalyze
from src.portal.headler.leaderboard import PortalTOPActiveGifts
from src.portal.headler.buy_sell_PORTAL import PortalTraiding

from src.mrkt.handler.auth import AuthHandler
from src.mrkt.handler.collections_analyzer import MRKTAnalyzeCollections



def main():
    logger.add("debug.log", format="{time} {level} {message}", level="DEBUG", rotation="500 KB", compression="zip")
    logger.info("Запуск программы")

    db_manager = DatabaseManager('database.db')

    with db_manager.get_cursor() as cursor:
        handler = InfoTableHandler(cursor)
        handler.create_table('portal_gifts')
        handler.create_table('market_gifts')

    while True:
        try:
            logger.info("Начинается новый цикл сбора данных")

            collections_raw = PortalTOPActiveGifts().collection
            collection_ids = [item['ID'] for item in collections_raw]
            logger.debug(f"Получено {len(collection_ids)} коллекций с портала")

            collections_data = {}
            for collection_id in tqdm(collection_ids, desc="Сбор данных с портала"):
                collection_info = PortalCollectionAnalyze([collection_id]).get_collections_info()
                collections_data.update(collection_info)

            portal_data = []
            for collection_id, data in tqdm(collections_data.items(), desc="Обработка portal данных"):
                if data['nfts']:
                    cheapest_nft = min(
                        data['nfts'],
                        key=lambda x: float(x['FloorPrice']) if x.get('FloorPrice') else float('inf')
                    )
                    portal_data.append({
                        'id': cheapest_nft['id'],
                        'name': cheapest_nft.get('name', ''),
                        'FloorPrice': cheapest_nft['FloorPrice']
                    })

            with db_manager.get_cursor() as cursor:
                handler = InfoTableHandler(cursor)
                for gift in tqdm(portal_data, desc="Сохранение portal_gifts"):
                    handler.add_info('portal_gifts', gift)

            logger.info("Данные с портала сохранены")

            auth = AuthHandler().auth_data
            market_data = []

            for gift in tqdm(portal_data, desc="Сбор данных с MRKT"):
                try:
                    mrkt = MRKTAnalyzeCollections(auth_token=auth, collection=gift['name'])
                    data_gift_min = mrkt.find_min_gift_info()
                    market_data.append({
                        'id': data_gift_min['id'],
                        'name': gift['name'],
                        'FloorPrice': data_gift_min['FloorPrice']
                    })
                except Exception as e:
                    logger.warning(f"Ошибка при получении данных с MRKT для {gift['name']}: {e}")

            with db_manager.get_cursor() as cursor:
                handler = InfoTableHandler(cursor)
                for gift in tqdm(market_data, desc="Сохранение market_gifts"):
                    handler.add_info('market_gifts', gift)

            logger.info("Данные с MRKT сохранены")

            with db_manager.get_cursor() as cursor:
                spread_handler = SpreadTableHandler(cursor)
                spread_handler.create_table('spreads')

            with db_manager.get_cursor() as cursor:
                info_handler = InfoTableHandler(cursor)
                portal_prices = info_handler.get_all('portal_gifts')
                market_prices = info_handler.get_all('market_gifts')

            spread_data = []
            for portal_item in portal_prices:
                for market_item in market_prices:
                    if portal_item['name'] == market_item['name']:
                        price_portal = float(portal_item['FloorPrice'])
                        price_market = float(market_item['FloorPrice']) / 1e9

                        if price_portal < price_market:
                            nft_id = portal_item['id']  
                            source = 'portal'
                        else:
                            nft_id = market_item['id']  
                            source = 'market'

                        spread_data.append({
                            'id': nft_id,
                            'source': source,  
                            'NameColl': portal_item['name'],
                            'PricePortal': portal_item['FloorPrice'],
                            'PriceMRKT': market_item['FloorPrice']
                        })

            with db_manager.get_cursor() as cursor:
                spread_handler = SpreadTableHandler(cursor)
                spread_handler.calculate_and_insert_spreads('spreads', spread_data)

            with db_manager.get_cursor() as cursor:
                spread_handler = SpreadTableHandler(cursor)
                best_opportunity = spread_handler.get_max_profit_opportunity('spreads')
                all_spreads = spread_handler.get_all_spreads('spreads')


            profitable_spreads = [
                spread for spread in all_spreads
                if spread['TotalProfit'] is not None and spread['TotalProfit'] >= 0.2
            ]

            if profitable_spreads:
                logger.info("Найдено прибыльных спредов (TotalProfit >= 0.2):")

                table_data = [
                    [spread['NameColl'], spread.get('id', 'N/A'), spread.get('source', 'N/A'), round(spread['TotalProfit'], 3)]
                    for spread in profitable_spreads
                ]
                table_headers = ["Название", "ID", "Источник", "Total Profit"]


                table = tabulate(table_data, headers=table_headers, tablefmt="fancy_grid", stralign="left", floatfmt=".3f")
                print(table)  
            else:
                logger.info("Прибыльных спредов (TotalProfit >= 0.2) не найдено.")

        except Exception as e:
            logger.exception(f"Неожиданная ошибка в основном цикле: {e}")
            time.sleep(3)


if __name__ == "__main__":
    main()
