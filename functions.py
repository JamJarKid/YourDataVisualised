!pip install gmplot
import gmplot
import pandas as pd
from pandas.io.json import json_normalize

def json_to_df(filepath, full=False):
    """
    Return DataFrame with location data from json document.
    
    Args:
      filepath: filepath of the json document
      full: if True, returns all the data in the json file, 
            if False (default) returns the data needed to plot the data
    Returns: 
            DataFrame with location data
    """
    
    #read in data
    json_data = pd.read_json(filepath)['locations']
    
    #turn into usable format
    location_data = json_normalize(data=json_data.values.tolist())
    
    #Turn longitude and latitude to normal ranges 
    location_data.loc[:,['latitudeE7', 'longitudeE7']] = location_data[['latitudeE7', 'longitudeE7']]/1e7

    #Convert time in ms to datetime
    location_data['timestampMs'] = pd.to_datetime(location_data['timestampMs'], unit='ms')
    location_data = location_data.rename({'timestampMs':'time'}, axis='columns')
    location_data = location_data.set_index('time')
    
    if full:
        #Clean activity column
        location_data.loc[location_data['activity'].notnull(), 'activity'] = location_data.loc[location_data['activity'].notnull()]['activity'].apply(lambda x:x[0]['activity'][0]['type'])
        location_data.loc[location_data['activity'].isnull(), 'activity'] = 'Unknown'
    else:
        #Drop columns that do not contribute directly to the gmap plotting
        extra_data = ['verticalAccuracy', 'velocity', 'heading', 'altitude', 'activity', 'accuracy']
        location_data = location_data.drop(extra_data, axis=1)
        location_data.columns = ['latitude', 'longitude']
        
def line(df, filename):
    """
    Returns line plot from location data
    
    Args:
        df: DataFrame in the same format returned by json_to_df
        filename: User defined filename for the plot
        
    Returns:
        Downloads .html file to computer
        None
    """
    
    if filename.endswith('.html'):
        pass
    else: filename = filename + '.html'
    
    min_lat, max_lat = min(df['latitude']), max(df['latitude'])
    min_lon, max_lon = min(df['longitude']), max(df['longitude'])
    
    mymap = gmplot.GoogleMapPlotter((max_lat + min_lat) / 2, (max_lon + min_lon) / 2, 7, apikey='AIzaSyAA7rltyt7Ow_ubEtdt3kRimmnM8BUGlzg')

    mymap.plot(df['latitude'], df['longitude'], 'blue', edge_width=1)
    
    mymap.draw(filename)
    
    return 'Plot downloaded'

def scatter(df, filename = 'mymap.html'):
    """
    Returns scatter plot from location data
    
    Args:
        df: DataFrame in the same format returned by json_to_df
        filename: User defined filename for the plot
        
    Returns:
        Downloads .html file to computer
        None
    """
    if filename.endswith('.html'):
        pass
    else: filename = filename + '.html'
    
    min_lat, max_lat = min(df['latitude']), max(df['latitude'])
    min_lon, max_lon = min(df['longitude']), max(df['longitude'])
    
    mymap = gmplot.GoogleMapPlotter((max_lat + min_lat) / 2, (max_lon + min_lon) / 2, 7, apikey='AIzaSyAA7rltyt7Ow_ubEtdt3kRimmnM8BUGlzg')

    mymap.scatter(tuple(df.latitude), tuple(df.longitude), 'blue', size=1000, marker=False)
    
    mymap.draw(filename)
    
    return 'Plot downloaded'

def heatmap(df, filename):
    """
    Returns heatmap from location data
    
    Args:
        df: DataFrame in the same format returned by json_to_df
        filename: User defined filename for the plot
        
    Returns:
        Downloads .html file to computer
        None
    """

    if filename.endswith('.html'):
        pass
    else: filename = filename + '.html'
    
    min_lat, max_lat = min(df['latitude']), max(df['latitude'])
    min_lon, max_lon = min(df['longitude']), max(df['longitude'])
    
    mymap = gmplot.GoogleMapPlotter((max_lat + min_lat) / 2, (max_lon + min_lon) / 2, 7, apikey='AIzaSyAA7rltyt7Ow_ubEtdt3kRimmnM8BUGlzg')

    mymap.heatmap(tuple(df.latitude), tuple(df.longitude), threshold=0.00001, radius=10)
    
    mymap.draw(filename)
    
    return 'Plot downloaded'
        
    return location_data