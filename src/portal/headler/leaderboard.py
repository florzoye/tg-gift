import requests
from typing import List, Dict, Any
from loguru import logger

portal_auth_token = ''

class PortalTOPActiveGifts:
    def __init__(self):
        self.address = 'https://portals-market.com/api/collections'
        logger.info("Запрашиваем данные по активным коллекциям...")
        self.collection = self.get_response()

    @property
    def headers(self) -> Dict[str, str]:
        return {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ru,en;q=0.9',
            'authorization': portal_auth_token,
            'priority': 'u=1, i',
            'referer': 'https://portals-market.com/collection-list',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "YaBrowser";v="25.4", "Yowser";v="2.5"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-storage-access': 'active',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 YaBrowser/25.4.0.0 Safari/537.36',
        }

    @property
    def params(self) -> Dict[str, str]:
        return {
            'limit': '100',
            'sort_by': 'day_volume desc',
        }

    def get_response(self) -> List[Dict[str, Any]]:
        try:
            response = requests.get(
                self.address,
                params=self.params,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            collections_data = response.json().get('collections', [])

            logger.success(f"Успешно получено {len(collections_data)} коллекций.")
            return [
                {
                    'Name': collection['name'],
                    'ID': collection['id'],
                    'Volume': collection.get('volume', 'N/A'),
                    'Day Volume': collection.get('day_volume', 'N/A'),
                    'Floor Price': collection.get('floor_price', 'N/A'),
                }
                for collection in collections_data
            ]

        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при получении данных: {e}")
            return []
        except (KeyError, ValueError) as e:
            logger.error(f"Ошибка при обработке данных: {e}")
            return []


if __name__ == "__main__":

    analyzer = PortalTOPActiveGifts()
    logger.info("ТОП активных коллекций:")
    for collection in analyzer.collection:
        logger.info(collection)
