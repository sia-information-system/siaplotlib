import geopandas as gpd
from shapely.geometry import Point


# DatasetPreprocessor
class DataframePreprocessor:
  def __init__(self, dataset):
    self.__dataset = dataset


  def filter_dims(self, dim_conditions):
    return DataframePreprocessor(
      dataset=self.__dataset.sel(dim_conditions, method = 'nearest'))
  
  
  def get_df(self):
    # Convert xarrat.Dataset to pandas.Dataframe.
    df = self.__dataset.to_dataframe()
    # Delete index (dimensions in a netcdf file).
    df.reset_index(inplace=True) 
    return df
  

  def get_geodf(self, lon_dim_name = 'longitude', lat_dim_name = 'latitude'):
    df = self.get_df()
    # Create dimensiones (Points) using longitude and latitude for geopandas.
    geom = [Point(x,y) for x, y in zip(df[lon_dim_name], df[lat_dim_name])]
    # Create GeoDataFrame.
    return gpd.GeoDataFrame(df, geometry=geom)
  

  def get_min(self, var, dim = None):
    mins = self.__dataset.min(dim = dim)
    return float(mins[var])
  

  def get_max(self, var, dim = None):
    mins = self.__dataset.max(dim = dim)
    return float(mins[var])
