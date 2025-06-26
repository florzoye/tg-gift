import requests
from typing import Dict, Any, Optional, List

portal_auth_token = ''

class PortalCollectionAnalyze:
    def __init__(self, collections_id: List[str]):
        self.endpoint = 'https://portals-market.com/api/nfts/search'
        self.collections = collections_id
        self.collections_data = self.get_all_collections_data()

    @property
    def headers(self) -> Dict[str, str]:
        return {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ru,en;q=0.9',
            'authorization': portal_auth_token,
            'priority': 'u=1, i',
            'referer': 'https://portals-market.com/collection',
            'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "YaBrowser";v="25.4", "Yowser";v="2.5"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-storage-access': 'active',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 YaBrowser/25.4.0.0 Safari/537.36',
        }

    def params(self, collection_id: str) -> Dict[str, str]:
        return {
            'offset': '0',
            'limit': '20',
            'collection_id': collection_id,
        }
    
    def get_collection_data(self, collection_id: str) -> Dict[str, Any]:
        """Получает данные для одной коллекции"""
        try:
            response = requests.get(
                self.endpoint,
                params=self.params(collection_id),
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for collection {collection_id}: {e}")
            return {'results': []}

    def get_all_collections_data(self) -> Dict[str, Dict[str, Any]]:
        """Получает данные для всех коллекций и формирует итоговый словарь"""
        result = {}
        
        for collection_id in self.collections:
            collection_response = self.get_collection_data(collection_id)
            
            if not collection_response.get('results'):
                print(f"No results found for collection {collection_id}")
                result[collection_id] = {
                    'collection_id': collection_id,
                    'nfts_count': 0,
                    'nfts': [],
                    'floor_price': None
                }
                continue
                
            nfts_info = []
            valid_prices = []
            
            for nft in collection_response['results']:
                price = nft.get('price')
                nft_info = {
                    'FloorPrice': price,
                    'owner_id': nft.get('owner_id'),
                    'id': nft.get('id'),
                    'name': nft.get('name', ''),
                    'collection_id': collection_id
                }
                nfts_info.append(nft_info)
                
                if price is not None and str(price).strip():
                    try:
                        valid_prices.append(float(price))
                    except (ValueError, TypeError):
                        pass
            
            result[collection_id] = {
                'collection_id': collection_id,
                'nfts_count': len(nfts_info),
                'nfts': nfts_info,
                'FloorPrice': min(valid_prices) if valid_prices else None
            }
        
        return result

    def get_collections_info(self) -> Dict[str, Dict[str, Any]]:
        """Возвращает полную информацию по всем коллекциям"""
        return self.collections_data

