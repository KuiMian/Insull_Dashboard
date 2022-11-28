#!/usr/bin/env python
# coding: utf-8

# In[1]:


import csv
import codecs
import urllib.request
import urllib.error
import sys

import datetime
import os 

import pandas as pd

# import logging
# logging.basicConfig(format='[%(asctime)s]%(levelname)s:\n%(message)s', level=logging.DEBUG)


# In[2]:


name = 'name'
latitude = 'latitude'
longitude = 'longitude'

BaseURL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'

ApiKey = #######################

yesterday = 'yesterday'

sheets = ['烟台', '德州', '东营','菏泽', '滨州', '潍坊', '青岛', '临沂', 
          '威海', '济南', '济宁', '淄博', '枣庄', '泰安', '日照', '聊城', '莱芜']

# sheets = ['聊城', '莱芜']

##########################

Target = ['datetime', 'windspeed', 'windgust']

base_path = 'data/'
data_path = 'wind_data/'
city_path = 'city/'
summary_path = 'summary/'

# result_path = 'myResult/'
result_path = base_path + data_path

# time_range = ('2022-7-1', '2022-11-17')

# time_range = yesterday

time_range = None
##########################


# In[3]:


def set_range_and_mode(time_range, circle=14):
    
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    today_str = today.strftime('%Y-%m-%d')
    yesterday_str = yesterday.strftime('%Y-%m-%d')
    
    if isinstance(time_range, (list, tuple)):
        start, end = time_range
        print(f'gather model: from {start} to {end}.')
        
        future_suffix = ''
        write_mode = 'w'
    
    elif time_range == 'yesterday':
        print(f'gather model: yesterday.')
        start = end = yesterday_str
        
#         start = '2022-11-18'
#         end = '2022-11-22'
    
        future_suffix = ''
        write_mode = 'a'
        
    else:
        print(f'gather model: the next {circle} days from {today_str}.')

        start = f'next{circle}days'
        end = ''
        
        future_suffix = '_future'
        write_mode = 'w'
        
    return start, end, future_suffix, write_mode

start, end, future_suffix, write_mode = set_range_and_mode(time_range)
print(f'future_suffix: {future_suffix}\nwrite_mode: {write_mode}')


# In[4]:


def make_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)    

def get_data_path():
    
    path = result_path
    make_dir(path)
    
    return path

path = get_data_path()

print(f'data path: {path}\nwrite mode: {write_mode}')

city_path = path + city_path
summary_path = path + summary_path

now_path = None
sheet = None


# In[5]:


def get_location_info(location):
#     """
#     list:[name, latitude, longitude]
    
#     """
#     if isinstance(location, (list, tuple)):
#         # to dataframe
#         return location[0], f'{location[1]},{location[2]}'
#     else:  # pandas.Dataframe
#         return location[name], f'{location.latitude},{location.longitude}'
    
    return location[name], f'{location.latitude},{location.longitude}'

    
def get_ApiQuery(Location, StartDate=start, EndDate=end, UnitGroup='us', ContentType="csv", Include="hours"):
    # basic query including location
    ApiQuery = BaseURL + Location

    # append the start and end date if present
    if(len(StartDate)):
        ApiQuery += "/" + StartDate
        if(len(EndDate)):
            ApiQuery += "/" + EndDate

    # Url is completed. Now add query parameters (could be passed as GET or POST)
    ApiQuery += "?"

    # append each parameter as necessary
    if(len(UnitGroup)):
        ApiQuery += "&unitGroup=" + UnitGroup
#         ApiQuery += "unitGroup=" + UnitGroup
        

    if(len(ContentType)):
        ApiQuery += "&contentType=" + ContentType

    if(len(Include)):
        ApiQuery += "&include=" + Include

    ApiQuery += "&key=" + ApiKey

    return ApiQuery

def generate_csv_data(ApiQuery, filename):
    try: 
        CSVBytes = urllib.request.urlopen(ApiQuery)
    except urllib.error.HTTPError  as e:
        ErrorInfo= e.read().decode() 
        print('Error code: ', e.code, ErrorInfo)
        sys.exit()
    except urllib.error.URLError as e:
        ErrorInfo= e.read().decode() 
        print('Error code: ', e.code,ErrorInfo)
        sys.exit()
    
    data = CSVBytes.read().decode('utf-8')
    
    filename = f'{now_path}{filename}{future_suffix}.csv'
    
    # 若文件已存在则只在末尾追加数据部分，不会写入表头
    if os.path.exists(filename) and write_mode == 'a':
        data = data[223:]
        
    with open(filename, write_mode, encoding='utf-8') as myFile:
        myFile.write(data)

def gather_data(location, start=start, end=end):
    location_name, loc_string = get_location_info(location)

    ApiQuery = get_ApiQuery(loc_string, start, end)
    
    generate_csv_data(ApiQuery, location_name)
#     print(f'{location_name} done.')


# In[6]:


"""
更新未来数据
"""


start, end, future_suffix, write_mode = set_range_and_mode(time_range)
print(f'future_suffix: {future_suffix}\nwrite_mode: {write_mode}')


now_path = city_path
make_dir(now_path)

_path = now_path
print(f'root path: {now_path}')
print(f'*'*40)

# update future()    

for sheet in sheets:
    now_path += f'{sheet}/'  # data/wind_data/city/烟台/

    print(f'now_path: {now_path}')
    make_dir(now_path)

    data = pd.read_excel('locations.xlsx', sheet_name=sheet)[[name, latitude, longitude]]

    _ = data.apply(gather_data, axis=1)
    print('-'*40)

    now_path = _path


# In[ ]:




