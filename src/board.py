import pandas as pd
import datetime as dt

from shimoku import Client
from utils.utils import get_data

class Board:
    """
    A class used to represent a Dashboard for displaying various data visualizations.

    Attributes:
        board_name (str): Name of the dashboard.
        dfs (DFs): An instance of a DFs class for handling data frames.
        shimoku (Client): An instance of a Client class for Shimoku API interactions.
    """

    def __init__(self, shimoku: Client):
        """
        The constructor for the Dashboard class.

        Parameters:
            shimoku (Client): An instance of a Client class for Shimoku API interactions.
        """

        file_names = ['data/order_details.csv', 'data/orders.csv', 'data/pizza_types.csv', 'data/pizzas.csv']
        # Name of the dashboard
        self.board_name = "Sales Pizza Feedback"
        # Get the data from CSV file
        self.dfs = get_data(file_names)
        # Shimoku client instance
        self.shimoku = shimoku
        # Setting up the board in Shimoku
        self.shimoku.set_board(name=self.board_name)
        # Make the board public
        self.shimoku.boards.update_board(name=self.board_name, is_public=True)

    def transform(self) -> bool:
        """
        Perform data transformations.

        This method is responsible for handling any data transformations
        required before plotting the data on the dashboard.
        """

        df_social_media = self.dfs["order_details"]

        totaldays2015 = pd.Timestamp(2015, 12, 31).dayofyear

        # Get dataframe
        df_orders = self.dfs['orders']
        df_order_details = self.dfs['order_details']
        df_pizzas = self.dfs['pizzas']

        # Compute orders per day
        seriesCountPerYear = df_orders.date.groupby(df_orders.date).count()
        df_year_orders = seriesCountPerYear.to_frame(name="order").reset_index()

        # Compute total sale over 2015
        pizzasByTypes = df_order_details.groupby(df_order_details.pizza_id).sum()

        totalSales = 0
        for index, row in pizzasByTypes.iterrows():
            totalSales += row['quantity'] * (df_pizzas[df_pizzas['pizza_id']==index]['price'].squeeze() * 100)
            totalSales = totalSales / 100

        # Compute total pizzas, total orders
        totalPizzas = df_order_details['quantity'].sum()
        totalOrders = df_orders.shape[0]

        # Compute average total pizzas and orders per days
        averageOrders = totalOrders // totaldays2015
        averagePizza = totalPizzas // totaldays2015

        # Set List[dict] of the KPIs
        keysKPIs = ['Total Sales', 'Total Pizzas', 'Total Orders', 'Avg. Pizzas/day', 'Avg. Orders/day']
        valuesKPIs = [totalSales, totalPizzas, totalOrders, averageOrders, averagePizza]
        main_kpis = [
            {
            'title': key,
            'value': round(value),
            'color': 'success',
            'align': 'center',
            'variant': 'topColor',
            }
        for key, value in zip(keysKPIs, valuesKPIs)]

        # Set List[dict] where each element has month, sales and orders value
        monthSalesOrders = [
            {
                'date': dt.date(2015, month, 1),
                'sales': '0',
                'orders': '0'
            }
        for month in range(1,13)]

        # Loop for each month,
        for month in monthSalesOrders:
            # filter orders by month
            ordersPerMonth = df_orders[df_orders['date'].dt.month == month['date'].month]
            # filter order details by order in each month
            orderDetailsPerMonth = df_order_details[df_order_details['order_id'].isin(ordersPerMonth['order_id'])]
            pizzasByTypes = orderDetailsPerMonth.groupby(orderDetailsPerMonth.pizza_id).sum()

            # Compute total sales for the orders in month
            totalMonthSales = 0
            for index, row in pizzasByTypes.iterrows():
                totalMonthSales += row['quantity'] * (df_pizzas.loc[df_pizzas['pizza_id']==index, 'price'].squeeze() * 100)

            month['sales'] = '%.2f'%(totalMonthSales / 100)
            month['orders'] = '%d'%pizzasByTypes['quantity'].sum()



        # Set List[dict] for each hour on daily
        df_daily_orders = [
            {
                'date': hour,
                'pizzas': '0',
                'orders': '0'
            }
        for hour in range(9,25)]

        # loop over each hour
        for hour in df_daily_orders:
            # filter order_id for each hour over the whole year and compute the average order per hour
            ordersPerHour = df_orders[df_orders['time'].dt.hour == hour['date']]['order_id']
            avgOrdersPerHour = ordersPerHour.count() / totaldays2015
            hour['orders'] = round(avgOrdersPerHour, 2)

            # filter pizza quantity for each hour over the whole year and compute the average pizza quantity per hour
            orderDetailsPerHour = df_order_details[df_order_details['order_id'].isin(ordersPerHour)]['quantity']
            avgOrderDetailsPerHour = orderDetailsPerHour.sum() / totaldays2015
            hour['pizzas'] = round(avgOrderDetailsPerHour, 2)

        # Dictionary of the dataframes
        self.df_app = {
            "year_orders": pd.DataFrame(df_year_orders),
            "main_kpis": main_kpis,
            "sales_orders": pd.DataFrame(monthSalesOrders),
            "daily_orders": pd.DataFrame(df_daily_orders),
        }

        return True

    def plot(self):
        """
        A method to plot Social Media Shares Performance.

        This method utilizes the SocialMediaSharesPerformance class from the paths.social_media_shares_performance
        module to create and display a plot related to the social media posts. It assumes that
        SocialMediaSharesPerformance requires a reference to the instance of the class from which
        this method is called.

        Args:
        self: A reference to the current instance of the class.

        Returns:
        None. The function is used for its side effect of plotting data.

        Note:
        - This method imports the SocialMediaSharesPerformance class within the function scope
          to avoid potential circular dependencies.
        - Ensure that the SocialMediaSharesPerformance class has access to all necessary data
          through the passed instance.
        """

        from paths.sales_pizza import SalesPizza

        SP = SalesPizza(self)
        SP.plot()
