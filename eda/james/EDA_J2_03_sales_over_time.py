#Code from Juypter notebook as doesn't display well on git
#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#EDA 3 Looks at the profile of sales
#will look at the top elements and see if have similar pattern

#randomly selected bunch of mid & low and see if same or different behaviours


# In[141]:


#read in the file, group the sales, add the Year Month variable and then pivot the data 
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import os
import pixiedust as pix
dateCols = ['date']
train2=pd.read_csv("/home/cdsw/train_plus_not_imputted.csv",parse_dates=dateCols)
train2["Month"]=train2.date.dt.month
train2["Year"]=train2.date.dt.year
train2['YM'] = train2['Year']*100+train2["Month"]
sales_per_item_PM= train2.groupby(['item_id','YM'])['item_cnt_day'].sum().reset_index()
sales_perM= sales_per_item_PM.pivot_table(index=["item_id"],columns="YM",values="item_cnt_day", fill_value=0).reset_index() 
sales_perM.head()


# In[142]:


#create the filters for high or low
sales_per_item=train2.groupby(["item_id"])["item_cnt_day"].sum().reset_index()
sales_per_item["permonth"]=sales_per_item.item_cnt_day/36
sales_per_item["perweek"]=sales_per_item.item_cnt_day/150
len(sales_per_item[sales_per_item.perweek >20])


# In[108]:


#create a sorted list of the frequency of sales
ordered_sales=sales_per_item.sort_values(by='item_cnt_day', ascending=False)
ordered_sales["id"]="it_" + ordered_sales.item_id.astype(str)
ordered_sales.head(20)


# In[89]:


ordered_sales.id[0:9]


# In[35]:


#restrict to those that are high sales
high=sales_perM[sales_perM.item_id.isin(sales_per_item.item_id[sales_per_item.perweek>20])]
high["item_id"]= "it_" + high["item_id"].astype(str)
high.index=high.item_id

high_t=high.drop("item_id",axis=1).transpose()
high_t.head()


# In[113]:



def printcharts(df):
     
    """Take 9 of the products and plot them to show how the sales over time"""

    # Initialize the figure
    plt.style.use('seaborn-darkgrid')

    # create a color palette
    palette = plt.get_cmap('Set1')

    # multiple line plot
    num=0
    for column in df:
        num+=1

        # Find the right spot on the plot
        plt.subplot(3,3, num)

        # Plot the lineplot
        plt.plot(range(1,37), df[column], marker='', color=palette(num), linewidth=1.9, alpha=0.9, label=column)

        # Same limits for everybody!
        plt.xlim(0,37)
        plt.ylim(0,df.max().max())

        # Not ticks everywhere
        if num in range(7) :
            plt.tick_params(labelbottom='off')
        if num not in [1,4,7] :
            plt.tick_params(labelleft='off')

        # Add title
        plt.title(column, loc='left', fontsize=12, fontweight=0, color=palette(num) )

    # general title
    plt.suptitle("Sales for 9 items", fontsize=13, fontweight=0, color='black', style='italic', y=1.02)

#I've not forgotten that python is zero indexed - the first variable is just way bigger and I wanted to remove that scaling
printcharts(high_t.loc[:,list(ordered_sales.id[1:10])])
ordered_sales.iloc[1:10,]


# In[175]:


#display(high[high.item_id.isin(ordered_sales.id[1:10])])
#compare 1855  6675 5822 17717 2808 
#compare  16787 3734 , poss sep 3732 3731
display(high[high.item_id.isin(["it_1855" ,"it_6675", "it_5822", "it_17717", "it_2808"])])


# In[115]:


#so even though some items have similar volumes over time, and whilst they all have some form of peak, some have more extreme
#peaks
#do they peeter out until almost nothing?  Is there a relationship to its max and how long that takes?
printcharts(high_t.loc[:,list(ordered_sales.id[10:19])])
ordered_sales.iloc[10:19,]


# In[116]:


printcharts(high_t.loc[:,list(ordered_sales.id[19:28])])
ordered_sales.iloc[19:28,]


# In[121]:


#some of the patterns are really interesting...practically flat yet still account for relatively high volume here
#for example it_3732 has a peak but still had some good sales for 5 months before hand...
plt.plot(range(1,37),high_t.it_3732)
print(high_t.loc[:,"it_3732"].head(10))


# In[124]:


#lets see if we get a similar view for another it_16790 - yep
plt.plot(range(1,37), high_t.it_16790)
high_t.loc[:,"it_16790"].head(20)


# In[146]:


#create transposed file for all so can look at all not just those who are not selling most
sales_perM["id"]= "it_" + sales_perM["item_id"].astype(str)
sales_perM.index=sales_perM.id

sales_perM_t=sales_perM.drop(["item_id","id"],axis=1).transpose()
#printcharts(sales_perM_t.loc[:,list(ordered_sales.id[500:509])])
printcharts(sales_perM_t.loc[:,list(ordered_sales.id[500:509])])


# In[70]:


printcharts(high_t.iloc[:,9:18])


# In[73]:


printcharts(high_t.iloc[:,18:27])

