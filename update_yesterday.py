import numpy as np
import pandas as pd

import datetime

import os
from glob import glob

sheets = ['烟台', '德州', '东营', '菏泽', '滨州', '潍坊', '青岛', '临沂',
          '威海', '济南', '济宁', '淄博', '枣庄', '泰安', '日照', '聊城', '莱芜']
#
# sheets = ['莱芜']

WIND_TARGET = ['datetime', 'windspeed', 'windgust']
SOLAR_TARGET = ['datetime', 'temp', 'cloudcover', 'solarradiation', 'solarenergy']

base_path = 'data/'
wind_data_path = base_path + 'wind_data/'
solar_data_path = base_path + 'solar_data/'
city_path = 'city/'
summary_path = 'summary/'

write_mode = 'w'


def get_csv_files(path, suffix=''):
    return glob(os.path.join(path, f'*{suffix}.csv'))


def merge_history(history_ls, yesterday_ls):
    suffix = '_yesterday.csv'

    data = pd.read_csv(history_ls[-1])

    dates = np.array(data['datetime'], dtype=np.datetime64)
    now = datetime.datetime.now()
    zero_yesterday = now - datetime.timedelta(days=1, hours=now.hour, minutes=now.minute, seconds=now.second,
                                              microseconds=now.microsecond)

    if zero_yesterday in dates:
        print(f'merge pass', end='---')
    else:

        del data, dates

        for filename in history_ls:
            df_history = pd.read_csv(filename)

            yesterday_name = filename[:-4] + suffix

            df_yetserday = pd.read_csv(yesterday_name)

            # os.remove(os.path.join(path, yesterday_name))

            pd.concat([df_history, df_yetserday]).reset_index(drop=True).to_csv(filename[:-4] + '.csv')


def merge_all_history(path):
    path += city_path

    _path = path

    print(f'_path: {_path}')
    for sheet in sheets:
        path += f'{sheet}/'

        all_files = get_csv_files(path)

        future_files = get_csv_files(path, suffix='_future')
        yesterday_files = get_csv_files(path, suffix='_yesterday')
        history_files = list(set(all_files) - set(future_files) - set(yesterday_files))

        merge_history(history_files, yesterday_files)
        print(f'{sheet} merge done.')

        path = _path


def start():
    merge_all_history(wind_data_path)
    merge_all_history(solar_data_path)


start()
