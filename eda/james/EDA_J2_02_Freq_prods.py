#this is a python replica file of the juypter file of the same name 
#because juypter isn't rendering on Git - hence the odd format

#!/usr/bin/env python
# coding: utf-8

# In[86]:


#now that I've looked at the data in EDA file, wanted to look at how the frequency changes a bit more over time
#how change in a month
import pandas as pd
from matplotlib import pyplot as plt
import pandas as pd
import os
import pixiedust as pix


# In[2]:


os.listdir("/home/cdsw/01_future-sales/data")


# In[3]:


dateCols = ['date']
train2=pd.read_csv("/home/cdsw/train_plus_not_imputted.csv",parse_dates=dateCols)
#weird that this is crazy quick to load vs the original? is it compressed?


# In[4]:


train2.info()


# In[5]:


len(set(train2.date))


# In[6]:


train2.date.max()
#so apparently I haven't trimmed the data - works out as am predicting the November and have the start to see how it leads in


# In[7]:


train2.info()


# In[8]:


#create a month variable and then see how many months are at 1 or zero
train2["Month"]=train2.date.dt.month
train2["Year"]=train2.date.dt.year
train2['YM'] = train2['Year']*100+train2["Month"]
train2.head()



# In[9]:


#create a month variable and then see how many months are at 1 or zero
train2["Month"]=train2.date.dt.month
train2["Year"]=train2.date.dt.year
train2["YM"]=train2.Year*100+train2.Month




# In[10]:


train2.info()


# In[11]:


train2.head()


# In[12]:


#group by sales per month
sales_per_item_PM= train2.groupby(['item_id','YM'])['item_cnt_day'].sum().reset_index()

print(sales_per_item_PM.info())
sales_per_item_PM.head()


# In[13]:


#questions to answer now
    #how many of these have sales in every month
        #count of count of this table per id being 34
        # vs a unique number of products

    #Should I restrict this to the bigger items - how many sold over all?    
    #what is the development of the sales shape
        


# In[14]:


#Question1
#how many of these have sales in every month
        #count of count of this table per id being 34
        # vs a unique number of products
num_months=sales_per_item_PM.groupby(["item_id"]).count()
num_months["item_id"]=num_months.index
#print(num_months.info())
num_months.head()


# In[15]:


all_months=num_months[num_months.YM>30]
all_months.info()


# In[16]:


#so only 1654 items which were presented in 31 or more months of the 22k products
#what are the volumes of these items - are they all a certain category type

#overall sales per item
sales_per_item=train2.groupby(["item_id"])["item_cnt_day"].sum().reset_index()
sales_per_item["perweek"]=sales_per_item.item_cnt_day/150


print("Number of items sold less than 1-10 times a week:", len(sales_per_item[(sales_per_item.perweek<10) & (sales_per_item.perweek>=5) ]))
print("Number of items sold less than 11-50 times a week:", len(sales_per_item[(sales_per_item.perweek<50) & (sales_per_item.perweek>=10) ]))
print("Number of items sold less than 51-500 times a week:", len(sales_per_item[(sales_per_item.perweek<500) & (sales_per_item.perweek>=50) ]))

print("Remember these are just averages!!!  There can be a lot of volume in one week that skew this")


# In[35]:


sales_per_item["permonth"]=sales_per_item.item_cnt_day/36


# In[17]:


#TO DOs
#Create a look up of high low medium volumes (more levels) from this and then look this up to see if those that are every week
# are high volume
# or just transfer the average over and assess it that way

#then it will be interesting to assess the higher volume elements and see in how many weeks they are purchased


# In[36]:


#combine those showing how many weeks are sold in and what are sold on average per week
reg_vol=num_months.merge(sales_per_item[['item_id','perweek',"permonth"]], on='item_id', how='left', indicator=True).drop("YM",1)
reg_vol = reg_vol.rename(columns={'item_cnt_day': 'MonthsPresent'})
reg_vol.head()


# In[37]:


#of those sold every week, is this high volume
reg=reg_vol[reg_vol.MonthsPresent >30]
reg.describe()


# In[38]:


#of those high volume, how often are they sold
high=reg_vol[reg_vol.perweek> 20]
high.describe()


# In[46]:


#so there are only 1654 items that are sold every month... and these sell an average of 5 per week
#there are then only 107 of 22k items which sell more than 20 per week, and these are mostly present in every week...

#how much of the sales do these 20 products account for
print("%.1f%%" % (100 * sum(high.perweek*150)/sum(train2.item_cnt_day)))


# In[ ]:


#what is their variation


# In[53]:


#are there other products which are sold, not in the 107 which account for a high frequency?
nothigh=sales_per_item[~sales_per_item.item_id.isin(high.item_id)]
nothigh.sort_values("item_cnt_day",ascending=False).head()


# In[56]:


mid_high=reg_vol[(reg_vol.perweek<= 20) & (reg_vol.perweek>10)]
print("%.1f%%" % (100*sum(mid_high.perweek*150)/sum(train2.item_cnt_day)))
mid.describe()
#these are also slightly less often present than high - 28 average vs 31


# In[58]:


mid=reg_vol[(reg_vol.perweek>5)&(reg_vol.perweek<=10)]
print("%.1f%%" % (100*sum(mid.perweek*150/sum(train2.item_cnt_day))))
mid.describe()


# In[65]:


print(len(mid)+len(high)+len(mid_high), "products account for ", 
      "%.1f%%" % (100*(sum(mid.perweek*150)/sum(train2.item_cnt_day)+
                       sum(mid_high.perweek*150)/sum(train2.item_cnt_day)+
                       sum(high.perweek*150)/sum(train2.item_cnt_day))),"volume sold")


# In[66]:


#df.pivot_table(index=['First','Last'],columns='Group',values='Measure',fill_value=0)
sales_per_item_PM.head()


# In[74]:


sales_perM= sales_per_item_PM.pivot_table(index=["item_id"],columns="YM",values="item_cnt_day", fill_value=0).reset_index() 
#sales_perM["item_id"]=sales_perM.index
print(sales_perM.info())
sales_perM.head()


# In[75]:


sales_perM[sales_perM.item_id==1495]


# In[81]:


high_wide=sales_perM[sales_perM.item_id.isin(high.item_id) ]
pix.display(high_wide)


# In[88]:


high_chart=sales_per_item_PM[sales_per_item_PM.item_id.isin(high.item_id) ].head()
pix.display(high_chart)


# In[ ]:


#export the PM dataset and then see how constant the high and low values are - are there trends?
#could do as an explore here with plot lib...


# In[18]:


#this is an example you want to replicate, to find the data in the often sold from the general volume data
df[~df.countries.isin(countries)]
df1 = pd.DataFrame({'c': ['A', 'A', 'B', 'C', 'C'],
                    'k': [1, 2, 2, 2, 2],
                    'l': ['a', 'b', 'a', 'a', 'd']})
df2 = pd.DataFrame({'c': ['A', 'C'],
                    'l': ['b', 'a']})
keys = list(df2.columns.values)
i1 = df1.set_index(keys).index
i2 = df2.set_index(keys).index
df1[~i1.isin(i2)]


# In[19]:


df1


# In[20]:


df2


# In[21]:


i1

