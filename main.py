import time
from datetime import datetime, timedelta
import random
import matplotlib.pyplot as plt
import numpy as np

from market import Asset, Market
from bank import Bank
from player import Player
from plotting import LivePlot  # Import the LivePlot class
from derivatives import Call, Put


def initialize_assets(num_assets):
    """
    Initialize assets for the market.

    Parameters:
    num_assets (int): Number of assets to initialize.

    Returns:
    list: List of initialized Asset objects.
    """
    assets = []
    for i in range(num_assets):
        lower = random.uniform(0.95, 0.99)
        upper = random.uniform(1.01, 1.07)
        asset = Asset(name=f"Asset {i+1}", initial_price=random.randint(95, 105),
                      mean_change_range=(lower, upper),
                      variance_change_range=(0.005, (upper / lower - 1)))
        assets.append(asset)
    return assets


def initialize_players():
    """
    Initialize players for the simulation.

    Returns:
    tuple: Two initialized Player objects.
    """
    player1 = Player(name="Player 1", initial_cash=1000)
    player2 = Player(name="Player 2", initial_cash=1000)
    return player1, player2


def initialize_bank():
    """
    Initialize the bank for the simulation.

    Returns:
    Bank: Initialized Bank object.
    """
    return Bank(name="ABC Bank")


def initialize_simulation():
    """
    Initialize assets, players, and bank for the simulation.

    Returns:
    tuple: Initialized assets, players, and bank.
    """
    assets = initialize_assets(5)
    bank = initialize_bank()
    player1, player2 = initialize_players()
    return assets, bank, player1, player2


def simulate_market(assets, bank, player1, player2, num_days, live_plotter=None, player3=None):
    """
    Simulate the market based on asset value changes.

    Parameters:
    assets (list): List of Asset objects.
    bank (Bank): Bank object.
    player1 (Player): Player 1 object.
    player2 (Player): Player 2 object.
    num_days (int): Number of days to simulate.
    """
    today = datetime.now().date()

    for day in range(num_days):
        expiration_date = today + timedelta(weeks=2)
        # Update asset prices in the market
        for asset in assets:
            asset.update_price()

        # Player 1 buys stocks
        for asset in assets:
            quantity = random.randint(0, 2)  # Random quantity
            player1.buy_stock(asset, quantity)

        # Player 2 buys derivatives from the bank
        for asset in assets:
            option_type = random.choice(['Call', 'Put'])  # Random option type
            option = bank.sell_option(option_type, asset, expiration_date)
            quantity = random.randint(0, int(option.premium))  # Random quantity
            if quantity:
                player2.buy_option(option, 1)

        # Execute expired derivatives
        execute_expired_derivatives(bank, today + timedelta(days=day), assets, player2)

        if live_plotter is not None:
            plot(live_plotter, assets, day, player1, player2, player3)

        # Allow the third player to interactively buy stocks and derivatives
        if player3 is not None:
            print("\nThird Player:")
            interactive_buy(player3, assets, bank, today + timedelta(days=day))

        # Print portfolio values of players and bank
        print(f"Day {day+1}:")
        print(f"{player1.name}'s portfolio value: {player1.calculate_portfolio_value(assets)}")
        print(f"{player2.name}'s portfolio value: {player2.calculate_portfolio_value(assets)}")
        print(f"{player3.name}'s portfolio value: {player3.calculate_portfolio_value(assets)}")
        print(f"{bank.name}'s derivatives portfolio value: {bank.calculate_portfolio_value()}")
        print("-----------------------")


def interactive_buy(player, assets, bank, today):
    """
    Allow a player to interactively buy or sell stocks and derivatives through the command line.

    Parameters:
    player (Player): The player object making the purchases.
    assets (list): List of Asset objects available for purchase.
    bank (Bank): The bank object from which derivatives can be purchased.
    """
    print(f"{player.name}, you have ${player.cash}.")

    # Allow the player to buy or sell stocks
    while True:
        try:
            action = input("(B)uy or (S)ell stocks or (L)ist asset (or Enter to skip): ").upper()
            if action == '':
                break
            elif action == 'B':
                asset_number, quantity = input("Enter asset number and quantity (separated by space): ").split()
                asset_number = int(asset_number)
                quantity = int(quantity)
                asset = assets[asset_number - 1]
                if quantity <= 0:
                    raise ValueError("Please enter a positive integer for buying stocks.")
                elif quantity * asset.price_history[-1] > player.cash:
                    raise ValueError("Insufficient funds to buy the stocks.")
                player.buy_stock(asset, quantity)
            elif action == 'S':
                asset_number, quantity = input("Enter asset number and quantity (separated by space): ").split()
                asset_number = int(asset_number)
                quantity = int(quantity)
                asset = assets[asset_number - 1]
                if quantity <= 0:
                    raise ValueError("Please enter a positive integer for selling stocks.")
                player.sell_stock(asset, quantity)
            elif action == 'L':
                print("Stocks:")
                for stock, quantity in player.stocks_portfolio.items():
                    print(f"{stock}: {quantity}")
            else:
                raise ValueError("Invalid action. Please enter 'B' to buy or 'S' to sell stocks.")
        except ValueError as e:
            print(e)
            continue

    # Allow the player to buy derivatives from the bank
    while True:
        try:
            action = input("(B)uy or (S)ell or (L)ist options (or Enter to skip): ").upper()
            if action == '':
                break
            elif action == 'B':
                option_type, asset_number, quantity, risk = input("Enter Call/Put, asset number, quantity, and risk (separated by space): ").split()
                asset_number = int(asset_number)
                quantity = int(quantity)
                risk = float(risk)
                asset = assets[asset_number - 1]
                if option_type not in ['Call', 'Put']:
                    raise ValueError("Invalid option type. Please choose 'Call' or 'Put'.")
                duration = input("Enter duration in days: ")
                expiration_date = today + timedelta(days=float(duration))
                if not expiration_date:
                    raise ValueError("Expiration date is required.")
                option = bank.sell_option(option_type, asset, expiration_date, risk=risk)
                player.buy_option(option, quantity)
            elif action == 'S':
                option_type, asset_number, quantity = input("Enter Call/Put, asset number, quantity (separated by space): ").split()
                asset_number = int(asset_number)
                quantity = int(quantity)
                asset = assets[asset_number - 1]
                player.sell_option(option_type, asset, quantity)
            elif action == 'L':
                print("Options:")
                for option in player.derivatives_portfolio:
                    print(f"{option.type} on {option.underlying_asset} until {option.expiration_date} "
                          f"with strike price {option.strike_price}")
        except ValueError as e:
            print(e)
            continue


def execute_expired_derivatives(bank, current_date, assets, player):
    """
    Execute expired derivatives in the bank's portfolio.

    Parameters:
    bank (Bank): Bank object.
    current_date (datetime.date): Current date.
    """
    expired_derivatives = [derivative for derivative in bank.derivatives_portfolio if derivative.expiration_date <= current_date]
    for derivative in expired_derivatives:
        payoff = derivative.payoff([asset.price_history[-1] for asset in assets
                                    if derivative.underlying_asset == asset.name][0])
        if derivative in player.derivatives_portfolio:
            player.cash += payoff

        bank.derivatives_portfolio.remove(derivative)


def plot(live_plotter, assets, day, player1, player2, player3):
    # Update the plots
    live_plotter.update_stock_plot(assets, day + 1)
    if player3 is not None:
        live_plotter.update_player_plot([player1, player2, player3], assets, day + 1)
    else:
        live_plotter.update_player_plot([player1, player2], assets, day + 1)

    # Add a pause to show the plot for each day
    plt.pause(1)


def main():
    # Initialize assets, players, and bank
    assets, bank, player1, player2 = initialize_simulation()
    player3 = Player(name="Player 3", initial_cash=1000)

    # Initialize live plotting
    live_plotter = LivePlot()

    # Initialize the plots for stock values and player asset values
    live_plotter.initialize_stock_plot(assets)
    live_plotter.initialize_player_plot([player1, player2, player3])

    # Simulate market changes for a certain number of days
    num_days = 30
    # Simulate market changes for the current day
    simulate_market(assets, bank, player1, player2, num_days, live_plotter, player3=player3)

    # Keep the plots open after the simulation finishes
    plt.show()


if __name__ == "__main__":
    main()
