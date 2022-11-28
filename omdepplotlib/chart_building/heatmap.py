import pathlib
from PIL import Image
import os
import numpy as np
import io
import sys
from omdepplotlib.charts import heatmap
from omdepplotlib.raw_image import ChartImage

class HeatMapBuilder:
  def __init__(self, preprocesor, out_dir = None):
    self.preprocesor = preprocesor
    self.out_dir = out_dir
    self.__chart = None


  def build_static(
    self, 
    var, 
    chart_title, 
    limit_coord_lon=[-90, -80], 
    limit_coord_lat=[10, 30],
    dim_constraints = {},
    has_legend=True,
    name_legend=''):
      gdf = self.preprocesor.filter_dims(dim_constraints).get_geodf()
      self.__chart = heatmap.HeatMap(
        gdf=gdf, 
        var=var, 
        title=f'{chart_title}', 
        limit_coord_lon=limit_coord_lon, 
        limit_coord_lat=limit_coord_lat, 
        has_legend=has_legend,
        name_legend=name_legend)
      
      return self


  def __make_gif(self, charts):
    img_buff = io.BytesIO()
    frames = [Image.open(chart.to_buffer()) for chart in charts]
    frame_one = frames[0]
    frames.pop(0)
    frames.append(frames[-1]) # Duplicate last frame to simulate a small stop at the end.
    frame_one.save(
      img_buff, format='GIF', append_images=frames,
      save_all=True, duration=500, loop=0)
    
    # Closes all file and destroys the core images object.
    frame_one.close()
    for frame in frames:
        frame.close()
    print(f'Gif created.')
    return img_buff


  # TODO: use dime_constraints and thinks in a better way of iterate all avaiable dates in dataset
  def build_gif(
    self,
    var, 
    chart_title, 
    limit_coord_lon=[-90, -80], 
    limit_coord_lat=[10, 30],
    dim_constraints = {},
    time_dim_name = 'time',
    has_legend=True,
    name_legend=''):
      vmin = np.round(self.preprocesor.get_min(var))
      vmax = np.round(self.preprocesor.get_max(var))

      print('Creating images (frames) to create gif.')
      # TODO: Use start_date and end_date from parameters.
      chart_list = []
      for i in range(1, 13):
        month = '0'+str(i) if i < 10 else i
        date = f'2020-{month}-01'
        dim_constraints[time_dim_name] = [date]
        gdf = self.preprocesor.filter_dims(dim_constraints).get_geodf()

        chart = heatmap.HeatMap(
          gdf=gdf, 
          var=var, 
          title=f'{chart_title} {date}', 
          limit_coord_lon=limit_coord_lon, 
          limit_coord_lat=limit_coord_lat, 
          has_legend=has_legend,
          name_legend=name_legend,
          vmin=vmin,
          vmax=vmax,
          verbose=False)
        
        chart_list.append(chart)
      
      print('Making gif.')
      img_buff = self.__make_gif(chart_list)
      print('Closing intermediate figures', file=sys.stderr)
      for chart in chart_list:
        chart.close()

      self.__chart = ChartImage(
        img_source=img_buff,
        var=var, 
        title=chart_title, 
        limit_coord_lon=limit_coord_lon, 
        limit_coord_lat=limit_coord_lat,
        has_legend=has_legend,
        name_legend=name_legend)
      
      return self

  
  def save(self, filepath):
    if type(self.__chart) is heatmap.HeatMap:
      self.__chart.save(filepath)
    else:
      with open(filepath, "wb") as f:
        f.write(self.__chart.get_img_buff().getbuffer())
        print('Gift actually saved.', file=sys.stderr)
