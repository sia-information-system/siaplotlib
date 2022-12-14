from PIL import Image
import numpy as np
import io
import sys
import pathlib
from omdepplotlib.charts import heatmap
from omdepplotlib.raw_image import ChartImage

class HeatMapBuilder:
  # Public methods.

  def __init__(
    self,
    dataset,
    verbose = False):
      self.dataset = dataset
      self.__chart = None
      self.verbose = verbose


  def build_static(
    self, 
    var: str,
    lat_dim_name: str,
    lon_dim_name: str,
    title: str,
    dim_constraints: dict = {},
    label: str = None,
    color_palett: str = None):
      subset, vmin, vmax, lon_data, lat_data, lon_interval, lat_interval = self.__subset(
        var, dim_constraints, lon_dim_name, lat_dim_name)
      
      self.__chart = heatmap.HeatMap(
        dataset=subset,
        label=label,
        title=title,
        lon_interval=lon_interval,
        lat_interval=lat_interval,
        lat_data=lat_data.data,
        lon_data=lon_data.data,
        vmax=vmax,
        vmin=vmin,
        color_palett=color_palett,
        verbose=self.verbose)
      
      return self


  # TODO: use dime_constraints and thinks in a better way of iterate all avaiable dates in dataset
  def build_gif(
    self,
    var: str,
    lat_dim_name: str,
    lon_dim_name: str,
    time_dim_name: str,
    title: str,
    dim_constraints: dict = {},
    label: str = None,
    color_palett: str = None,
    duration: int = 0.5,
    duration_unit: str = 'SECONDS_PER_FRAME'):
      subset, vmin, vmax, lon_data, lat_data, lon_interval, lat_interval = self.__subset(
        var, dim_constraints, lon_dim_name, lat_dim_name)

      if self.verbose:
        print('Creating images (frames) to create gif.', file=sys.stderr)
      
      chart_list = []
      for  i in range(len(subset[time_dim_name])):
        time_constraint = {}
        time_constraint[time_dim_name] = [i]
        date_subset = subset.isel(time_constraint).squeeze()
        date = np.datetime_as_string(date_subset[time_dim_name].data, unit='D')

        chart = heatmap.HeatMap(
          dataset=date_subset,
          label=label,
          title=f'{title} {date}',
          lon_interval=lon_interval,
          lat_interval=lat_interval,
          lat_data=lat_data.data,
          lon_data=lon_data.data,
          vmax=vmax,
          vmin=vmin,
          color_palett=color_palett,
          verbose=self.verbose)
        
        chart_list.append(chart)
      
      img_buff = self.__make_gif(
        chart_list,
        duration=duration,
        duration_unit=duration_unit)
      
      if self.verbose:
        print('Closing intermediate figures', file=sys.stderr)
      for chart in chart_list:
        chart.close()

      self.__chart = ChartImage(
        img_source=img_buff,
        var=var, 
        title=title, 
        lon_interval=lon_interval, 
        lat_interval=lat_interval,
        label=label)
      
      return self

  
  def save(self, filepath: str | pathlib.Path):
    if type(self.__chart) is heatmap.HeatMap:
      self.__chart.save(filepath)
    else:
      with open(filepath, "wb") as f:
        f.write(self.__chart.get_img_buff().getbuffer())
        if self.verbose:
          print('Gift actually saved.', file=sys.stderr)


  # Private Methods.

  def __subset(self, var: str, dim_constraints: str, lon_dim_name: str, lat_dim_name: str):
    if self.verbose:
      print('Subsetting.', file=sys.stderr)
    subset = self.dataset[var].sel(dim_constraints, method = 'nearest').squeeze()
    vmin = np.round( float(subset.min().data), 3 )
    vmax = np.round( float(subset.max().data), 3 )
    lon_data = subset[lon_dim_name]
    lat_data = subset[lat_dim_name]
    lon_interval = [
      np.round( float(lon_data.min().data), 3 ),
      np.round( float(lon_data.max().data), 3 )
    ]
    lat_interval = [
      np.round( float(lat_data.min().data), 3 ),
      np.round( float(lat_data.max().data), 3 )
    ]
    if self.verbose:
      print('Subsetting done.', file=sys.stderr)
    return subset, vmin, vmax, lon_data, lat_data, lon_interval, lat_interval

  
  def __make_gif(self, charts: list, duration: float = 0.5, duration_unit: str = 'SECONDS_PER_FRAME'):
    if self.verbose:
      print('Making gif.', file=sys.stderr)
    
    frame_duration = None
    if duration_unit == 'SECONDS_PER_FRAME':
      frame_duration = int(duration * 1000)
    elif duration_unit == 'FRAMES_PER_SECOND':
      frame_duration = int(1000 / duration)
    else:
      raise RuntimeError(f'Unit "{duration_unit}" is not supported.')
    
    img_buff = io.BytesIO()
    frames = [Image.open(chart.to_buffer()) for chart in charts]
    frame_one = frames.pop(0)
    frames.append(frames[-1]) # Duplicate last frame to simulate a small stop at the end.
    # Image docs: https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.save
    # GIF docs: https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
    # Durations is defined in milliseconds.
    frame_one.save(
      img_buff, format='GIF', append_images=frames,
      save_all=True, duration=frame_duration, loop=0)
    # Closes all file and destroys the core images object.
    frame_one.close()
    for frame in frames:
        frame.close()
    if self.verbose:
      print(f'Gif created.', file=sys.stderr)
    return img_buff
