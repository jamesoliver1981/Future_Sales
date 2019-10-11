# !pip3 install --upgrade pip
# !pip3 install pandas_profiling

import pandas as pd
from matplotlib import pyplot as plt
# import pandas_profiling as pp

item_cat = pd.read_csv("01_future-sales/data/item_categories.csv")
item_cat.shape

item_cat.info()
item_cat.describe()
item_cat.columns
item_cat.head()


items = pd.read_csv("01_future-sales/data/items.csv")

items.info()
items.describe()
items.columns
items.head()

train = pd.read_csv("01_future-sales/data/sales_train_v2.csv")

train.info()
train.describe()
train.columns
train.head()

