import sys
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import omdepplotlib.charts.general as general_charts
import xarray as xr
import numpy as np


class HeatMap(general_charts.Chart):
  '''
    Create a heat map chart.

    lon_interval is a list with [west coord, east coord]
    lat_interval is a list with [south coord, north coord]
  '''
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
    color_palett: str = 'viridis',
    build_on_create: bool =True,
    verbose: bool = False
    ):
      self.dataset = dataset
      self.title = title
      self.lon_interval = lon_interval
      self.lat_interval = lat_interval
      self.lon_data = lon_data
      self.lat_data = lat_data
      self.label = label
      self.vmin = vmin
      self.vmax = vmax
      self.color_palett = color_palett

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
      cmap=self.color_palett)

    cbar = f.colorbar(im, ax=ax)
    if self.label is not None:
      cbar.set_label(self.label)

    self._fig = f

    if self.verbose:
      print(f'Image created.', file=sys.stderr)
    
    return self
