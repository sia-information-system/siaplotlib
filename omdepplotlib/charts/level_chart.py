import sys
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from omdepplotlib.charts import base_chart
import xarray as xr
import numpy as np


class HeatMap(base_chart.Chart):
  """
  Create a heat map chart.

  lon_interval is a list with [west coord, east coord]
  lat_interval is a list with [south coord, north coord]
  """
  def __init__(
    self,
    dataset: xr.DataArray, 
    lon_interval: list,
    lat_interval: list,
    lon_data: np.ndarray,
    lat_data: np.ndarray,
    vmin: float,
    vmax: float,
    title: str, 
    label: str = None,
    color_palette: str = 'viridis',
    build_on_create: bool =True,
    verbose: bool = False
  ) -> None:
    self.dataset = dataset
    self.title = title
    self.lon_interval = lon_interval
    self.lat_interval = lat_interval
    self.lon_data = lon_data
    self.lat_data = lat_data
    self.label = label
    self.vmin = vmin
    self.vmax = vmax
    self.color_palette = color_palette

    super().__init__(verbose = verbose)

    if build_on_create:
      self.build()


  def build(self):
    self.close()
    
    # Definition of the plot features.
    f = plt.figure()
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.coastlines()
    ax.add_feature(cfeature.LAND, zorder=1, edgecolor='k')
    ax.set_extent(self.lon_interval + self.lat_interval, crs=ccrs.PlateCarree())
    ax.set_title(self.title)
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True)
    gl.right_labels = False
    gl.top_labels = False
    gl.rotate_labels = True

    im = ax.pcolor(
      self.lon_data,
      self.lat_data,
      self.dataset,
      vmin=self.vmin,
      vmax=self.vmax,
      cmap=self.color_palette)

    cbar = f.colorbar(im, ax=ax)
    if self.label is not None:
      cbar.set_label(self.label)

    self._fig = f

    if self.verbose:
      print(f'Image created.', file=sys.stderr)
    
    return self


class ContourMap(base_chart.Chart):
  """
  Create a heat map chart.

  lon_interval is a list with [west coord, east coord]
  lat_interval is a list with [south coord, north coord]
  """
  def __init__(
    self,
    dataset: xr.DataArray, 
    lon_interval: list,
    lat_interval: list,
    lon_data: np.ndarray,
    lat_data: np.ndarray,
    vmin: float,
    vmax: float,
    num_levels: int,
    title: str, 
    label: str = None,
    color_palette: str = 'viridis', # Not in use.
    build_on_create: bool =True,
    verbose: bool = False
  ) -> None:
    super().__init__(verbose=verbose)
    self.dataset = dataset
    self.title = title
    self.lon_interval = lon_interval
    self.lat_interval = lat_interval
    self.lon_data = lon_data
    self.lat_data = lat_data
    self.label = label
    self.vmin = vmin
    self.vmax = vmax
    self.num_levels = num_levels
    self.color_palette = color_palette

    if build_on_create:
      self.build()


  def build(self):
    self.close()

    # Define the caracteristics of the plot
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax.set_global()
    ax.coastlines()
    ax.add_feature(cfeature.LAND, zorder=1, edgecolor='k')
    ax.set_extent(self.lon_interval + self.lat_interval, crs=ccrs.PlateCarree())
    ax.set_title(self.title)
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True)
    gl.right_labels = False
    gl.top_labels = False
    gl.rotate_labels = True

    x = self.lon_data
    y = self.lat_data
    z = self.dataset

    # Add colourful filled contours.
    filled_c = ax.contourf(
      x, y, z, 
      transform=ccrs.PlateCarree(), 
      levels=np.linspace(self.vmin, self.vmax, self.num_levels), 
      vmin=self.vmin, 
      vmax=self.vmax)

    # Add a colorbar for the filled contour.
    cbar = fig.colorbar(filled_c, ax=ax)
    if self.label is not None:
      cbar.set_label(self.label)

    # And black line contours.
    line_c = ax.contour(
      x, y, z,
      levels=filled_c.levels,
      colors=['black'],
      transform=ccrs.PlateCarree())
    
    self._fig = fig

    if self.verbose:
      print(f'Image created.', file=sys.stderr)
    
    return self

class VerticalSlice(base_chart.Chart):
  def __init__(
    self,
    x_values: np.ndarray,
    y_values: np.ndarray,
    z_values: np.ndarray,
    vmin: float,
    vmax: float,
    lon_interval: list[float],
    lat_interval: list[float],
    title: str,
    measure_label: str,
    y_label: str,
    x_label: str = None,
    color_palette: str = 'plasma',
    build_on_create: bool = True,
    verbose=False
  ) -> None:
    super().__init__(verbose=verbose)
    self.x_values = x_values
    self.y_values = y_values
    self.z_values = z_values
    self.vmin = vmin
    self.vmax = vmax
    self.lon_interval = lon_interval
    self.lat_interval = lat_interval
    self.title = title
    self.measure_label = measure_label
    self.y_label = y_label
    self.x_label = x_label
    self.color_palette = color_palette

    if build_on_create:
      self.build()


  def build(self):
    # Define the caracteristics of the plot
    f = plt.figure()                                                      # create a figure and define its size
    ax = f.add_subplot(111)                                               # create the axes of the plot
    ax.set_title(self.title)                                              # set the title of the figure
    ax.set_ylabel(self.y_label)                                           # set the  y axis label
    ax.set_xlabel(self.x_label)                                           # set the  y axis label
    ax.invert_yaxis()                                                     # reverse the y axis 

    im = ax.pcolor(
      self.x_values,
      self.y_values,
      self.z_values,
      vmin=self.vmin,
      vmax=self.vmax,
      cmap=self.color_palette)                                            # display the temperature
    cbar = f.colorbar(im,ax=ax)                                           # add the colorbar
    cbar.set_label(self.measure_label)                                    # add the title of the colorbar

    # Display the locations of the line on a mini map
    ax_mini_map = f.add_axes([0.74, 0.97, 0.2, 0.2], projection=ccrs.PlateCarree())  # create the minimap and define its projection
    gl = ax_mini_map.gridlines(draw_labels=True)                                     # add the coastlines
    gl.right_labels = False                                                          # remove latitude labels on the right
    gl.top_labels = False                                                            # remove longitude labels on the top
    ax_mini_map.add_feature(cfeature.LAND, zorder=1, edgecolor='k')                  # add land mask 
    ax_mini_map.set_extent(
      self.lon_interval + self.lat_interval,
      crs=ccrs.PlateCarree())                                                        # define the extent of the map [lon_min,lon_max,lat_min,lat_max]
    ax_mini_map.plot(self.lon_interval,self.lat_interval,'r')                        # add the location of the line on the mini map
    self._fig = f
