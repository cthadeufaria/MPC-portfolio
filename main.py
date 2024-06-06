from market_data import MarketData
from gradient_ascent.mathematical_model import Model
from portfolio_manager import Manager



def main():
    market_data = MarketData()
    model = Model(market_data)
    manager = Manager(model, market_data)
    manager.create_portfolio()



if __name__ == "__main__":
    main()