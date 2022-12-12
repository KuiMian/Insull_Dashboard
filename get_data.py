import pandas as pd

regions = ['山东', '烟台', '德州', '东营', '菏泽', '滨州', '潍坊', '临沂', '青岛',
           '威海', '济南', '济宁', '枣庄', '淄博', '泰安', '日照', '聊城', '莱芜']

# regions = ['山东', '莱芜']

# regions = ['山东']

wind_data_path = 'data/wind_data/summary/'
solar_data_path = 'data/solar_data/summary/'

future = '_future'
suffix = '.csv'


def get_data(region):
    wind_path = wind_data_path + region
    solar_path = solar_data_path + region

    def _get_data(path):
        history_data = pd.read_csv(path + suffix)
        future_data = pd.read_csv(path + future + suffix)
        data = pd.concat([history_data, future_data])

        return data

    wind_data = _get_data(wind_path)
    solar_data = _get_data(solar_path)

    return wind_data, solar_data
