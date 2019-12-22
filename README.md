# Predicting Future Sales
This is where I document the work I carried out on the Kaggle competition to predict a month of sales for Russian software company 1C.  There were just under 3 years of data provided, at the product and shop level on a daily basis, and with this I need to create a prediction for November for every product and shop combination.  This meant that I needed to generate just over 214k predictions.
This work involved exploratory data analysis, data mungung, data cleaning, visualisation, building and tuning machine learning models.  All of this was carried out in Python via Juypter Notebooks.
The evaluation criteria was Root Mean Squared Error, and the winning entry was 0.79215, and my best entry to date is 1.13087 using XGBoost.

The data and further information can be found [here](https://www.kaggle.com/c/competitive-data-science-predict-future-sales)

# Data Provided
We are provided with a main sales file, which identifies the quantity of the product sold in each shop, at which price, per day from a period of January 2013 to October 2015, with the target for prediction being November 2015.  
There are also 
  * an item file which provides a description of the product, unfortunately mostly in Russian, & a category id for the 22k products.  Whilst this was mostly in Russian, it did flag up that a number of these are computer games, which became a very relevant point.
  * an item category file which describes the category id, unfortunately in Russian, but shows there are only 84 categories
  * a shops file, which gives the (Russian) name for the id in the sales file, & shows there are 60 shops
  * the test file shows which product combinations are needed to be predicted and an ID with which can be merged on to the submission file
  
# Initial Data Analysis
Whilst there are over 22k products, initial data analysis found that there only 1654 products which are present in 31 or more of the 34 months in the dataset.  These sold an average of 5 per week, before I broke it further down into the 60 shops, yet represented 20% of total sales volume.  
Given this low volume, I then looked at the variance of some of these products graphically to understand what was happening.
