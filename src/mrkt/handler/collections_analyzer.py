import requests
from pprint import pprint
import time
from loguru import logger

class MRKTAnalyzeCollections:
    def __init__(self, 
                 collection: str,
                 auth_token: str):
        self.auth_token = auth_token
        self.address = 'https://api.tgmrkt.io/api/v1/gifts/saling'
        self.collection = collection
        self.cursor = ''

    @property
    def json_data(self):
        return {
            'count': 20,
            'cursor': self.cursor,
            'collectionNames': [self.collection],
            'modelNames': [],
            'backdropNames': [],
            'symbolNames': [],
            'minPrice': None,
            'maxPrice': None,
            'mintable': None,
            'number': None,
            'ordering': 'Price',
            'lowToHigh': True,
            'isPremarket': None,
            'query': None,
        }

    @property
    def headers(self):
        return {
            'accept': '*/*',
            'accept-language': 'ru,en;q=0.9',
            'authorization': self.auth_token,
            'content-type': 'application/json',
            'origin': 'https://cdn.tgmrkt.io',
            'priority': 'u=1, i',
            'referer': 'https://cdn.tgmrkt.io/',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "YaBrowser";v="25.4", "Yowser";v="2.5"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 YaBrowser/25.4.0.0 Safari/537.36',
        }
    

    def gift_info(self, 
                  number: int | None = None,
                   id: str | None = None
                   ):
        found = False
        while True:
            response = requests.post(self.address, 
                                     headers=self.headers, 
                                     json=self.json_data)
            
            if response.status_code != 200:
                print(f"Ошибка запроса: {response.status_code}")
                break

            response_data = response.json()
            gifts = response_data.get("gifts", [])
            
            for gift in gifts:
                if number and str(gift.get('number')) == str(number):
                    logger.info("\nСтикер найден по number!")
                    found = True
                    break
                if id and gift.get('id') == id:
                    logger.info("\nСтикер найден по ID!")
                    found = True
                    break
            
            if found:
                break
                
            self.cursor = response_data.get("cursor")
            if not self.cursor:
                logger.warning("\nСтикер не найден. Достигнут конец списка.")
                break

            time.sleep(0.5)

    def find_min_gift_info(self) -> dict | None:
        min_price_nTON = None
        
        try:
            response = requests.post(self.address, headers=self.headers, json=self.json_data)
            
            if response.status_code != 200:
                logger.warning(f"Ошибка запроса: {response.status_code}")
                return None

            response_data = response.json()
            gifts = response_data.get("gifts", [])
            min_price_nTON = gifts[0]['salePrice']
            id_min_gift = gifts[0]['id']

            return {'FloorPrice': min_price_nTON,
                    'id':id_min_gift}
        
        except Exception as e:
            logger.error(f'Произошла ошибка при попытке найти самый дешовый стикер - {e}')
            

       