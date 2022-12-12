from get_data import regions, get_data
from get_plot import get_plot

from bokeh.plotting import show, column


plots = dict()
source = dict()
plot_all = []

for region in regions:
    wind_data, solar_data = get_data(region)
    plots[region], source[region] = get_plot(wind_data, solar_data, region)
    plot_all.extend(plots[region])


# show(column(*plot_all))
