#!/usr/bin/env python
# coding: utf-8

# In[1]:


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

sheets = ['烟台', '德州', '东营', '菏泽', '滨州', '潍坊', '青岛', '临沂',
          '威海', '济南', '济宁', '淄博', '枣庄', '泰安', '日照', '聊城', '莱芜']

# sheets = ['聊城', '莱芜']

##########################


WIND_TARGET = ['datetime', 'windspeed', 'windgust']
SOLAR_TARGET = ['datetime', 'temp', 'cloudcover', 'solarradiation', 'solarenergy']

# base_path = 'data_test/'
base_path = 'data/'
wind_data_path = 'wind_data/'
solar_data_path = 'solar_data/'
city_path = 'city/'
summary_path = 'summary/'

wind_result_path = base_path + wind_data_path
solar_result_path = base_path + solar_data_path

# write_mode = 'a'
write_mode = 'w'

future_suffix = '_future'
yesterday_suffix = '_yesterday'

##########################


# In[3]:


def make_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def get_data_path(category):
    if category == 'wind':
        path = wind_result_path
        make_dir(path)
    elif category == 'solar':
        path = solar_result_path
        make_dir(path)
    else:
        raise KeyError

    return path




wind_path = get_data_path(category='wind')
solar_path = get_data_path(category='solar')

wind_city_path = wind_path + city_path
wind_summary_path = wind_path + summary_path

solar_city_path = solar_path + city_path
solar_summary_path = solar_path + summary_path

now_path = None
sheet = None


# In[4]:


def get_csv_files(path, suffix=''):
    return glob.glob(os.path.join(path, f"*{suffix}.csv"))


def generate_csv_file(files_list, output_path, category, name, suffix, unit_conversion=True):
    if category == 'wind':
        target = WIND_TARGET
    else:
        target = SOLAR_TARGET

    df = pd.DataFrame()

    for csv_file in files_list:
        df2 = pd.read_csv(csv_file)[target]
        df = pd.concat([df, df2])

    avg = df.groupby(df['datetime']).mean()

    # 单位换算 km/h -> m/s °F -> °C
    if unit_conversion:
        if category == 'wind':
            avg['windspeed'] /= 3.6
            avg['windgust'] /= 3.6
        else:
            avg['temp'] = (avg['temp'] - 32) * 5 / 9

    #     # 若文件已存在则只在末尾追加数据部分，不会写入表头
    filename = output_path + name + suffix + '.csv'
    #     header = False if os.path.exists(filename) and write_mode == 'a' else True

    #     avg.to_csv(filename, mode=write_mode, header=header)
    avg.to_csv(filename)

    print(f'{filename} done.')


def summary(input_path, output_path, category, name, mode=write_mode, unit_conversion=True):
    csv_files = get_csv_files(input_path)
    future_files = get_csv_files(input_path, suffix=future_suffix)
    yesterday_files = get_csv_files(input_path, suffix=yesterday_suffix)
    history_files = list(set(csv_files) - set(future_files) - set(yesterday_files))

    print('-' * 40)
    print(f'path: {input_path}\ncsv num:{len(csv_files)} histroy num:{len(future_files)} future num:{len(history_files)}')

    # 历史汇总数据追加
    generate_csv_file(files_list=history_files, output_path=output_path, category=category, name=name, suffix='',
                      unit_conversion=unit_conversion)

    # 未来汇总数据重写
    generate_csv_file(files_list=future_files, output_path=output_path, category=category, name=name, suffix=future_suffix,
                      unit_conversion=unit_conversion)


# In[5]:


make_dir(wind_summary_path)

if os.path.exists(wind_summary_path + '山东.csv'):
    os.remove(wind_summary_path + '山东.csv')
if os.path.exists(wind_summary_path + '山东_future.csv'):
    os.remove(wind_summary_path + '山东_future.csv')

for sheet in sheets:
    path = wind_city_path + f'{sheet}/'

    summary(input_path=path, output_path=wind_summary_path, category='wind', name=sheet)

summary(input_path=wind_summary_path, output_path=wind_summary_path, category='wind', name='山东', unit_conversion=False)

make_dir(solar_summary_path)

if os.path.exists(solar_summary_path + '山东.csv'):
    os.remove(solar_summary_path + '山东.csv')
if os.path.exists(solar_summary_path + '山东_future.csv'):
    os.remove(solar_summary_path + '山东_future.csv')

for sheet in sheets:
    path = solar_city_path + f'{sheet}/'

    summary(input_path=path, output_path=solar_summary_path, category='solar', name=sheet)

summary(input_path=solar_summary_path, output_path=solar_summary_path, category='solar', name='山东', unit_conversion=False)

# In[ ]:
