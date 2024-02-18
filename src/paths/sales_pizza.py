from utils.utils import beautiful_header
from board import Board

class SalesPizza:
    """
    This path is responsible for rendering the social media shares performance page.
    """

    def __init__(self, board: Board):
        """
        Initializes the SocialMediaSharesPerformance with a shimoku client instance.

        Parameters:
            shimoku: An instance of the Shimoku client.
        """
        self.df_app = board.df_app

        self.shimoku = board.shimoku

        # Initialize order of plotting elements
        self.order = 0
        # Set the menu path for this page
        self.menu_path = "Overview"

        # Delete existing menu path if it exists
        if self.shimoku.menu_paths.get_menu_path(name=self.menu_path):
            self.shimoku.menu_paths.delete_menu_path(name=self.menu_path)

        # Create the menu path
        self.shimoku.set_menu_path(name=self.menu_path)

    def __str__(self) -> str:
        return f"Dashboard {self.menu_path}"

    def plot(self):
        """
        Plots the Social Media Shares Performance page.
        Each method is responsible for plotting a specific section of the page.
        """
        self.plot_header()
        self.plot_one_year()
        self.plot_indicators()
        self.plot_pizza_sales()
        self.plot_pizza_orders()
        self.plotDailyOrders()
    #         subtitle="Pizza sales resume from a fictitious pizza place over 2015. The dataset represent the pizza's orders considering the price of each pizza type.",

    def plot_header(self) -> bool:
        """Header plot of the menu path

        Returns:
            bool: Execution status
        """
        title = "Pizza's Sales Overview"

        indicator = beautiful_header(title=title)
        self.shimoku.plt.html(
            indicator,
            order=self.order,
            rows_size=1,
            cols_size=10,
            padding='0,1,0,1',
        )
        self.order += 1

        return True

    def plot_one_year(self) -> bool:
        # Plot Series
        self.shimoku.plt.line(
            data=self.df_app["year_orders"],
            order=self.order,
            cols_size=10,
            rows_size=2,
            padding='0,1,0,1',
            x='date',
            x_axis_name='date',
            y_axis_name="pizza's orders",
            title='Orders per day over 2015',
            option_modifications={'dataZoom': {'show': True}, 'toolbox': {'show': True}},
        )

        self.order += 1

        return True

    def plot_indicators(self) -> bool:
        self.shimoku.plt.indicator(
            data=self.df_app["main_kpis"],
            order=self.order,
            rows_size=1,
            cols_size=10,
            padding='0,1,0,1',
        )

        self.order += len(self.df_app["main_kpis"]) + 1

        return True

    def plot_pizza_sales(self) -> bool:
        # Plot Series
        self.shimoku.plt.bar(
            data=self.df_app["sales_orders"],
            order=self.order,
            cols_size=5,
            rows_size=2,
            title="Pizza's sale per month",
            x='date',
            y='sales',
            x_axis_name='date',
            y_axis_name="pizza's sales",
            padding='0,0,0,1',
        )
        self.order += 1

        return True

    def plot_pizza_orders(self) -> bool:
        self.shimoku.plt.bar(
            data=self.df_app["sales_orders"],
            order=self.order,
            cols_size=5,
            rows_size=2,
            title="Pizza's orders per month",
            x='date',
            y='orders',
            x_axis_name='date',
            y_axis_name="pizza's orders",
            padding='0,1,0,0',
        )
        self.order += 1

        return True

    def plotDailyOrders(self) -> bool:
        self.shimoku.plt.area(
            data=self.df_app["daily_orders"],
            order=self.order,
            title="Pizza and Order average per hour",
            cols_size=10,
            x='date',
            x_axis_name='hour',
            y_axis_name="pizza / order",
            padding='0,1,0,1',
        )
        self.order += 1

        return True