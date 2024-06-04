"""Any connection channel with available exchanges."""
import os, requests, hmac, hashlib, time
from urllib.parse import urlencode
from binance import Client



class Connection:
    def __init__(self, environment) -> None:
        self.environment = environment
        self.endpoints = {}
        endpoints = {
            'test' : '/api/v3/ping',
            'server_time' : '/api/v3/time',
            'exchange_info' : '/api/v3/exchangeInfo',
            'order_book' : '/api/v3/depth',
            'candlestick' : '/api/v3/klines',
            'avg_price' : '/api/v3/avgPrice',
            'best_price' : '/api/v3/ticker/bookTicker',
            'acc_info' : '/api/v3/account',
            'acc_snapshot' : '/sapi/v1/accountSnapshot',
            'price' : '/api/v3/ticker/price',
            'price_hist' : '/api/v3/historicalTrades',
            'order' : '/api/v3/order',
            'test_order' : '/api/v3/order/test',
            'trades' : '/api/v3/myTrades',
            'test_new_order' : '/api/v3/order/test',
            'new_order' : '/api/v3/order',
            'options_exchange_info' : '/eapi/v1/exchangeInfo',
            'options_order_book' : '/eapi/v1/depth',
            'options_mark_price' : '/eapi/v1/mark',
            'options_klines': '/eapi/v1/klines', 
        }
        if self.environment == 'test':
            main_endpoint = 'https://testnet.binance.vision'
            options_endpoint = 'https://testnet.binancefuture.com'
            self.auth_dict = {
                'key' : os.environ.get('TEST_KEY'),
                'skey' : os.environ.get('TEST_SKEY'),
            }
        elif self.environment == 'production':
            main_endpoint = 'https://api1.binance.com'
            options_endpoint = 'https://eapi.binance.com'
            self.auth_dict = {
                'key' : os.environ.get('SPOT_KEY'),
                'skey' : os.environ.get('SPOT_SKEY'),
            }
        # complete endpoints strings
        for endpoint in endpoints:
            if endpoint[0:7] == 'options':
                self.endpoints[endpoint] = options_endpoint + endpoints[endpoint]
            else:
                self.endpoints[endpoint] = main_endpoint + endpoints[endpoint]
        self.ping()
        self.client = Client(self.auth_dict['key'], self.auth_dict['skey'])


    def ping(self) -> None:
        """Ping the api server."""
        r = requests.get(self.endpoints['test'])
        if str(r) == "<Response [200]>":
            print('Connected to Binance API.', "\n")
        else:
            raise Exception("Connection with exchange server unsuccessful.")


    def sha256_signature(self, endpoint_params) -> None:
        """Create hashed sign dict for instantiated object."""
        secret = self.auth_dict['skey']
        params = urlencode(endpoint_params)
        hashedsig = hmac.new(secret.encode('utf-8'), params.encode('utf-8'), hashlib.sha256).hexdigest()
        self.hashedsig_dict = {
            "signature" : hashedsig
        }


    def get_timestamp(self):
        t = int(time.time()*1000)
        servertime = requests.get(self.endpoints['server_time'])
        st = servertime.json()['serverTime']
        return st, t