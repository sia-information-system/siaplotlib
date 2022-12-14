from PIL import Image
import numpy as np
import io
import sys
import pathlib
from omdepplotlib.charts import heatmap
from omdepplotlib.charts.raw_image import ChartImage
from omdepplotlib.preprocessing import subsetting
import xarray as xr

class HeatMapBuilder:
  # Public methods.

  def __init__(
    self,
    dataset: xr.DataArray,
    verbose: bool = False):
      self.dataset = dataset
      self._chart = None
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
      subset, vmin, vmax = subsetting.slice_dice(
        dataset=self.dataset,
        dim_constraints=dim_constraints,
        var=var)
      
      lon_data, lat_data, lon_interval, lat_interval = subsetting.get_coords(
        dataset=subset,
        lon_dim_name=lon_dim_name,
        lat_dim_name=lat_dim_name)
      
      self._chart = heatmap.HeatMap(
        dataset=subset,
        label=label,
        title=title,
        lon_interval=lon_interval,
        lat_interval=lat_interval,
        lat_data=lat_data,
        lon_data=lon_data,
        vmax=vmax,
        vmin=vmin,
        color_palett=color_palett,
        verbose=self.verbose)
      
      return self


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
      subset, vmin, vmax = subsetting.slice_dice(
        dataset=self.dataset,
        dim_constraints=dim_constraints,
        var=var)
      
      lon_data, lat_data, lon_interval, lat_interval = subsetting.get_coords(
        dataset=subset,
        lon_dim_name=lon_dim_name,
        lat_dim_name=lat_dim_name)

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
          lat_data=lat_data,
          lon_data=lon_data,
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

      self._chart = ChartImage(
        img_source=img_buff,
        var=var, 
        title=title, 
        lon_interval=lon_interval, 
        lat_interval=lat_interval,
        label=label)
      
      return self

  
  def save(self, filepath: str | pathlib.Path):
    if type(self._chart) is heatmap.HeatMap:
      self._chart.save(filepath)
    else:
      with open(filepath, "wb") as f:
        f.write(self._chart.get_img_buff().getbuffer())
        if self.verbose:
          print('Gift actually saved.', file=sys.stderr)


  # Private Methods.
  
  def __make_gif(self, charts: list, duration: float = 0.5, duration_unit: str = 'SECONDS_PER_FRAME'):
    if self.verbose:
      print('Making gif.', file=sys.stderr)
    
    frame_duration = None
    if duration_unit == 'SECONDS_PER_FRAME':
      frame_duration = np.round(duration * 1000)
    elif duration_unit == 'FRAMES_PER_SECOND':
      frame_duration = np.round(1000 / duration)
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
