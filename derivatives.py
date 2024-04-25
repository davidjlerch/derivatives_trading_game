import math
from scipy.stats import norm


class Derivative:
    def __init__(self, underlying_asset, strike_price, expiration_date, underlying_price, time_to_expiration,
                 volatility, risk_free_rate):
        self.underlying_asset = underlying_asset
        self.strike_price = strike_price
        self.expiration_date = expiration_date
        self.premium = None
        self.calculate_premium(underlying_price, strike_price, time_to_expiration, volatility, risk_free_rate)

    def payoff(self, price):
        pass  # Placeholder method, to be implemented in child classes

    def calculate_premium(self, underlying_price, strike_price, time_to_expiration, volatility, risk_free_rate):
        """
        Calculates the premium of an option using the Black-Scholes model.

        Parameters:
        underlying_price (float): Current market price of the underlying asset.
        strike_price (float): Price at which the option holder can buy (for call options) or sell (for put options) the underlying asset.
        time_to_expiration (float): Time remaining until the option contract expires, in years.
        volatility (float): Volatility of the underlying asset's price.
        risk_free_rate (float): Risk-free interest rate prevailing in the market.

        Returns:
        float: Estimated premium of the option.
        """
        # Calculate d1 and d2
        d1 = (math.log(underlying_price / strike_price) + (
                    risk_free_rate + 0.5 * volatility ** 2) * time_to_expiration) / (
                         volatility * math.sqrt(time_to_expiration))
        d2 = d1 - volatility * math.sqrt(time_to_expiration)

        # Calculate premium using the Black-Scholes formula
        premium = underlying_price * norm.cdf(d1) - strike_price * math.exp(
            -risk_free_rate * time_to_expiration) * norm.cdf(d2)

        self.premium = premium

    def print_info(self):
        print("Option Type:", type(self).__name__, "Underlying Asset:", self.underlying_asset,
              "Strike Price:", self.strike_price, "Expiration Date:", self.expiration_date, "Premium:", self.premium)


class Call(Derivative):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'call'

    def payoff(self, price):
        return max(0, price - self.strike_price)


class Put(Derivative):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = 'put'

    def payoff(self, price):
        return max(0, self.strike_price - price)


# Example usage:
if __name__ == "__main__":
    # Parameters for option pricing
    underlying_price_ = 100
    strike_price_ = 100
    time_to_expiration_ = 1  # Time to expiration in years
    volatility_ = 0.5
    risk_free_rate_ = 0.05

    call_ = Call(underlying_asset='Call Asset', strike_price=strike_price_, expiration_date='2024-12-31',
                 underlying_price=underlying_price_, time_to_expiration=time_to_expiration_, volatility=volatility_,
                 risk_free_rate=risk_free_rate_)
    print("Call option premium:", call_.premium)
