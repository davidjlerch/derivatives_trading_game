import matplotlib.pyplot as plt


class LivePlot:
    def __init__(self):
        self.fig, self.ax = plt.subplots(2, 1, figsize=(10, 10))
        self.lines_stock = []
        self.lines_player = []
        self.player_asset_values = [[]]

    def initialize_stock_plot(self, assets):
        for asset in assets:
            line, = self.ax[0].plot([], [], label=asset.name)
            self.lines_stock.append(line)
        self.ax[0].set_title("Stock Values Over Time")
        self.ax[0].set_xlabel("Day")
        self.ax[0].set_ylabel("Stock Value")
        self.ax[0].legend()
        self.ax[0].grid(True)

    def initialize_player_plot(self, players):
        for player in players:
            line, = self.ax[1].plot([], [], label=player.name)
            self.lines_player.append(line)
            self.player_asset_values.append([])  # Initialize empty list for each player
        self.ax[1].set_title("Player Asset Values Over Time")
        self.ax[1].set_xlabel("Day")
        self.ax[1].set_ylabel("Asset Value")
        self.ax[1].legend()
        self.ax[1].grid(True)

    def update_stock_plot(self, assets, num_days):
        for i, asset in enumerate(assets):
            stock_values = asset.price_history[:num_days]
            self.lines_stock[i].set_data(range(1, len(stock_values) + 1), stock_values)
        self.ax[0].relim()
        self.ax[0].autoscale_view()
        self.fig.canvas.draw_idle()

    def update_player_plot(self, players, assets, num_days):
        for i, player in enumerate(players):
            asset_values = player.calculate_portfolio_value(assets)
            self.player_asset_values[i].append(asset_values)  # Extend the stored asset values
            self.lines_player[i].set_data(range(1, len(self.player_asset_values[i]) + 1), self.player_asset_values[i])
        self.ax[1].relim()
        self.ax[1].autoscale_view()
        self.fig.canvas.draw_idle()

