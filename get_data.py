import numpy as np
import pandas as pd

# regions = ['山东', '烟台', '德州', '东营','菏泽', '滨州', '潍坊', '青岛', '临沂',
#           '威海', '济南', '济宁', '淄博', '枣庄', '泰安', '日照', '聊城', '莱芜']

regions = ['山东', '莱芜']

# regions = ['山东']

data_path = 'data/wind_data/summary/'
future = '_future'
suffix = '.csv'


def get_data(region):
    path = data_path + region

    history_data = pd.read_csv(path + suffix)
    future_data = pd.read_csv(path + future + suffix)
    data = pd.concat([history_data, future_data])

    return data