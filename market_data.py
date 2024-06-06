"""Class to manage all data workflows from exchanges."""
from binance.exceptions import BinanceAPIException
from exchange_connection import Connection



class MarketData(Connection):
    def __init__(self) -> None:
        super().__init__()


    def get_klines(self, symbol: str, interval: str, limit: int=1000) -> list:
        """Get Historical Klines from Binance API."""
        try:
            return self.client.get_historical_klines(symbol=symbol, interval=interval, limit=limit)
        except BinanceAPIException as e:
            print(e)
            return [-1]