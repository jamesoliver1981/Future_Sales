!pip3 install --upgrade pip
!pip3 install pandas_profiling

import pandas as pd
from matplotlib import pyplot as plt
#import pandas_profiling as prf

item_cat= pd.read_csv("01_future-sales/data/item_categories.csv")

item_cat.shape
item_cat.columns