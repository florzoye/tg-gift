import requests
import json


class AuthHandler:
    def __init__(self, data):
        self.headers = {
            'accept': '*/*',
            'accept-language': 'ru,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://cdn.tgmrkt.io',
            'priority': 'u=1, i',
            'referer': 'https://cdn.tgmrkt.io/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 YaBrowser/25.4.0.0 Safari/537.36',
        }
        
        self.json_data = {
            'data': data,
            'appId': None,
        }
        
        self.auth_url = 'https://api.tgmrkt.io/api/v1/auth'
        self.response = self._send_auth_request()
    
    def _send_auth_request(self):
        try:
            response = requests.post(
                self.auth_url,
                headers=self.headers,
                json=self.json_data
            )
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.RequestException as e:
            print(f"Auth error: {e}")
            return None
    
    @property
    def auth_data(self):
        return self.response['token']
    
    @property
    def is_authenticated(self):
        return self.response is not None and 'token' in self.response
    
if __name__ == '__main__':
    ins = AuthHandler()
    print(ins.auth_data)

