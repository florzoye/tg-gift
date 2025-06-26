import requests
from loguru import logger




class PortalTraiding:
    def __init__(self,
                 gift: dict):
        self.data = gift
        self.base_endpoint = 'https://portals-market.com/api/'
        self.list_endpoint = f'{self.base_endpoint}nfts/bulk-list'
        self.buy_endpoint = f'{self.base_endpoint}api/nfts'

    @property
    def list_json_data(self):
        return {
                    'nft_prices': [
                        {
                            'nft_id': self.data['id'],  # цена в TON
                            'price': self.data['FloorPrice'],
                        },
                    ],
                }
    
    @property
    def buy_json_data(self):
        return {
                    'nft_details': [
                        {
                            'id': self.data['id'],
                            'owner_id': self.data['owner_id'],
                            'price': self.data['FloorPrice'],
                        },
                    ],
                }


    @property
    def headers(self):
        return {
                    'accept': 'application/json, text/plain, */*',
                    'accept-language': 'ru,en;q=0.9',
                    'authorization': 'tma user=',
                    'content-type': 'application/json',
                    'origin': 'https://portals-market.com',
                    'priority': 'u=1, i',
                    'referer': 'https://portals-market.com/my-gifts',
                    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "YaBrowser";v="25.4", "Yowser";v="2.5"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-storage-access': 'active',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 YaBrowser/25.4.0.0 Safari/537.36',
                }
    
    def list_gift(self, ):
        try:
            response = requests.post(self.list_endpoint,
                                      headers=self.headers,
                                        json=self.list_json_data)
            if response.status_code == 200:
                logger.success(f'Выставлен подарок с id - {self.data['id']}, цена - {self.data['Floor']}')

        except Exception as e:
            logger.error(e)

    def buy_gift(self):
        try:
            response = requests.post(self.buy_endpoint,
                                     headers=self.headers,
                                     json=self.buy_json_data)
            if response.status_code == 200:
                logger.success(f'''Подарок с id - {self.data['id']}, успешно куплен \n 
                               цена - {self.data['Floor']}''')
        except Exception as e:
            logger.error(e)

    