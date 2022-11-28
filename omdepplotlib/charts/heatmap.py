import pathlib
import sys
import geopandas as gpd
import matplotlib.pyplot as plt
import io

VISUALIZATIONS_DIR = pathlib.Path(pathlib.Path(__file__).parent.absolute(), '..', '..', '..', 'tmp', 'visualizations')

class HeatMap():
  '''
    Create a heat map chart.

    limit_coord_lon is a list with [west coord, east coord]
    limit_coord_lat is a list with [south coord, north coord]
  '''
  def __init__(
    self,
    gdf, 
    var, 
    title, 
    limit_coord_lon=[-90, -80], 
    limit_coord_lat=[10, 30],
    has_legend=True,
    name_legend='',
    vmin=None,
    vmax=None,
    build_on_create=True,
    verbose=True
    ):
      self.__world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
      self.gdf = gdf
      self.var = var
      self.title = title
      self.limit_coord_lon = limit_coord_lon
      self.limit_coord_lat = limit_coord_lat
      self.has_legend = has_legend
      self.name_legend = name_legend
      self.vmin = vmin
      self.vmax = vmax
      self.verbose = verbose
      self.__fig = None
      self.__fig_path = None

      if build_on_create:
        self.build()


  def build(self):
    self.close()
    
    ax = self.__world.plot()
    self.gdf.plot(
      ax=ax, 
      column=self.var, 
      legend=self.has_legend, 
      legend_kwds={'label': self.name_legend}, 
      cmap='OrRd',
      vmin=self.vmin,
      vmax=self.vmax)

    ax.set_xlim(self.limit_coord_lon[0], self.limit_coord_lon[1])
    ax.set_ylim(self.limit_coord_lat[0], self.limit_coord_lat[1])
    ax.set_title(self.title)

    self.__fig = plt.gcf()

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
      print('Closing pyplot figure.', file=sys.stderr)
      plt.close(self.__fig)
      self.__fig = None
  

  def to_buffer(self):
    img_buff = io.BytesIO()
    self.__fig.savefig(img_buff, dpi=100, bbox_inches='tight')
    return img_buff
