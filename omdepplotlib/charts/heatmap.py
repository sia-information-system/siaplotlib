import sys
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np
import io


class HeatMap():
  '''
    Create a heat map chart.

    lon_interval is a list with [west coord, east coord]
    lat_interval is a list with [south coord, north coord]
  '''
  def __init__(
    self,
    dataset, 
    lon_interval = [],
    lat_interval = [],
    lon_data = None,
    lat_data = None,
    vmin=None,
    vmax=None,
    color_palett = 'viridis',
    title = None, 
    label = None,
    build_on_create=True,
    verbose=False
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
      self.verbose = verbose
      self.__fig = None
      self.__fig_path = None

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

    self.__fig = f

    if self.verbose:
      print(f'Image created.', file=sys.stderr)
    
    return self
    

  def plot(self):
    if self.__fig is None:
      # TODO: Raise and appropriate exception class.
      raise Exception('Heatmap figure has not been created.')
    self.__fig.show()
  

  def save(self, filepath):
    if self.__fig is None:
      # TODO: Raise and appropriate exception class.
      raise Exception('Heatmap figure has not been created.')
  
    self.__fig.savefig(filepath, dpi=100, bbox_inches='tight')
    self.__fig_path = filepath
    if self.verbose:
      print(f'Image saved in: {filepath}', file=sys.stderr)
  

  def close(self):
    if self.__fig is not None:
      if self.verbose:
        print('Closing pyplot figure.', file=sys.stderr)
      plt.close(self.__fig)
      self.__fig = None
  

  def to_buffer(self):
    img_buff = io.BytesIO()
    self.__fig.savefig(img_buff, dpi=100, bbox_inches='tight')
    return img_buff
