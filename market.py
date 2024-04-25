import random


class Asset:
    def __init__(self, name, initial_price, mean_change_range, variance_change_range):
        self.name = name
        self.price_history = [initial_price]
        self.mean_change_range = mean_change_range
        self.variance_change_range = variance_change_range

    def update_price(self):
        # Simulate price evolution with variable mean and variance
        mean_change = random.uniform(*self.mean_change_range)
        variance_change = random.uniform(*self.variance_change_range)

        # Ensure non-negative prices
        new_price = max(0.001, self.price_history[-1] * random.uniform(mean_change - variance_change, mean_change + variance_change))
        self.price_history.append(new_price)


class Market:
    def __init__(self):
        self.assets = {}

    def add_asset(self, asset):
        self.assets[asset.name] = asset

    def update_prices(self):
        for asset in self.assets.values():
            asset.update_price()


# Example usage:
if __name__ == "__main__":
    # Create assets with variable mean and variance change ranges
    stock_A = Asset(name="Stock A", initial_price=100, mean_change_range=(0.95, 1.05), variance_change_range=(0.8, 1.2))
    stock_B = Asset(name="Stock B", initial_price=50, mean_change_range=(0.9, 1.1), variance_change_range=(0.7, 1.3))

    # Create market
    market = Market()
    market.add_asset(stock_A)
    market.add_asset(stock_B)

    # Update prices for some time steps
    for _ in range(10):
        market.update_prices()

    # Print price history of each asset
    for asset_name, asset in market.assets.items():
        print(f"{asset_name} price history:", asset.price_history)
