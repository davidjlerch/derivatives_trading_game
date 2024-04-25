class Player:
    def __init__(self, name, initial_cash):
        self.name = name
        self.cash = initial_cash
        self.stocks_portfolio = {}
        self.derivatives_portfolio = []

    def buy_stock(self, asset, quantity):
        cost = quantity * asset.price_history[-1] + 5
        if cost > self.cash:
            print(f"{self.name} does not have enough cash to buy {quantity} stocks of {asset.name}.")
            return
        if asset.name in self.stocks_portfolio:
            self.stocks_portfolio[asset.name] += quantity
        else:
            self.stocks_portfolio[asset.name] = quantity
        self.cash -= cost
        print(f"{self.name} bought {quantity} stocks of {asset.name}.")

    def sell_stock(self, asset, quantity):
        if asset.name not in self.stocks_portfolio:
            print(f"{self.name} does not own any stocks of {asset.name}.")
            return
        if self.stocks_portfolio[asset.name] < quantity:
            print(f"{self.name} does not have enough stocks of {asset.name} to sell.")
            return
        self.stocks_portfolio[asset.name] -= quantity
        sale_proceeds = quantity * asset.price_history[-1] - 5
        self.cash += sale_proceeds
        print(f"{self.name} sold {quantity} stocks of {asset.name} for ${sale_proceeds}.")

    def buy_option(self, option, quantity):
        cost = quantity * option.premium
        if cost > self.cash:
            print(f"{self.name} does not have enough cash to buy {quantity} {option.type} options.")
            return
        self.derivatives_portfolio.extend([option] * quantity)
        self.cash -= cost
        print(f"{self.name} bought {quantity} {option.type} options for {option.underlying_asset}.")

    def sell_option(self, option_type, asset, quantity):
        sold = 0
        for _ in range(quantity):
            for option in self.derivatives_portfolio:
                if option.type == option_type.lower() and option.underlying_asset == asset.name and sold < quantity:
                    self.cash += option.premium
                    self.derivatives_portfolio.remove(option)
                    sold += 1

    def calculate_portfolio_value(self, assets):
        """
        Calculate the total value of the player's portfolio.

        Returns:
        float: Total value of the portfolio.
        """
        total_value = 0
        total_value += self.cash
        if len(self.stocks_portfolio.items()) > 0:
            for asset_name, quantity in self.stocks_portfolio.items():
                total_value += quantity * [asset.price_history[-1] for asset in assets if asset.name == asset_name][0]  # Assuming the latest price for valuation
        return total_value
