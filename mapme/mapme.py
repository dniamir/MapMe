import pandas as pd

class MapMe():

    def readjson(self, directory, filename):
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

    def derivetimeintervals(self, json_df):
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
                                       json_df['hour'].astype(str) + ':00')

        return json_df