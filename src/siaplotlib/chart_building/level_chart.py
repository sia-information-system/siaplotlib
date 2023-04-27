import sys
import numpy as np
import xarray as xr
from siaplotlib.charts import level_chart
from siaplotlib.charts import raw_image
from siaplotlib.processing import wrangling
from siaplotlib.processing import aggregation
from siaplotlib.processing import computations
from siaplotlib.chart_building.base_builder import ChartBuilder


class StaticWindRoseBuilder(ChartBuilder):
  # Public methods.
  def __init__(
    self, 
    dataset: xr.DataArray,
    eastward_var_name: str,
    northward_var_name: str,
    title: str,
    bin_min: float,
    bin_max: float,
    bin_jmp: float, 
    nsector: int,
    lon_dim_name: str,
    lat_dim_name: str,
    depth_dim_name: str,
    log_stream = sys.stderr,
    verbose: bool = False,
    dim_constraints: dict = {},
    color_palette: str = None
  ) -> None:
     super().__init__(
      dataset=dataset,
      log_stream=log_stream,
      verbose=verbose)
     self.eastward_var_name = eastward_var_name
     self.northward_var_name = northward_var_name
     self.lat_dim_name  = lat_dim_name 
     self.lon_dim_name = lon_dim_name
     self.depth_dim_name = depth_dim_name
     self. title = title
     self.bin_min = bin_min
     self.bin_max = bin_max
     self.bin_jmp = bin_jmp
     self.nsector = nsector
     self.dim_constraints = dim_constraints
     self.color_palette = color_palette
    
  def sync_build(self):
      
    subset = None
    if self.dim_constraints:
      subset = wrangling.slice_dice(
        dataset=self.dataset,
        dim_constraints=self.dim_constraints)
    else:
      subset = self.dataset
    
    lat_min = round(subset[self.lat_dim_name].values.min(),3)
    lat_max = round(subset[self.lat_dim_name].values.max(),3)

    lon_min = round(subset[self.lon_dim_name].values.min(),3)
    lon_max = round(subset[self.lon_dim_name].values.max(),3)

    depth = subset[self.depth_dim_name].values.max()
    depth = round(float(depth),3)

    title =  self.title + f'\n Depth: {depth} \n Lat: ({lat_min},{lat_max}), Lon: ({lon_min},{lon_max})'

    speed, direction = computations.calc_uniqueDir(
      dataset = subset,
      eastward_var_name = self.eastward_var_name,
      northward_var_name = self.northward_var_name)
    
  
    directionUp = computations.corr_cord(dataset = direction) 
    directionUp = wrangling.drop_nan(dataset = directionUp)
    speedUp = wrangling.drop_nan(dataset = speed)


    bin_range = computations.calc_bins(
      speed = speedUp,
      bin_min = self.bin_min,
      bin_max = self.bin_max,
      bin_jmp = self.bin_jmp,
    )
  
    self._chart = level_chart.WindRose(
      speed=speedUp,
      direction=directionUp,
      title=title,
      verbose=self.verbose,
      bin_range = bin_range,
      nsector = self.nsector,
      color_palette = self.color_palette)
    
    return self,subset

  
class StaticHeatMapBuilder(ChartBuilder):
  # Public methods.

  def __init__(
    self,
    dataset: xr.DataArray,
    lat_dim_name: str,
    lon_dim_name: str,
    title: str,
    dim_constraints: dict = {},
    var_name: str = None,
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
    subset = None
    if self.dim_constraints:
      subset = wrangling.slice_dice(
        dataset=self.dataset,
        dim_constraints=self.dim_constraints,
        var=self.var_name)
    elif self.var_name:
      subset = self.dataset[self.var_name]
    else:
      subset = self.dataset
    
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
    
    return self,subset
  
class AnimatedHeatMapBuilder(ChartBuilder):
  def __init__(
    self,
    dataset: xr.DataArray,
    lat_dim_name: str,
    lon_dim_name: str,
    time_dim_name: str,
    title: str,
    dim_constraints: dict = {},
    var_name: str = None,
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
    subset = None
    if self.dim_constraints:
      subset = wrangling.slice_dice(
        dataset=self.dataset,
        dim_constraints=self.dim_constraints,
        var=self.var_name)
    elif self.var_name:
      subset = self.dataset[self.var_name]
    else:
      subset = self.dataset
    
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
    
    return self,subset


class StaticContourMapBuilder(ChartBuilder):
  def __init__(self,
    dataset: xr.DataArray,
    lat_dim_name: str,
    lon_dim_name: str,
    num_levels: int,
    title: str,
    dim_constraints: dict = {},
    var_name: str = None,
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
    subset = None
    if self.dim_constraints:
      subset = wrangling.slice_dice(
        dataset=self.dataset,
        dim_constraints=self.dim_constraints,
        var=self.var_name)
    elif self.var_name:
      subset = self.dataset[self.var_name]
    else:
      subset = self.dataset
    
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
    
    return self,subset


class AnimatedContourMapBuilder(ChartBuilder):
  def __init__(
    self,
    dataset: xr.DataArray,
    lat_dim_name: str,
    lon_dim_name: str,
    time_dim_name: str,
    num_levels: int,
    title: str,
    dim_constraints: dict = {},
    var_name: str = None,
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
    subset = None
    if self.dim_constraints:
      subset = wrangling.slice_dice(
        dataset=self.dataset,
        dim_constraints=self.dim_constraints,
        var=self.var_name)
    elif self.var_name:
      subset = self.dataset[self.var_name]
    else:
      subset = self.dataset
    
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
    
    return self,subset


class StaticVerticalSliceBuilder(ChartBuilder):
  # Public methods.

  def __init__(
    self,
    dataset: xr.DataArray,
    x_dim_name: str,
    y_dim_name: str,
    lat_dim_name: str,
    lon_dim_name: str,
    title: str,
    var_label: str,
    y_label: str,
    x_label: str,
    dim_constraints: dict = {},
    var_name: str = None,
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
    subset = None
    if self.dim_constraints:
      subset = wrangling.slice_dice(
        dataset=self.dataset,
        dim_constraints=self.dim_constraints,
        var=self.var_name)
    elif self.var_name:
      subset = self.dataset[self.var_name]
    else:
      subset = self.dataset
    
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
    
    return self,subset
  

class AnimatedVerticalSliceBuilder(ChartBuilder):
  def __init__(
    self,
    dataset: xr.DataArray,
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
    var_name: str = None,
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
    subset = None
    if self.dim_constraints:
      subset = wrangling.slice_dice(
        dataset=self.dataset,
        dim_constraints=self.dim_constraints,
        var=self.var_name)
    elif self.var_name:
      subset = self.dataset[self.var_name]
    else:
      subset = self.dataset
    
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
    
    return self,subset
