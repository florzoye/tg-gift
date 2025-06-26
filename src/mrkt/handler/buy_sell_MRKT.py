import requests
from loguru import logger



class MRKTTraiding:
    def __init__(self, 
                 auth_token: str, 
                 gift_data: dict): #айди и флор прайс
        self.base_url = 'https://api.tgmrkt.io/api/v1/gifts'
        self.return_gift_endpoint = f'{self.base_url}/return'
        self.buy_endpoint = f'{self.base_url}/buy'
        self.sale_endpoint = f'{self.base_url}/sale'
        self.auth = auth_token
        self.data = gift_data


    @property
    def buy_json_data(self):
        return {
                    'ids': [
                        self.data['id'],
                    ],
                    'prices': {
                        self.data['id']: self.data['FloorPrice'],
                    },
                }
    
    @property
    def sale_json_data(self):
        return  {
                    'ids': [
                        self.data['id'],
                    ],
                    'price': self.data['FloorPrice'], #nTON
                }


    @property
    def return_json_data(self):
        return {
                    'ids': [
                        self.data['id'],
                    ],
                }

    @property
    def headers(self):
        return {
                    'accept': '*/*',
                    'accept-language': 'ru,en;q=0.9',
                    'authorization': self.auth,
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

    def buy_gift(self) -> bool:
        try:
            response = requests.post(
                self.buy_endpoint,
                headers=self.headers,
                json=self.buy_json_data,
                timeout=10
            )
            response.raise_for_status()
            logger.success(f"Успешно куплен подарок {self.data['id']}")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при покупке подарка {self.data['id']}: {e}")
            return False

    def place_for_sale(self) -> bool:
        try:
            response = requests.post(
                self.sale_endpoint,
                headers=self.headers,
                json=self.sale_json_data,
                timeout=10
            )
            response.raise_for_status()
            logger.success(f"Подарок {self.data['id']} выставлен на продажу")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при выставлении на продажу {self.data['id']}: {e}")
            return False

    def return_gift(self) -> bool:
        try:
            response = requests.post(
                self.return_gift_endpoint,
                headers=self.headers,
                json=self.return_json_data,
                timeout=10
            )
            response.raise_for_status()
            logger.success(f"Подарок {self.data['id']} возвращен владельцу")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при возврате подарка {self.data['id']}: {e}")
            return False



