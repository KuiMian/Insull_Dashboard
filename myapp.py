# myapp.py

from random import random

from bokeh.layouts import column
from bokeh.models import Button, ColumnDataSource
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc

import time

# create a plot and style its properties
p = figure(x_range=(0, 100), y_range=(0, 100), toolbar_location=None)
# p.border_fill_color = 'black'
p.background_fill_color = '#fafafa'
# p.outline_line_color = None
# p.grid.grid_line_color = None

source = ColumnDataSource(dict(x=[], y=[]))

# add a text renderer to the plot (no data yet)
p.circle('x', 'y', size=random()*40, source=source)

i = 0

def f(functions):
    print(f'{functions} done.')
    return functions

def f1():
    pass

def f2():
    pass

# create a callback that adds a number in a random location
def callback():

    global i

    # BEST PRACTICE --- update .data in one step with a new dict
    new_data = dict()
    # new_data['x'] = ds.data['x'] + [random()*70 + 15]
    # new_data['y'] = ds.data['y'] + [random()*70 + 15]
    # new_data['line_color'] = ds.data['line_color'] + [RdYlBu3[i%3]]

    new_data['x'] = [random()*70 + 15]
    new_data['y'] = [random()*70 + 15]
    new_data['line_color'] = [RdYlBu3[i%3]]

    f(f1)
    f(f2)

    source.data = new_data


# add a button widget and configure with the call back
button = Button(label="refresh Me")
button.on_event('button_click', callback)

# put the button and plot in a layout and add to the document
curdoc().add_root(column(button, p))