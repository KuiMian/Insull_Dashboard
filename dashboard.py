import random

from get_data import regions, get_data
from update_data import update_and_summary

import numpy as np

from bokeh.plotting import figure, curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, RangeTool, LinearAxis, Range1d, HoverTool, Button

import datetime


def as_str_time(data):
    return datetime.datetime.strptime(data, '%Y-%m-%dT%H:%M:%S').strftime('%Y.%m.%d %H时')


def get_columnDataSource_and_dates(data):
    dates = np.array(data['datetime'], dtype=np.datetime64)
    data['datetime_str'] = data['datetime'].apply(lambda x: as_str_time(x))
    data['bottom'] = [0] * len(dates)

    source = ColumnDataSource(
        data=dict(date=dates, speed=data['windspeed'], gust=data['windgust'], bottom=data['bottom'],
                  datetime_str=data['datetime_str'], temp=data['temp'], cloud=data['cloudcover'],
                  radiation=data['solarradiation'], energy=data['solarenergy']))

    return source, dates


def get_plot(data):
    source, dates = get_columnDataSource_and_dates(data)

    TOOLS = "xpan, wheel_zoom, save, reset"

    ###########################################

    # plot for windspeed and windgust

    ###########################################

    p_wind = figure(title=region + '     windspeed / windgust(m/s)', width=1450, height=400,
                    tools=TOOLS,  # toolbar_location=None,
                    x_axis_type="datetime", x_axis_location="above",
                    x_range=(dates[-1 - 120], dates[-1])
                    )

    speed_plot = p_wind.line('date', 'speed', line_color='#fdae61', line_width=2, line_alpha=0.9,
                             legend_label='windspeed',
                             source=source)
    p_wind.circle('date', 'speed', line_color='green', line_alpha=0.4, fill_color="white", size=7,
                  legend_label='windspeed',
                  source=source)

    gust_plot = p_wind.line('date', 'gust', line_width=0.5, line_dash="4 4", color='firebrick', legend_label='windgust',
                            source=source)
    p_wind.circle('date', 'gust', line_color='red', fill_color="white", size=8, legend_label='windgust', source=source)
    p_wind.varea('date', 'gust', 'bottom', color='firebrick', alpha=0.1, source=source)

    p_wind.title.text_font_size = '16px'

    p_wind.ygrid.band_fill_color = "olive"
    p_wind.ygrid.band_fill_alpha = 0.05

    p_wind.legend.location = 'top_left'
    p_wind.legend.click_policy = 'hide'

    speed_tips = """
        <div>
            <span style="font-size: 16px;">@datetime_str</span>&nbsp;
        </div>
        <div>
            <span style="font-size: 13px; color: black; font-weight: bold;">Speed</span>&nbsp;
            <span style="font-size: 17px; font-weight: bold;">@speed m/s</span>&nbsp;
        </div>
        """

    p_wind.add_tools(HoverTool(tooltips=speed_tips, renderers=[speed_plot]))

    gust_tips = """
        <div>
            <span style="font-size: 16px;">@datetime_str</span>&nbsp;
        </div>
        <div>
            <span style="font-size: 13px; color: black; font-weight: bold;">Gust</span>&nbsp;
            <span style="font-size: 17px; font-weight: bold;">@gust m/s</span>&nbsp;
        </div>
        """

    p_wind.add_tools(HoverTool(tooltips=gust_tips, renderers=[gust_plot]))

    ###########################################

    # plot for solarenergy and solar radiation

    ###########################################

    p_solar = figure()
    p_solar = figure(title=region + '     solarradiation(W/m^2) / solarenergy(MJ/m^2)', width=1450, height=400,
                     tools=TOOLS,  # toolbar_location=None,
                     x_axis_type="datetime", x_axis_location="above",
                     x_range=p_wind.x_range, y_range=(0, 1000)
                     )

    radiation_plot = p_solar.line('date', 'radiation', line_color='#fdae61', line_width=2, line_alpha=0.9,
                             legend_label='solarradiation',
                             source=source)
    p_solar.circle('date', 'radiation', line_color='green', line_alpha=0.4, fill_color="white", size=7,
                  legend_label='solarradiation',
                  source=source)

    p_solar.extra_y_ranges['energy'] = Range1d(0, 5)

    energy_plot = p_solar.line('date', 'energy', line_width=0.5, line_dash="4 4", color='firebrick', legend_label='solarenergy',
                            source=source, y_range_name='energy')
    p_solar.circle('date', 'energy', line_color='red', fill_color="white", size=8, legend_label='solarenergy', source=source, y_range_name='energy')
    p_solar.varea('date', 'energy', 'bottom', color='firebrick', alpha=0.1, source=source, y_range_name='energy')

    ax_energy = LinearAxis(y_range_name="energy")  # , axis_label="solar energy(MJ/m^2)")
    ax_energy.axis_label_text_color = "navy"
    p_solar.add_layout(ax_energy, 'right')

    p_solar.title.text_font_size = '16px'

    p_solar.ygrid.band_fill_color = "olive"
    p_solar.ygrid.band_fill_alpha = 0.05

    p_solar.legend.location = 'top_left'
    p_solar.legend.click_policy = 'hide'

    radiation_tips = """
            <div>
                <span style="font-size: 18px;">@datetime_str</span>&nbsp;
            </div>
            <div>
                <span style="font-size: 13px; color: black; font-weight: bold;">radiation</span>&nbsp;
                <span style="font-size: 15px; font-weight: bold;">@radiation W/m^2</span>&nbsp;
            </div>
            """

    p_solar.add_tools(HoverTool(tooltips=radiation_tips, renderers=[radiation_plot]))

    energy_tips = """
            <div>
                <span style="font-size: 18px;">@datetime_str</span>&nbsp;
            </div>
            <div>
                <span style="font-size: 13px; color: black; font-weight: bold;">energy</span>&nbsp;
                <span style="font-size: 15px; font-weight: bold;">@energy MJ/m^2</span>&nbsp;
            </div>
            """

    p_solar.add_tools(HoverTool(tooltips=energy_tips, renderers=[energy_plot]))

    ###########################################

    # plot for cloud cover and temp

    ###########################################

    p_cloud_and_temp = figure(title=region + '     cloudcover(%) / temperature(°C)', width=1450, height=400,
                              tools=TOOLS,  # toolbar_location=None,
                              x_axis_type="datetime", x_axis_location="above",
                              x_range=p_wind.x_range, y_range=(-20, 50)
                              )

    p_cloud_and_temp.line('date', 'temp', line_color='#F5E2A7', line_width=3, line_alpha=0.5, legend_label='temperature',
                          source=source)
    temp_plot = p_cloud_and_temp.circle('date', 'temp', line_color='#FDC072', fill_color='white', size=6,
                                        legend_label='temperature', source=source)

    p_cloud_and_temp.extra_y_ranges['cloud'] = Range1d(0, 105)

    p_cloud_and_temp.line('date', 'cloud', color='#364B9A', line_width=1.5, line_dash='4 4', legend_label='cloudcover',
                          source=source, y_range_name='cloud')
    cloud_plot = p_cloud_and_temp.circle('date', 'cloud', line_color='#77AED1', fill_color='white', size=7,
                                         legend_label='cloudcover', source=source, y_range_name='cloud')
    p_cloud_and_temp.varea('date', y1='cloud', y2='bottom', color='#A5D2E5', alpha=0.3, source=source,
                           y_range_name='cloud')

    ax_cloud = LinearAxis(y_range_name="cloud")  # , axis_label="cloud cover(percentage)")
    ax_cloud.axis_label_text_color = "navy"
    p_cloud_and_temp.add_layout(ax_cloud, 'right')

    p_cloud_and_temp.title.text_font_size = '16px'

    p_cloud_and_temp.ygrid.band_fill_color = "olive"
    p_cloud_and_temp.ygrid.band_fill_alpha = 0.05

    p_cloud_and_temp.legend.location = 'top_left'
    p_cloud_and_temp.legend.click_policy = 'hide'

    temp_tips = """
            <div>
                <span style="font-size: 16px;">@datetime_str</span>&nbsp;
            </div>
            <div>
                <span style="font-size: 13px; color: black; font-weight: bold;">Temp</span>&nbsp;
                <span style="font-size: 17px; font-weight: bold;">@temp °C</span>&nbsp;
            </div>
            """

    p_cloud_and_temp.add_tools(HoverTool(tooltips=temp_tips, renderers=[temp_plot]))

    cloud_tips = """
            <div>
                <span style="font-size: 16px;">@datetime_str</span>&nbsp;
            </div>
            <div>
                <span style="font-size: 13px; color: black; font-weight: bold;">Cloud</span>&nbsp;
                <span style="font-size: 17px; font-weight: bold;">@cloud %</span>&nbsp;
            </div>
            """

    p_cloud_and_temp.add_tools(HoverTool(tooltips=cloud_tips, renderers=[cloud_plot]))

    ###########################################

    # plot for range tool

    ###########################################

    select = figure(title="Range tool", width=1450, height=130,

                    x_axis_type="datetime", y_axis_type=None,
                    y_range=p_wind.y_range,

                    tools="", toolbar_location=None,
                    background_fill_color="#009E73", background_fill_alpha=0.05)

    range_tool = RangeTool(x_range=p_wind.x_range)
    range_tool.overlay.fill_color = "navy"
    range_tool.overlay.fill_alpha = 0.1

    select.line('date', 'speed', line_color='purple', source=source)
    select.ygrid.grid_line_color = None
    select.add_tools(range_tool)
    select.toolbar.active_multi = range_tool

    my_plot = [p_wind, p_solar, p_cloud_and_temp, select]

    return my_plot, source


# create a callback that adds a number in a random location
def callback():
    update_and_summary()

    for region in regions:
        data = get_data(region)
        new_source, _ = get_columnDataSource_and_dates(data)
        source[region].data = dict(new_source.data)


# add a button widget and configure with the call back
button = Button(label="refresh Me")
button.on_event('button_click', callback)

plots = dict()
source = dict()
plot_all = [button]

for region in regions:
    data = get_data(region)
    plots[region], source[region] = get_plot(data)
    plot_all.extend(plots[region])

# put the button and plot in a layout and add to the document
curdoc().add_root(column(*plot_all))
