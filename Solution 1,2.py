#!/usr/bin/env python
# coding: utf-8

# # Solution 1

# In[1]:


import pandas as pd 
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

import json 

import requests 

from bs4 import BeautifulSoup
import xml


# In[2]:


List_url = "https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M"
source = requests.get(List_url).text


# In[3]:


soup = BeautifulSoup(source, 'xml')


# In[4]:


table=soup.find('table')


# In[5]:


column_names = ['Postalcode','Borough','Neighborhood']
df = pd.DataFrame(columns = column_names)


# In[6]:


for tr_cell in table.find_all('tr'):
    row_data=[]
    for td_cell in tr_cell.find_all('td'):
        row_data.append(td_cell.text.strip())
    if len(row_data)==3:
        df.loc[len(df)] = row_data


# In[7]:


df.head()


# In[10]:


temp_df=df.groupby('Postalcode')['Neighborhood'].apply(lambda x: "%s" % ', '.join(x))
temp_df=temp_df.reset_index(drop=False)
temp_df.rename(columns={'Neighborhood':'Neighborhood_joined'},inplace=True)


# In[11]:


df_merge = pd.merge(df, temp_df, on='Postalcode')


# In[12]:


df_merge.drop(['Neighborhood'],axis=1,inplace=True)


# In[13]:


df_merge.drop_duplicates(inplace=True)


# In[14]:


df_merge.rename(columns={'Neighborhood_joined':'Neighborhood'},inplace=True)


# In[15]:


df_merge


# In[16]:


df_merge.shape


# # Solution 2

# In[17]:


import pandas as pd
import requests
from bs4 import BeautifulSoup


# In[18]:


List_url = "https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M"
source = requests.get(List_url).text


# In[19]:


soup = BeautifulSoup(source, 'xml')


# In[20]:


table=soup.find('table')


# In[21]:


column_names=['Postalcode','Borough','Neighbourhood']
df = pd.DataFrame(columns=column_names)


# In[22]:


for tr_cell in table.find_all('tr'):
    row_data=[]
    for td_cell in tr_cell.find_all('td'):
        row_data.append(td_cell.text.strip())
    if len(row_data)==3:
        df.loc[len(df)] = row_data


# In[23]:


df.head()


# In[26]:


temp_df=df.groupby('Postalcode')['Neighbourhood'].apply(lambda x: "%s" % ', '.join(x))
temp_df=temp_df.reset_index(drop=False)
temp_df.rename(columns={'Neighbourhood':'Neighbourhood_joined'},inplace=True)


# In[27]:


df_merge = pd.merge(df, temp_df, on='Postalcode')


# In[28]:


df_merge.drop(['Neighbourhood'],axis=1,inplace=True)


# In[29]:


df_merge.drop_duplicates(inplace=True)


# In[30]:


df_merge.rename(columns={'Neighbourhood_joined':'Neighbourhood'},inplace=True)
df_merge.head()


# In[31]:


df_merge.shape


# In[32]:


def get_geocode(postal_code):
    lat_lng_coords = None
    while(lat_lng_coords is None):
        g = geocoder.google('{}, Toronto, Ontario'.format(postal_code))
        lat_lng_coords = g.latlng
    latitude = lat_lng_coords[0]
    longitude = lat_lng_coords[1]
    return latitude,longitude


# In[33]:


geo_df=pd.read_csv('http://cocl.us/Geospatial_data')


# In[34]:


geo_df.head()


# In[35]:


geo_df.rename(columns={'Postal Code':'Postalcode'},inplace=True)
geo_merged = pd.merge(geo_df, df_merge, on='Postalcode')


# In[36]:


geo_data=geo_merged[['Postalcode','Borough','Neighbourhood','Latitude','Longitude']]


# In[37]:


geo_data.head()


# In[ ]:




