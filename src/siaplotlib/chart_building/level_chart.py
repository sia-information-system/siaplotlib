import sys
import numpy as np
import xarray as xr
from siaplotlib.charts import level_chart
from siaplotlib.charts import raw_image
from siaplotlib.processing import wrangling
from siaplotlib.processing import aggregation
from siaplotlib.chart_building import base_builder


class StaticHeatMapBuilder(base_builder.ChartBuilder):
  # Public methods.

  def __init__(
    self,
    dataset: xr.DataArray,
    var_name: str,
    lat_dim_name: str,
    lon_dim_name: str,
    title: str,
    dim_constraints: dict = {},
    var_label: str = None,
    color_palette: str = None,
    log_stream = sys.stderr,
    verbose: bool = False
  ) -> None:
    super().__init__(
      dataset=dataset,
      log_stream=log_stream,
      verbose=verbose)
    self.var_name = var_name
    self.lat_dim_name = lat_dim_name
    self.lon_dim_name = lon_dim_name
    self.title = title
    self.dim_constraints = dim_constraints
    self.var_label = var_label
    self.color_palette = color_palette


  def sync_build(self):
    subset = wrangling.slice_dice(
      dataset=self.dataset,
      dim_constraints=self.dim_constraints,
      var=self.var_name)
    
    vmin = aggregation.min(
      dataset=subset,
      rounding_precision=3)
    
    vmax = aggregation.max(
      dataset=subset,
      rounding_precision=3)
    
    lon_data, lat_data, lon_interval, lat_interval = wrangling.get_coords(
      dataset=subset,
      lon_dim_name=self.lon_dim_name,
      lat_dim_name=self.lat_dim_name)
    
    self._chart = level_chart.HeatMap(
      data=subset.data,
      data_label=self.var_label,
      title=self.title,
      lon_interval=lon_interval,
      lat_interval=lat_interval,
      lat_data=lat_data,
      lon_data=lon_data,
      vmax=vmax,
      vmin=vmin,
      color_palette=self.color_palette,
      log_stream=self.log_stream,
      verbose=self.verbose)
    
    return self


class AnimatedHeatMapBuilder(base_builder.ChartBuilder):
  def __init__(
    self,
    dataset: xr.DataArray,
    var_name: str,
    lat_dim_name: str,
    lon_dim_name: str,
    time_dim_name: str,
    title: str,
    dim_constraints: dict = {},
    var_label: str = None,
    color_palette: str = None,
    duration: int = 0.5,
    duration_unit: str = 'SECONDS_PER_FRAME',
    log_stream = sys.stderr,
    verbose: bool = False
  ) -> None:
    super().__init__(dataset=dataset, verbose=verbose, log_stream=log_stream)
    self.var_name = var_name
    self.lat_dim_name = lat_dim_name
    self.lon_dim_name = lon_dim_name
    self.time_dim_name = time_dim_name
    self.title = title
    self.dim_constraints = dim_constraints
    self.var_label = var_label
    self.color_palette = color_palette
    self.duration = duration
    self.duration_unit = duration_unit


  def sync_build(self):
    subset = wrangling.slice_dice(
      dataset=self.dataset,
      dim_constraints=self.dim_constraints,
      var=self.var_name)
    
    vmin = aggregation.min(
      dataset=subset,
      rounding_precision=3)
    
    vmax = aggregation.max(
      dataset=subset,
      rounding_precision=3)
    
    lon_data, lat_data, lon_interval, lat_interval = wrangling.get_coords(
      dataset=subset,
      lon_dim_name=self.lon_dim_name,
      lat_dim_name=self.lat_dim_name)

    self.log('Creating images (frames) to create gif.')
    
    chart_list = []
    for  i in range(len(subset[self.time_dim_name])):
      time_constraint = {}
      time_constraint[self.time_dim_name] = [i]
      date_subset = subset.isel(time_constraint).squeeze()
      date = np.datetime_as_string(date_subset[self.time_dim_name].data, unit='D')

      chart = level_chart.HeatMap(
        data=date_subset.data,
        data_label=self.var_label,
        title=f'{self.title} {date}',
        lon_interval=lon_interval,
        lat_interval=lat_interval,
        lat_data=lat_data,
        lon_data=lon_data,
        vmax=vmax,
        vmin=vmin,
        color_palette=self.color_palette,
        log_stream=self.log_stream,
        verbose=self.verbose)
      
      chart_list.append(chart)
    
    img_buff = self._make_gif(
      chart_list,
      duration=self.duration,
      duration_unit=self.duration_unit)
    
    self.log('Closing intermediate figures')
    for chart in chart_list:
      chart.close()

    self._chart = raw_image.ChartImage(
      img_source=img_buff,
      var_name=self.var_name, 
      title=self.title, 
      lon_interval=lon_interval, 
      lat_interval=lat_interval,
      var_label=self.var_label,
      log_stream=self.log_stream,
      verbose=self.verbose)
    
    return self

# TODO: Test the static of this, use the log method and make the Animated class
class StaticContourMapBuilder(base_builder.ChartBuilder):
  def __init__(self,
    dataset: xr.DataArray,
    var_name: str,
    lat_dim_name: str,
    lon_dim_name: str,
    num_levels: int,
    title: str,
    dim_constraints: dict = {},
    var_label: str = None,
    color_palette: str = None,
    log_stream = sys.stderr,
    verbose: bool = False
  ) -> None:
    super().__init__(dataset=dataset, verbose=verbose, log_stream=log_stream)
    self.var_name = var_name
    self.lat_dim_name = lat_dim_name
    self.lon_dim_name = lon_dim_name
    self.num_levels = num_levels
    self.title = title
    self.dim_constraints = dim_constraints
    self.var_label = var_label
    self.color_palette = color_palette

  
  def sync_build(self):
    subset = wrangling.slice_dice(
      dataset=self.dataset,
      dim_constraints=self.dim_constraints,
      var=self.var_name)
    
    vmin = aggregation.min(
      dataset=subset,
      rounding_precision=3)
    
    vmax = aggregation.max(
      dataset=subset,
      rounding_precision=3)
    
    lon_data, lat_data, lon_interval, lat_interval = wrangling.get_coords(
      dataset=subset,
      lon_dim_name=self.lon_dim_name,
      lat_dim_name=self.lat_dim_name)
    
    self._chart = level_chart.ContourMap(
      data=subset.data,
      data_label=self.var_label,
      title=self.title,
      lon_interval=lon_interval,
      lat_interval=lat_interval,
      lat_data=lat_data,
      lon_data=lon_data,
      vmax=vmax,
      vmin=vmin,
      num_levels=self.num_levels,
      color_palette=self.color_palette,
      log_stream=self.log_stream,
      verbose=self.verbose)
    
    return self


class AnimatedContourMapBuilder(base_builder.ChartBuilder):
  def __init__(
    self,
    dataset: xr.DataArray,
    var_name: str,
    lat_dim_name: str,
    lon_dim_name: str,
    time_dim_name: str,
    num_levels: int,
    title: str,
    dim_constraints: dict = {},
    var_label: str = None,
    color_palette: str = None,
    duration: int = 0.5,
    duration_unit: str = 'SECONDS_PER_FRAME',
    log_stream=sys.stderr,
    verbose: bool = False
  ) -> None:
    super().__init__(dataset=dataset, log_stream=log_stream, verbose=verbose)
    self.var_name = var_name
    self.lat_dim_name = lat_dim_name
    self.lon_dim_name = lon_dim_name
    self.time_dim_name = time_dim_name
    self.num_levels = num_levels
    self.title = title
    self.dim_constraints = dim_constraints
    self.var_label = var_label
    self.color_palette = color_palette
    self.duration = duration
    self.duration_unit = duration_unit
  
  
  def sync_build(self):
    subset = wrangling.slice_dice(
      dataset=self.dataset,
      dim_constraints=self.dim_constraints,
      var=self.var_name)
    
    vmin = aggregation.min(
      dataset=subset,
      rounding_precision=3)
    
    vmax = aggregation.max(
      dataset=subset,
      rounding_precision=3)
    
    lon_data, lat_data, lon_interval, lat_interval = wrangling.get_coords(
      dataset=subset,
      lon_dim_name=self.lon_dim_name,
      lat_dim_name=self.lat_dim_name)

    self.log('Creating images (frames) to create gif.')
    
    chart_list = []
    for  i in range(len(subset[self.time_dim_name])):
      time_constraint = {}
      time_constraint[self.time_dim_name] = [i]
      date_subset = subset.isel(time_constraint).squeeze()
      date = np.datetime_as_string(date_subset[self.time_dim_name].data, unit='D')

      chart = level_chart.ContourMap(
        data=date_subset.data,
        data_label=self.var_label,
        title=f'{self.title} {date}',
        lon_interval=lon_interval,
        lat_interval=lat_interval,
        lat_data=lat_data,
        lon_data=lon_data,
        vmax=vmax,
        vmin=vmin,
        color_palette=self.color_palette,
        num_levels=self.num_levels,
        log_stream=self.log_stream,
        verbose=self.verbose)
      
      chart_list.append(chart)
    
    img_buff = self._make_gif(
      chart_list,
      duration=self.duration,
      duration_unit=self.duration_unit)
    
    self.log('Closing intermediate figures.')
    for chart in chart_list:
      chart.close()

    self._chart = raw_image.ChartImage(
      img_source=img_buff,
      var_name=self.var_name, 
      title=self.title, 
      lon_interval=lon_interval, 
      lat_interval=lat_interval,
      var_label=self.var_label,
      log_stream=self.log_stream,
      verbose=self.verbose)
    
    return self


class StaticVerticalSliceBuilder(base_builder.ChartBuilder):
  # Public methods.

  def __init__(
    self,
    dataset: xr.DataArray,
    var_name: str,
    x_dim_name: str,
    y_dim_name: str,
    lat_dim_name: str,
    lon_dim_name: str,
    title: str,
    var_label: str,
    y_label: str,
    x_label: str,
    dim_constraints: dict = {},
    color_palette: str = None,
    log_stream = sys.stderr,
    verbose: bool = False
  ) -> None:
    super().__init__(
      dataset=dataset,
      log_stream=log_stream,
      verbose=verbose)
    self.var_name = var_name
    self.x_dim_name = x_dim_name
    self.y_dim_name = y_dim_name
    self.lat_dim_name = lat_dim_name
    self.lon_dim_name = lon_dim_name
    self.title = title
    self.var_label = var_label
    self.y_label = y_label
    self.x_label = x_label
    self.dim_constraints = dim_constraints
    self.color_palette = color_palette


  def sync_build(self):
    subset = wrangling.slice_dice(
      dataset=self.dataset,
      dim_constraints=self.dim_constraints,
      var=self.var_name)
    
    vmin = aggregation.min(
      dataset=subset,
      rounding_precision=3)
    
    vmax = aggregation.max(
      dataset=subset,
      rounding_precision=3)
    
    lon_data, lat_data, lon_interval, lat_interval = wrangling.get_coords(
      dataset=subset,
      lon_dim_name=self.lon_dim_name,
      lat_dim_name=self.lat_dim_name)
    
    self.log(f'vmin: {vmin}')
    self.log(f'vmax: {vmax}')
    self.log(f'lon_interval: {lon_interval}')
    self.log(f'lat_interval: {lat_interval}')
    
    y_values = subset[self.y_dim_name].data
    x_values = None
    if self.x_dim_name == self.lon_dim_name:
      x_values = lon_data
      self.log(f'Using lon dim as X values')
    elif self.x_dim_name == self.lat_dim_name:
      x_values = lat_data
      self.log(f'Using lat dim as X values')
    else:
      x_values = subset[self.x_dim_name].data
      self.log(f'Using {self.x_dim_name} dim as X values')
    
    self._chart = level_chart.VerticalSlice(
      x_values=x_values,
      y_values=y_values,
      z_values=subset.data,
      vmin=vmin,
      vmax=vmax,
      lon_interval=lon_interval,
      lat_interval=lat_interval,
      title=self.title,
      z_label=self.var_label,
      y_label=self.y_label,
      x_label=self.x_label,
      color_palette=self.color_palette,
      log_stream=self.log_stream,
      verbose=self.verbose
    )
    
    return self
  

class AnimatedVerticalSliceBuilder(base_builder.ChartBuilder):
  def __init__(
    self,
    dataset: xr.DataArray,
    var_name: str,
    x_dim_name: str,
    y_dim_name: str,
    time_dim_name: str,
    lat_dim_name: str,
    lon_dim_name: str,
    title: str,
    var_label: str,
    y_label: str,
    x_label: str,
    dim_constraints: dict = {},
    color_palette: str = None,
    duration: int = 0.5,
    duration_unit: str = 'SECONDS_PER_FRAME',
    log_stream=sys.stderr,
    verbose: bool = False
  ) -> None:
    super().__init__(dataset=dataset, log_stream=log_stream, verbose=verbose)
    self.var_name = var_name
    self.x_dim_name = x_dim_name
    self.y_dim_name = y_dim_name
    self.time_dim_name = time_dim_name
    self.lat_dim_name = lat_dim_name
    self.lon_dim_name = lon_dim_name
    self.title = title
    self.var_label = var_label
    self.y_label = y_label
    self.x_label = x_label
    self.dim_constraints = dim_constraints
    self.color_palette = color_palette
    self.duration = duration
    self.duration_unit = duration_unit


  def sync_build(self):
    subset = wrangling.slice_dice(
      dataset=self.dataset,
      dim_constraints=self.dim_constraints,
      var=self.var_name)
    
    vmin = aggregation.min(
      dataset=subset,
      rounding_precision=3)
    
    vmax = aggregation.max(
      dataset=subset,
      rounding_precision=3)
    
    lon_data, lat_data, lon_interval, lat_interval = wrangling.get_coords(
      dataset=subset,
      lon_dim_name=self.lon_dim_name,
      lat_dim_name=self.lat_dim_name)
    
    self.log(f'vmin: {vmin}')
    self.log(f'vmax: {vmax}')
    self.log(f'lon_interval: {lon_interval}')
    self.log(f'lat_interval: {lat_interval}')
    
    x_values = None
    if self.x_dim_name == self.lon_dim_name:
      x_values = lon_data
      self.log(f'Using lon dim as X values')
    elif self.x_dim_name == self.lat_dim_name:
      x_values = lat_data
      self.log(f'Using lat dim as X values')
    else:
      x_values = subset[self.x_dim_name].data
      self.log(f'Using {self.x_dim_name} dim as X values')

    self.log('Creating images (frames) to create gif.')
    
    chart_list = []
    for date in subset[self.time_dim_name]:
      date_subset = subset.sel({
        self.time_dim_name: date.data
      }).squeeze()
      date = np.datetime_as_string(date.data, unit='D')
      chart = level_chart.VerticalSlice(
        x_values=x_values,
        y_values=date_subset[self.y_dim_name].data,
        z_values=date_subset.data,
        vmin=vmin,
        vmax=vmax,
        lon_interval=lon_interval,
        lat_interval=lat_interval,
        title=f'{self.title} - {date}',
        z_label=self.var_label,
        y_label=self.y_label,
        x_label=self.x_label,
        color_palette=self.color_palette,
        log_stream=self.log_stream,
        verbose=self.verbose
      )
      
      chart_list.append(chart)
    
    img_buff = self._make_gif(
      chart_list,
      duration=self.duration,
      duration_unit=self.duration_unit)
    
    self.log('Closing intermediate figures.')
    for chart in chart_list:
      chart.close()

    self._chart = raw_image.ChartImage(
      img_source=img_buff,
      var_name=self.var_name, 
      title=self.title, 
      lon_interval=lon_interval, 
      lat_interval=lat_interval,
      var_label=self.var_label,
      log_stream=self.log_stream,
      verbose=self.verbose)
    
    return self
