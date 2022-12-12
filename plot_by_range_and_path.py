import numpy as np
import pandas as pd

from bokeh.plotting import figure, show
from bokeh.layouts import column
from bokeh.palettes import Sunset5


wind_data_path = '../data/wind_data/summary/山东_future.csv'
solar_data_path = '../data/solar_data/summary/山东_future.csv'


def plot_lines(path_list):

    p1 = figure(title='windgust对比', x_axis_type="datetime", width=1400, height=600)
    p2 = figure(title='solarenergy对比', x_axis_type="datetime", width=1400, height=600)

    for i, path in enumerate(path_list):
        wind_path = path + wind_data_path
        solar_path = path + solar_data_path

        wind_data = pd.read_csv(wind_path)
        solar_data = pd.read_csv(solar_path)

        dates = np.array(wind_data['datetime'], dtype=np.datetime64)

        p1.line(dates, wind_data['windgust'], color=Sunset5[i], legend_label=path[:11])  # 2022_01_01a
        p2.line(dates, solar_data['solarenergy'], color=Sunset5[i], legend_label=path[:11])

    show(column(p1, p2))


plot_lines([''])