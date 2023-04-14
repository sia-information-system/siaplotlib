# Standard
import sys
# Third party
import matplotlib.pyplot as plt
import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import xarray as xr
import numpy as np
# Own
from siaplotlib.charts import base_chart


class ArrowChart(base_chart.Chart):
  """
  Create an ArrowChart.
  """
  def __init__(
    self,
    dataset: xr.Dataset, 
    speed: np.ndarray,
    title: str, 
    data_label: str,
    eastward_var_name: str,
    northward_var_name: str,
    lat_dim_name: str,
    lon_dim_name: str,
    grouping_level: str,
    build_on_create: bool = True,
    log_stream = sys.stderr,
    verbose: bool = False
  ) -> None:
    self.dataset = dataset
    self.speed = speed
    self.title = title
    self.eastward_var_name = eastward_var_name
    self.northward_var_name = northward_var_name
    self.lat_dim_name = lat_dim_name
    self.lon_dim_name = lon_dim_name
    self.grouping_level = grouping_level
    self.data_label = data_label


    super().__init__(log_stream=log_stream, verbose=verbose)

    if build_on_create:
      self.build()


  def build(self):
    self.close()

    data = self.dataset
    grp = self.grouping_level

    vo = data[self.northward_var_name]
    uo = data[self.eastward_var_name]

    lon = data[self.lon_dim_name][::grp]
    lat = data[self.lat_dim_name][::grp]

    fig = plt.figure(figsize=(4, 6))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    cmap = plt.cm.rainbow
    im = ax.quiver(lon,lat, uo[::grp,::grp], vo[::grp,::grp], self.speed[::grp,::grp], cmap=cmap, transform=ccrs.PlateCarree(), pivot='tail')

    ax.coastlines()
    ax.add_feature(cfeature.LAND, facecolor='lightgray')
    plt.title(self.title)
    plt.colorbar(im, label=self.data_label)

    self._fig = ax.figure

    if self.verbose:
      print(f'Image created.', file=sys.stderr)
    
    return self


class RegionMap(base_chart.Chart):
  """
  Create the region map.
  """
  def __init__(
    self,
    amplitude: float,
    lon_dim_min: float,
    lon_dim_max: float,
    lat_dim_min: float,
    lat_dim_max: float,
    build_on_create: bool = True,
    log_stream = sys.stderr,
    verbose: bool = False
  ) -> None:
    super().__init__(log_stream=log_stream, verbose=verbose)
    self.lon_dim_min = lon_dim_min
    self.lon_dim_max = lon_dim_max 
    self.lat_dim_min = lat_dim_min
    self.lat_dim_max = lat_dim_max
    self.amplitude = amplitude

    if build_on_create:
      self.build()

  def build(self):
    self.close()

    # Crear una figura y un objeto de proyección del mapa
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    amp = self.amplitude

    # Establecer los límites del mapa a las coordenadas límite del cuadrilátero
    # Al igual se se agrega la amplitud, la cual esta dada en coordenadas.
    ax.set_extent([self.lon_dim_min - amp, self.lon_dim_max + amp, 
                   self.lat_dim_max + amp, self.lat_dim_min - amp], crs=ccrs.PlateCarree())

    # Personalizar la apariencia del mapa
    ax.add_feature(cfeature.OCEAN, color='lightblue')
    ax.add_feature(cfeature.LAND, color='green')
    ax.coastlines(linewidth=0.5)
    ax.gridlines(draw_labels=True, linewidth=0.5, color='gray', alpha=0.5, linestyle='--')

    # Dibujar las líneas que forman el cuadrilátero
    ax.plot([self.lon_dim_min, self.lon_dim_max, self.lon_dim_max, 
             self.lon_dim_min, self.lon_dim_min], 
            [self.lat_dim_min, self.lat_dim_min,
              self.lat_dim_max, self.lat_dim_max, self.lat_dim_min], 
              color='red', linewidth=2, transform=ccrs.PlateCarree())

    self._fig = ax.figure
    self.log('Image created.')

    return self


class SinglePointTimeSeries(base_chart.Chart):
  """
  In order to plot each series in the graph,
  the following properties of a pandas.Series
  are used as follows.

  * index: used in the 'x' axis.
  * values: used in the 'y' axis.
  * names: used to label the current series.
  """
  def __init__(
    self,
    series_data: list[pd.Series],
    lon: float,
    lat: float,
    lon_interval: list[float],
    lat_interval: list[float],
    title: str,
    grouping_var_label: str,
    y_label: str,
    x_label: str = None,
    show_series_names: bool = True,
    build_on_create: bool = True,
    log_stream = sys.stderr,
    verbose: bool = False
  ) -> None:
    super().__init__(log_stream=log_stream, verbose=verbose)
    self.series_data = series_data
    self.lon = lon
    self.lat = lat
    self.lon_interval = lon_interval
    self.lat_interval = lat_interval
    self.title = title
    self.grouping_var_label = grouping_var_label
    self.y_label = y_label
    self.x_label = x_label
    self.show_series_names = show_series_names

    if build_on_create:
      self.build()


  def build(self):
    # Define the caracteristics of the plot
    fig = plt.figure()
    ax = fig.add_subplot(111)

    for series in self.series_data:
      ax.plot(
        series.index,
        series.values,
        label=series.name)                                                      # plot the time serie

    ax.grid()                                                                            # add the grid lines
    ax.set_title(self.title)
    ax.set_ylabel(self.y_label)
    if self.x_label is not None:
      ax.set_xlabel(self.x_label)
    if self.show_series_names:
      ax.legend(loc='center right', title=self.grouping_var_label)
    fig.suptitle(
      f'Longitude: {self.lon}°\nLatitude: {self.lat}°',
      horizontalalignment='left',
      x=0.12,
      y=1.05)                                                                            # Display the coordinates on the plot
    fig.autofmt_xdate(ha='center')                                                       # format the dates in the x axis

    # Display the location of the point on a mini map
    # .add_axes: https://www.geeksforgeeks.org/how-to-add-axes-to-a-figure-in-matplotlib-with-python/
    ax_mini_map = fig.add_axes([0.74, 0.97, 0.2, 0.2], projection=ccrs.PlateCarree())    # create the minimap and define its projection
    ax_mini_map.add_feature(cfeature.LAND, zorder=1, edgecolor='k')                      # add land mask 
    ax_mini_map.set_extent(self.lon_interval + self.lat_interval, crs=ccrs.PlateCarree()) # define the extent of the map [lon_min,lon_max,lat_min,lat_max]
    ax_mini_map.scatter(self.lon, self.lat, 20, transform=ccrs.PlateCarree())                      # plot the location of the point
    gl = ax_mini_map.gridlines(draw_labels=True)                                         # add the coastlines
    gl.right_labels = False                                                              # remove latitude labels on the right
    gl.top_labels = False                                                                # remove longitude labels on the top

    self._fig = fig
    return self


class SinglePointVerticalProfile(base_chart.Chart):
  """
  In order to plot each series in the graph,
  the following properties of a pandas.Series
  are used as follows.

  * index: used in the 'x' axis.
  * values: used in the 'y' axis.
  * names: used to label the current series.
  """
  def __init__(
    self,
    series_data: list[pd.Series],
    lon: float,
    lat: float,
    lon_interval: list[float],
    lat_interval: list[float],
    title: str,
    grouping_var_label: str,
    y_label: str,
    x_label: str = None,
    show_series_names: bool = True,
    build_on_create: bool = True,
    log_stream = sys.stderr,
    verbose: bool = False
  ) -> None:
    super().__init__(log_stream=log_stream, verbose=verbose)
    self.series_data = series_data
    self.lon = lon
    self.lat = lat
    self.lon_interval = lon_interval
    self.lat_interval = lat_interval
    self.title = title
    self.grouping_var_label = grouping_var_label
    self.y_label = y_label
    self.x_label = x_label
    self.show_series_names = show_series_names

    if build_on_create:
      self.build()
  

  def build(self):
    # Define the caracteristics of the plot
    fig = plt.figure()
    ax = fig.add_subplot(111)

    for series in self.series_data:
      ax.plot(series.index, series.values, label=series.name)

    ax.grid()                                                                           # add the grid lines
    ax.set_title(self.title)
    ax.invert_yaxis()                                                                   # reverse the y axis
    ax.set_xlabel(self.x_label)
    ax.set_ylabel(self.y_label)
    # ax.legend(loc='upper left')
    if self.show_series_names:
      ax.legend(loc='upper left', title=self.grouping_var_label)
    fig.suptitle(
      f'Longitude: {self.lon}°\nLatitude: {self.lat}°',
      horizontalalignment='left',
      x=0.12,
      y=1.05) 

    # Display the location of the point on a mini map
    ax_mini_map = fig.add_axes([0.74, 0.97, 0.2, 0.2], projection=ccrs.PlateCarree())   # create the minimap and define its projection
    ax_mini_map.add_feature(cfeature.LAND, zorder=1, edgecolor='k')                     # add land mask 
    ax_mini_map.set_extent(self.lon_interval + self.lat_interval, crs=ccrs.PlateCarree()) # define the extent of the map [lon_min,lon_max,lat_min,lat_max]
    ax_mini_map.scatter(self.lon, self.lat, 20, transform=ccrs.PlateCarree())           # plot the first location
    gl = ax_mini_map.gridlines(draw_labels=True)                                        # add the coastlines
    gl.right_labels = False                                                             # remove latitude labels on the right
    gl.top_labels = False                                                               # remove longitude labels on the top

    self._fig = fig

    return self
