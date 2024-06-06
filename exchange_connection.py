"""Connection channel object with available exchanges."""
import os

from binance import Client
from binance.exceptions import BinanceAPIException



class Connection:
    def __init__(self) -> None:
        auth_dict = {
            'key' : os.environ.get('SPOT_KEY'),
            'skey' : os.environ.get('SPOT_SKEY'),
        }
        self.client = Client(auth_dict['key'], auth_dict['skey'])
        self.system_status = self.get_system_status()


    def ping(self) -> dict:
        try:
            return self.client.ping()
        except BinanceAPIException as e:
            print(e)
            return {-1: 'Error'}
        
    
    def get_system_status(self) -> dict:
        try:
            return self.client.get_system_status()
        except BinanceAPIException as e:
            print(e)
            return {-1: 'Error'}