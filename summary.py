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
import glob

import pandas as pd

# import logging
# logging.basicConfig(format='[%(asctime)s]%(levelname)s:\n%(message)s', level=logging.DEBUG)


# In[2]:


# name = 'name'
# latitude = 'latitude'
# longitude = 'longitude'

# BaseURL = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/'

# ApiKey = 'RXUKQPBJ3PWR56ZL94QPGLHBK'

# yesterday = 'yesterday'

sheets = ['烟台', '德州', '东营','菏泽', '滨州', '潍坊', '青岛', '临沂', 
          '威海', '济南', '济宁', '淄博', '枣庄', '泰安', '日照', '聊城', '莱芜']

# sheets = ['聊城', '莱芜']

##########################

Target = ['datetime', 'windspeed', 'windgust', 'temp', 'cloudcover', 'solarradiation', 'solarenergy']

base_path = 'data/'
data_path = 'wind_data/'
city_path = 'city/'
summary_path = 'summary/'

# result_path = 'myResult/'
result_path = base_path + data_path

# write_mode = 'a'
write_mode = 'w'

suffix = '_future'

##########################


# In[3]:


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


# In[4]:


def get_csv_files(path):
    return glob.glob(os.path.join(path, "*.csv"))

def get_future_csv(path):
    return glob.glob(os.path.join(path, f"*{suffix}.csv"))

def generate_csv_file(files_list, output_path, name, suffix, unit_conversion=True):
    
    df = pd.DataFrame()

    for csv_file in files_list:
        df2 = pd.read_csv(csv_file)[Target]
        df = pd.concat([df, df2])

    avg = df.groupby(df['datetime']).mean()
    
    # 单位换算 km/h -> m/s °F -> °C
    if unit_conversion:
        avg['windspeed'] /= 3.6
        avg['windgust'] /= 3.6
        avg['temp'] = (avg['temp'] - 32) * 5 / 9
    
#     # 若文件已存在则只在末尾追加数据部分，不会写入表头
    filename = output_path + name + suffix + '.csv'
#     header = False if os.path.exists(filename) and write_mode == 'a' else True
    
#     avg.to_csv(filename, mode=write_mode, header=header)
    avg.to_csv(filename)
    
    print(f'{filename} done.')

def summary(input_path, output_path, name, mode=write_mode, unit_conversion=True):
    csv_files = get_csv_files(input_path)
    future_data = get_future_csv(input_path)
    history_data = list(set(csv_files) - set(future_data))
    
    print('-'*40)
    print(f'path: {input_path}\ncsv num:{len(csv_files)} histroy num:{len(future_data)} future num:{len(history_data)}')
    
    # 历史汇总数据追加
    generate_csv_file(files_list=history_data, output_path=output_path, name=name, suffix='', unit_conversion=unit_conversion)
    
    # 未来汇总数据重写
    generate_csv_file(files_list=future_data, output_path=output_path, name=name, suffix=suffix, unit_conversion=unit_conversion)


# In[5]:


make_dir(summary_path)

if os.path.exists(summary_path + '山东.csv'):
    os.remove(summary_path + '山东.csv')
if os.path.exists(summary_path + '山东_future.csv'):
    os.remove(summary_path + '山东_future.csv')    

for sheet in sheets:
    path = city_path + f'{sheet}/'
    
    summary(input_path=path, output_path=summary_path, name=sheet)

summary(input_path=summary_path, output_path=summary_path, name='山东', unit_conversion=False)


# In[ ]:




