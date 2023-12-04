# Pizza Sales
It is a Shimoku DataApp using a data of a fictitious pizza place over 2015.

## Installation

Follow the next steps to install the repository over a linux distributions or a WSL over Windows.

First create the virtual environmental with Python +3.9

```bash
python -m venv ven
source venv/bin/activate
pip install -r requirements.txt
```

Create a .env file to work with the environmental variables and complete variable values.
```
SHIMOKU_TOKEN = ...
UNIVERSE_ID = ...
WORKSPACE_ID = ...
```

To run the code, just execute the python main file over the src folder
```bash
python src/main.py
```

Finally we can go to [Shimoku.io](Shimoku.io) and visualize the dashboard with our data.


## Data
The Dataset used on this project was from [Kaggle DataSet](https://www.kaggle.com/datasets/mysarahmadbhat/pizza-place-sales). We can obtain the following tables from the csv files

- orders.csv
- order_details.csv
- pizzas.csv
- pizza_types.csv

The EER diagram of the dataset

![EER diagram](/assets/pizzaPlaceSales.png)

## Screanshots
![Screanshot 1](Screenshot_1.png)
![Screanshot 2](Screenshot_2.png)
![Screanshot 3](Screenshot_3.png)