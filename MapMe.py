import os
import pandas as pd
from plotly.graph_objs import *
import plotly
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

class MapMeClass:
    """ Class for all Google Location Services functions and properties"""

    def __init__(self, directory, filename):
        self.data = self.__ReadJson(directory, filename)
        self.data = self.__DeriveTimeIntervals(self.data)
        self.data = self.__FixLatLong(self.data)

    def __ReadJson(self, directory, filename):
        """ Read JSON file provided by Google Location Services into a Dataframe

        args:
            directory: location of the json file
            filename: name of the json file

        returns:
            json_df dataframe containing the json data
        """
        path = os.path.join(directory, filename)
        json_data = pd.read_json(path, orient='values')
        dict_list = json_data['locations'].tolist()
        json_df = pd.DataFrame.from_dict(dict_list)
        json_df = json_df.filter(items=['latitudeE7', 'longitudeE7', 'timestampMs'])
        return json_df

    def __DeriveTimeIntervals(self, json_df):
        """ Derive time properties from Google location services josn file time stamp

        args:
            df: location of the json file

        returns:
            json_df dataframe containing the json data
        """
        date_time = pd.to_datetime(json_df['timestampMs'], unit='ms')
        json_df['year'] = date_time.dt.year
        json_df['month'] = date_time.dt.month
        json_df['day'] = date_time.dt.day
        json_df['hour'] = date_time.dt.hour
        json_df['min'] = date_time.dt.minute
        json_df['sec'] = date_time.dt.second

        json_df['timestamp_fixed'] = date_time.dt.to_pydatetime()
        json_df['timestamp_string'] = (json_df['month'].astype(str) + '/' +
                                       json_df['day'].astype(str) + '/' +
                                       json_df['year'].astype(str).astype(str) + ' ' +
                                       json_df['hour'].astype(str) + ':' +
                                       json_df['min'].astype(str))

        return json_df

    def __FixLatLong(self, json_df):
        """ Fix Lat and Long coordinates so Google Maps can Read them

        args:
            json_df: Dataframe derived from Jason file

        returns:
            json_df: Same Dataframe with updated latitude and longitude
        """
        json_df['latitudeE7'] = json_df['latitudeE7'] / 10000000
        json_df['longitudeE7'] = json_df['longitudeE7'] / 10000000
        return json_df

    def __SetScatterData(self,
                         mode='markers',
                         markersize=10,
                         markercolour='rgb(255,0,0)',
                         opacity=0.3):

        marker_dict = dict(size=markersize,
                           color=markercolour,
                           opacity=opacity,)

        scatter_dict = dict(lat=self.data['latitudeE7'],
                            lon=self.data['longitudeE7'],
                            mode=mode,
                            text=self.data['timestamp_string'],
                            marker=marker_dict)

        self.scatterdata = Data([Scattermapbox(scatter_dict)])

    def __SetLayout(self,
                    height=800,
                    width=1200,
                    style='outdoors',
                    mapbox_access_token=None):

        center_dict = dict(lat=self.data['latitudeE7'].values[0],
                           lon=self.data['longitudeE7'].values[0]
                           )

        mapbox_dict =dict(accesstoken=mapbox_access_token,
                          bearing=0,
                          center=center_dict,
                          pitch=0,
                          zoom=10,
                          style=style,
                          )

        layout_dict = dict(autosize=True,
                           height=height,
                           width=width,
                           hovermode='closest',
                           mapbox=mapbox_dict
                          )

        self.layout = Layout(layout_dict)

    def Filter(self, filter):
        """ Filter MapMeClass data by index

        args:
            filter: Boolean series filter
        """
        self.data = self.data.loc[filter, :]

    def PlotMap(self,
                mode='markers',
                markersize=10,
                markercolour='rgb(255,0,0)',
                opacity=0.3,
                height=800,
                width=1200,
                style='outdoors',
                mapbox_access_token=None):
        """ Plot location data on a plotly interactive map

        args:
            mode: Type of plot
            markersize: Marker size
            markercolour: Marker colour
            opacity: Marker opacity
            height: Height of figure
            width: Width of figure
            style: Style of map
            mapbox_access_token: Token required to access mapbox

        return:
            self.fig: plotly figure
        """

        # Set Data and Layout
        self.__SetScatterData(mode=mode,
                              markersize=markersize,
                              markercolour=markercolour,
                              opacity=opacity,)

        self.__SetLayout(height=height,
                         width=width,
                         style=style,
                         mapbox_access_token=mapbox_access_token)

        # Plot Data
        init_notebook_mode(connected=True);
        plotly.offline.init_notebook_mode();
        self.fig = dict(data=self.scatterdata, layout=self.layout)
        plotly.offline.plot(self.fig)
        return self.fig


