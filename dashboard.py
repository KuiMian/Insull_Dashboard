from get_data import regions, get_data
from get_plot import get_columnDataSource_and_dates, get_plot
from update_data import update_and_summary

from bokeh.plotting import curdoc, column
from bokeh.models import Button


# from bokeh.server.server import Server


# def dashboard(doc):

# create a callback that adds a number in a random location
def callback():
    update_and_summary()

    for region in regions:
        wind_data, solar_data = get_data(region)
        new_source, _ = get_columnDataSource_and_dates(wind_data, solar_data)
        source[region].data = dict(new_source.data)


# add a button widget and configure with the call back
button = Button(label="refresh Me")
button.on_event('button_click', callback)

plots = dict()
source = dict()
plot_all = [button]

for region in regions:
    wind_data, solar_data = get_data(region)
    plots[region], source[region] = get_plot(wind_data, solar_data, region)
    plot_all.extend(plots[region])

# put the button and plot in a layout and add to the document
curdoc().add_root(column(*plot_all))
# doc.add_root(*plot_all)

# server = Server({'/dashboard': dashboard})
# server.start
