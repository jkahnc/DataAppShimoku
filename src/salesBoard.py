import os
import datetime as dt
import pandas as pd
from re import sub
from shimoku_api_python import Client

class Dashboard():
  def __init__(self, shimoku: Client) -> None:
    self.order = 0
    self.shimoku = shimoku
    self.dashboardName = 'Sales Pizza'
    self.__fileNames = ['./data/order_details.csv', './data/orders.csv', './data/pizza_types.csv', './data/pizzas.csv']
    self.dfs = self.getData()
    self.totaldays2015 = pd.Timestamp(2015, 12, 31).dayofyear


  def __str__(self) -> str:
    return f"Dashboard {self.dashboardName}"


  def setDashboard(self):
    self.shimoku.set_board(self.dashboardName)
    self.shimoku.set_menu_path(name="Overview")

    self.plotHeader("Overview")
    self.plotOneYear()
    self.plotIndicators()
    self.plotSalesPerMonth()
    self.plotDailyOrders()


  def plotHeader(self, title: str):
    self.shimoku.plt.html(
      order=self.order,
      html=self.shimoku.html_components.create_h1_title(
        title="Pizza's Sales Overview",
        subtitle="Pizza sales resume from a fictitious pizza place over 2015. The dataset represent the pizza's orders considering the price of each pizza type.",
      )
    )
    self.order += 1


  def plotOneYear(self):
    # Get dataframe
    dfOrders = self.dfs['orders']

    # Compute orders per day
    seriesCountPerYear = dfOrders.date.groupby(dfOrders.date).count()

    # Plot Series
    self.shimoku.plt.line(
      data=self.convert_series_to_array(seriesCountPerYear, 'Orders'),
      x='date',
      order=self.order,
      rows_size=2,
      cols_size=10,
      padding='0,0,0,1',
      x_axis_name='date',
      y_axis_name="pizza's orders",
      title='Orders per day over 2015',
      option_modifications={'dataZoom': {'show': True}, 'toolbox': {'show': True}},
    )

    self.order += 1


  def plotIndicators(self):
    # get dataframes
    dfOrders = self.dfs['orders']
    dfOrderDetails = self.dfs['order_details']
    dfPizzas = self.dfs['pizzas']

    # Compute total sale over 2015
    totalSales = 0
    pizzasByTypes = dfOrderDetails.groupby(dfOrderDetails.pizza_id).sum()

    for index, row in pizzasByTypes.iterrows():
      totalSales += row['quantity'] * (dfPizzas[dfPizzas['pizza_id']==index]['price'].squeeze() * 100)
    totalSales = totalSales / 100

    # Compute total pizzas, total orders
    totalPizzas = dfOrderDetails['quantity'].sum()
    totalOrders = dfOrders.shape[0]

    # Compute average total pizzas and orders per days
    averageOrders = totalOrders // self.totaldays2015
    averagePizza = totalPizzas // self.totaldays2015

    # Set List[dict] of the KPIs
    keysKPIs = ['Total Sales', 'Total Pizzas', 'Total Orders', 'Avg. Pizzas/day', 'Avg. Orders/day']
    valuesKPIs = [totalSales, totalPizzas, totalOrders, averageOrders, averagePizza]
    data = [{
      'title': key,
      'value': str(value),
      'color': 'success',
      'align': 'center',
      'variant': 'topColor',
    } for key, value in zip(keysKPIs, valuesKPIs)]

    self.shimoku.plt.indicator(
      data=data,
      order=self.order,
      rows_size=1,
      cols_size=12,
      padding='0,0,0,0',
    )

    self.order += len(keysKPIs) + 1


  def plotSalesPerMonth(self):
    # Get dataframe
    dfOrders = self.dfs['orders']
    dfOrderDetails = self.dfs['order_details']
    dfPizzas = self.dfs['pizzas']

    # Set List[dict] where each element has month, sales and orders value
    monthSalesOrders = [ {'date': dt.date(2015, month, 1), 'sales': '0', 'orders': '0'} for month in range(1,13)]

    # Loop for each month,
    for month in monthSalesOrders:
      # filter orders by month
      ordersPerMonth = dfOrders[dfOrders['date'].dt.month == month['date'].month]
      # filter order details by order in each month
      orderDetailsPerMonth = dfOrderDetails[dfOrderDetails['order_id'].isin(ordersPerMonth['order_id'])]
      pizzasByTypes = orderDetailsPerMonth.groupby(orderDetailsPerMonth.pizza_id).sum()

      # Compute total sales for the orders in month
      totalMonthSales = 0
      for index, row in pizzasByTypes.iterrows():
        totalMonthSales += row['quantity'] * (dfPizzas.loc[dfPizzas['pizza_id']==index, 'price'].squeeze() * 100)

      month['sales'] = '%.2f'%(totalMonthSales / 100)
      month['orders'] = '%d'%pizzasByTypes['quantity'].sum()

    # Plot Series
    self.shimoku.plt.bar(
      data=monthSalesOrders,
      x='date',
      y='sales',
      order=self.order,
      rows_size=2,
      cols_size=5,
      x_axis_name='date',
      y_axis_name="pizza's sales",
      title="Pizza's sale per month",
      padding='0,0,0,1',
    )
    self.order += 1

    self.shimoku.plt.bar(
      data=monthSalesOrders,
      x='date',
      y='orders',
      order=self.order,
      rows_size=2,
      cols_size=5,
      x_axis_name='date',
      y_axis_name="pizza's orders",
      title="Pizza's orders per month",
      padding='0,1,0,0',
    )
    self.order += 1


  def plotDailyOrders(self):
    # Get dataframe
    dfOrders = self.dfs['orders']
    dfOrderDetails = self.dfs['order_details']

    # Set List[dict] for each hour on daily
    data = [ {'date': hour, 'pizzas': '0', 'orders': '0'} for hour in range(9,25)]

    # loop over each hour
    for hour in data:
      # filter order_id for each hour over the whole year and compute the average order per hour
      ordersPerHour = dfOrders[dfOrders['time'].dt.hour == hour['date']]['order_id']
      avgOrdersPerHour = ordersPerHour.count() / self.totaldays2015
      hour['orders'] = "%.2f"%avgOrdersPerHour

      # filter pizza quantity for each hour over the whole year and compute the average pizza quantity per hour
      orderDetailsPerHour = dfOrderDetails[dfOrderDetails['order_id'].isin(ordersPerHour)]['quantity']
      avgOrderDetailsPerHour = orderDetailsPerHour.sum() / self.totaldays2015
      hour['pizzas'] = "%.2f"%avgOrderDetailsPerHour

    self.shimoku.plt.area(
      data=data,
      order=self.order,
      x='date',
      cols_size=10,
      x_axis_name='hour',
      y_axis_name="pizza / order",
      title="Pizza and Order average per hour",
      padding='0,1,0,1',
    )
    self.order += 1


  def getData(self) -> dict:
    """ Get the data in Dataframes from the files in the data folder.

    Returns:
        dict: Dictionary of dataframes
    """
    dictDataframes = dict()
    for fileName in self.__fileNames:
      df = pd.read_csv(fileName)

      columnasFecha = [col for col in df.columns if "date" in col or "time" in col]
      if columnasFecha:
        df['order_time'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='%Y-%m-%d %H:%M:%S')
        for columna in columnasFecha:
          df[columna] = df[columna].apply(pd.to_datetime)

      dictDataframes[os.path.splitext(os.path.basename(fileName))[0]] = df

    return dictDataframes


  def convert_dataframe_to_array(self, df):
    """Convert a dataframe to a dictionary

    Args:
        df (Dataframe): a Dataframe

    Returns:
        Dict: Dictionary of the dataframe
    """
    columnsToInclude = df.columns.tolist()
    newData = []
    for index, row in df.iterrows():
        newDict = {column: row[column] for column in columnsToInclude}
        newData.append(newDict)
    return newData


  def convert_series_to_array(self, df, rowName: str = 'Count'):
    """Convert a serie to a dictionary

    Args:
        df (Series): a Series

    Returns:
        Dict: Dictionary of the serie
    """
    new_data = [{'date': index, rowName: row} for index, row in df.items()]
    return new_data