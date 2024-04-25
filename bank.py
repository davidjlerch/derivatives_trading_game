import random

import numpy as np
from datetime import datetime, timedelta
from derivatives import Call, Put
from market import Asset


class Bank:
    def __init__(self, name, risk_free_rate=0.025):
        self.name = name
        self.risk_free_rate = risk_free_rate
        self.total_value = 0
        self.derivatives_portfolio = []
        self.today = datetime.now().date()  # Initialize today's date

    def sell_option(self, option_type, asset, expiration_date, risk=1):
        """
        Sell an option (either Call or Put) and add it to the bank's derivatives portfolio.

        Parameters:
        option_type (str): Type of option to sell ('Call' or 'Put').
        asset (Asset): Asset object representing the underlying asset.
        expiration_date (str): Expiration date of the option (in YYYY-MM-DD format).

        Returns:
        str: Confirmation message indicating the successful sale of the option.
        """

        # Calculate underlying price as the average of historical prices
        underlying_price = asset.price_history[-1]

        # Calculate risk-free rate (considering a constant rate for simplicity)
        risk_free_rate = 0.025  # Example rate, can be based on historical data or other factors

        # Calculate volatility from historical prices
        returns = np.diff(asset.price_history) / asset.price_history[:-1]
        volatility = np.std(returns) * np.sqrt(252)  # Assuming 252 trading days in a year

        # Calculate time to expiration
        time_to_expiration = (expiration_date - self.today).days / 365.25  # Time in years
        premium = 0
        if option_type.lower() == 'call':
            i = 1
            while premium < risk:
                strike_price = underlying_price * random.uniform(1 - 0.001*i, 1 + 0.001*i)
                option = Call(underlying_asset=asset.name,
                              strike_price=strike_price,
                              expiration_date=expiration_date,
                              underlying_price=underlying_price,
                              time_to_expiration=time_to_expiration,
                              volatility=volatility,
                              risk_free_rate=risk_free_rate
                              )
                premium = option.premium
                i += 1
        elif option_type.lower() == 'put':
            i = 1
            while premium < risk:
                strike_price = underlying_price * random.uniform(1 - 0.001*i, 1 + 0.001*i)
                option = Put(underlying_asset=asset.name,
                             strike_price=strike_price,
                             expiration_date=expiration_date,
                             underlying_price=underlying_price,
                             time_to_expiration=time_to_expiration,
                             volatility=volatility,
                             risk_free_rate=risk_free_rate
                             )
                premium = option.premium
                i += 1
        else:
            raise ValueError("Invalid option type. Please choose 'Call' or 'Put'.")
        self.total_value += option.premium
        self.derivatives_portfolio.append(option)
        return option

    def calculate_portfolio_value(self):
        """
        Calculate the total value of the bank's derivatives portfolio.

        Returns:
        float: Total value of the derivatives portfolio.
        """
        return self.total_value


# Example usage:
if __name__ == "__main__":
    # Create a bank
    bank = Bank(name="ABC Bank", risk_free_rate=0.05)

    # Parameters for option pricing
    underlying_price_ = 100

    # Create assets with variable mean and variance change ranges
    stock_A = Asset(name="Stock A", initial_price=100, mean_change_range=(0.95, 1.05), variance_change_range=(0.8, 1.2))
    stock_B = Asset(name="Stock B", initial_price=50, mean_change_range=(0.9, 1.1), variance_change_range=(0.7, 1.3))

    # Sell options
    bank.sell_option(option_type="Call", asset=stock_A, expiration_date="2024-12-31")
    bank.sell_option(option_type="Put", asset=stock_B, expiration_date="2025-12-31")

    # Calculate portfolio value
    portfolio_value = bank.calculate_portfolio_value()
    print(f"{bank.name}'s derivatives portfolio value: {portfolio_value}")
