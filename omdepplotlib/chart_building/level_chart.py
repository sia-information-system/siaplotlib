import sys
import numpy as np
import xarray as xr
from omdepplotlib.charts import level_chart
from omdepplotlib.charts import raw_image
from omdepplotlib.preprocessing import munging
from omdepplotlib.preprocessing import aggregation
from omdepplotlib.chart_building import base_builder


class HeatMapBuilder(base_builder.ChartBuilder):
  # Public methods.

  def __init__(
    self,
    dataset: xr.DataArray,
    verbose: bool = False
  ) -> None:
    super().__init__(
      dataset=dataset,
      verbose=verbose)


  def build_static(
    self, 
    var: str,
    lat_dim_name: str,
    lon_dim_name: str,
    title: str,
    dim_constraints: dict = {},
    label: str = None,
    color_palette: str = None
  ):
    subset = munging.slice_dice(
      dataset=self.dataset,
      dim_constraints=dim_constraints,
      var=var)
    
    vmin = aggregation.min(
      dataset=subset,
      rounding_precision=3)
    
    vmax = aggregation.max(
      dataset=subset,
      rounding_precision=3)
    
    lon_data, lat_data, lon_interval, lat_interval = munging.get_coords(
      dataset=subset,
      lon_dim_name=lon_dim_name,
      lat_dim_name=lat_dim_name)
    
    self._chart = level_chart.HeatMap(
      dataset=subset,
      label=label,
      title=title,
      lon_interval=lon_interval,
      lat_interval=lat_interval,
      lat_data=lat_data,
      lon_data=lon_data,
      vmax=vmax,
      vmin=vmin,
      color_palette=color_palette,
      verbose=self.verbose)
    
    return self


  def build_animation(
    self,
    var: str,
    lat_dim_name: str,
    lon_dim_name: str,
    time_dim_name: str,
    title: str,
    dim_constraints: dict = {},
    label: str = None,
    color_palette: str = None,
    duration: int = 0.5,
    duration_unit: str = 'SECONDS_PER_FRAME'
  ):
    subset = munging.slice_dice(
      dataset=self.dataset,
      dim_constraints=dim_constraints,
      var=var)
    
    vmin = aggregation.min(
      dataset=subset,
      rounding_precision=3)
    
    vmax = aggregation.max(
      dataset=subset,
      rounding_precision=3)
    
    lon_data, lat_data, lon_interval, lat_interval = munging.get_coords(
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

      chart = level_chart.HeatMap(
        dataset=date_subset,
        label=label,
        title=f'{title} {date}',
        lon_interval=lon_interval,
        lat_interval=lat_interval,
        lat_data=lat_data,
        lon_data=lon_data,
        vmax=vmax,
        vmin=vmin,
        color_palette=color_palette,
        verbose=self.verbose)
      
      chart_list.append(chart)
    
    img_buff = self._make_gif(
      chart_list,
      duration=duration,
      duration_unit=duration_unit)
    
    if self.verbose:
      print('Closing intermediate figures', file=sys.stderr)
    for chart in chart_list:
      chart.close()

    self._chart = raw_image.ChartImage(
      img_source=img_buff,
      var=var, 
      title=title, 
      lon_interval=lon_interval, 
      lat_interval=lat_interval,
      label=label)
    
    return self


class ContourMapBuilder(base_builder.ChartBuilder):
  def __init__(self,
    dataset: xr.DataArray,
    verbose: bool = False
  ) -> None:
    self.dataset = dataset
    self._chart = None
    self.verbose = verbose

  
  def build_static(
    self,
    var: str,
    lat_dim_name: str,
    lon_dim_name: str,
    num_levels: int,
    title: str,
    dim_constraints: dict = {},
    label: str = None,
    color_palette: str = None
  ):
    subset = munging.slice_dice(
      dataset=self.dataset,
      dim_constraints=dim_constraints,
      var=var)
    
    vmin = aggregation.min(
      dataset=subset,
      rounding_precision=3)
    
    vmax = aggregation.max(
      dataset=subset,
      rounding_precision=3)
    
    lon_data, lat_data, lon_interval, lat_interval = munging.get_coords(
      dataset=subset,
      lon_dim_name=lon_dim_name,
      lat_dim_name=lat_dim_name)
    
    self._chart = level_chart.ContourMap(
      dataset=subset,
      label=label,
      title=title,
      lon_interval=lon_interval,
      lat_interval=lat_interval,
      lat_data=lat_data,
      lon_data=lon_data,
      vmax=vmax,
      vmin=vmin,
      num_levels=num_levels,
      color_palette=color_palette,
      verbose=self.verbose)
    
    return self


  def build_animation(
    self,
    var: str,
    lat_dim_name: str,
    lon_dim_name: str,
    time_dim_name: str,
    num_levels: int,
    title: str,
    dim_constraints: dict = {},
    label: str = None,
    color_palette: str = None,
    duration: int = 0.5,
    duration_unit: str = 'SECONDS_PER_FRAME'
  ):
    subset = munging.slice_dice(
      dataset=self.dataset,
      dim_constraints=dim_constraints,
      var=var)
    
    vmin = aggregation.min(
      dataset=subset,
      rounding_precision=3)
    
    vmax = aggregation.max(
      dataset=subset,
      rounding_precision=3)
    
    lon_data, lat_data, lon_interval, lat_interval = munging.get_coords(
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

      chart = level_chart.ContourMap(
        dataset=date_subset,
        label=label,
        title=f'{title} {date}',
        lon_interval=lon_interval,
        lat_interval=lat_interval,
        lat_data=lat_data,
        lon_data=lon_data,
        vmax=vmax,
        vmin=vmin,
        color_palette=color_palette,
        num_levels=num_levels,
        verbose=self.verbose)
      
      chart_list.append(chart)
    
    img_buff = self._make_gif(
      chart_list,
      duration=duration,
      duration_unit=duration_unit)
    
    if self.verbose:
      print('Closing intermediate figures', file=sys.stderr)
    for chart in chart_list:
      chart.close()

    self._chart = raw_image.ChartImage(
      img_source=img_buff,
      var=var, 
      title=title, 
      lon_interval=lon_interval, 
      lat_interval=lat_interval,
      label=label,
      verbose=self.verbose)
    
    return self


class VerticalSliceBuilder(base_builder.ChartBuilder):
  # Public methods.

  def __init__(
    self,
    dataset: xr.DataArray,
    verbose: bool = False
  ) -> None:
    super().__init__(
      dataset=dataset,
      verbose=verbose)


  def build_static(
    self, 
    var: str,
    x_dim_name: str,
    y_dim_name: str,
    lat_dim_name: str,
    lon_dim_name: str,
    title: str,
    measure_label: str,
    y_label: str,
    x_label: str,
    dim_constraints: dict = {},
    color_palette: str = None
  ):
    subset = munging.slice_dice(
      dataset=self.dataset,
      dim_constraints=dim_constraints,
      var=var)
    
    vmin = aggregation.min(
      dataset=subset,
      rounding_precision=3)
    
    vmax = aggregation.max(
      dataset=subset,
      rounding_precision=3)
    
    lon_data, lat_data, lon_interval, lat_interval = munging.get_coords(
      dataset=subset,
      lon_dim_name=lon_dim_name,
      lat_dim_name=lat_dim_name)
    
    if self.verbose:
      print(f'vmin: {vmin}', file=sys.stderr)
      print(f'vmax: {vmax}', file=sys.stderr)
      print(f'lon_interval: {lon_interval}', file=sys.stderr)
      print(f'lat_interval: {lat_interval}', file=sys.stderr)
    
    y_values = subset[y_dim_name].data
    x_values = None
    if x_dim_name == lon_dim_name:
      x_values = lon_data
      if self.verbose:
        print(f'Using lon dim as X values', file=sys.stderr)
    elif x_dim_name == lat_dim_name:
      x_values = lat_data
      if self.verbose:
        print(f'Using lat dim as X values', file=sys.stderr)
    else:
      x_values = subset[x_dim_name].data
      if self.verbose:
        print(f'Using {x_dim_name} dim as X values', file=sys.stderr)
    
    self._chart = level_chart.VerticalSlice(
      x_values=x_values,
      y_values=y_values,
      z_values=subset.data,
      vmin=vmin,
      vmax=vmax,
      lon_interval=lon_interval,
      lat_interval=lat_interval,
      title=title,
      measure_label=measure_label,
      y_label=y_label,
      x_label=x_label,
      color_palette=color_palette
    )
    
    return self
  

  def build_animation(
    self,
    var: str,
    x_dim_name: str,
    y_dim_name: str,
    time_dim_name: str,
    lat_dim_name: str,
    lon_dim_name: str,
    title: str,
    measure_label: str,
    y_label: str,
    x_label: str,
    dim_constraints: dict = {},
    color_palette: str = None,
    duration: int = 0.5,
    duration_unit: str = 'SECONDS_PER_FRAME'
  ):
    subset = munging.slice_dice(
      dataset=self.dataset,
      dim_constraints=dim_constraints,
      var=var)
    
    vmin = aggregation.min(
      dataset=subset,
      rounding_precision=3)
    
    vmax = aggregation.max(
      dataset=subset,
      rounding_precision=3)
    
    lon_data, lat_data, lon_interval, lat_interval = munging.get_coords(
      dataset=subset,
      lon_dim_name=lon_dim_name,
      lat_dim_name=lat_dim_name)
    
    if self.verbose:
      print(f'vmin: {vmin}', file=sys.stderr)
      print(f'vmax: {vmax}', file=sys.stderr)
      print(f'lon_interval: {lon_interval}', file=sys.stderr)
      print(f'lat_interval: {lat_interval}', file=sys.stderr)
    
    x_values = None
    if x_dim_name == lon_dim_name:
      x_values = lon_data
      if self.verbose:
        print(f'Using lon dim as X values', file=sys.stderr)
    elif x_dim_name == lat_dim_name:
      x_values = lat_data
      if self.verbose:
        print(f'Using lat dim as X values', file=sys.stderr)
    else:
      x_values = subset[x_dim_name].data
      if self.verbose:
        print(f'Using {x_dim_name} dim as X values', file=sys.stderr)

    if self.verbose:
      print('Creating images (frames) to create gif.', file=sys.stderr)
    
    chart_list = []
    for date in subset[time_dim_name]:
      date_subset = subset.sel({
        time_dim_name: date.data
      }).squeeze()
      date = np.datetime_as_string(date.data, unit='D')
      chart = level_chart.VerticalSlice(
        x_values=x_values,
        y_values=date_subset[y_dim_name].data,
        z_values=date_subset.data,
        vmin=vmin,
        vmax=vmax,
        lon_interval=lon_interval,
        lat_interval=lat_interval,
        title=f'{title} - {date}',
        measure_label=measure_label,
        y_label=y_label,
        x_label=x_label,
        color_palette=color_palette
      )
      
      chart_list.append(chart)
    
    img_buff = self._make_gif(
      chart_list,
      duration=duration,
      duration_unit=duration_unit)
    
    if self.verbose:
      print('Closing intermediate figures', file=sys.stderr)
    for chart in chart_list:
      chart.close()

    self._chart = raw_image.ChartImage(
      img_source=img_buff,
      var=var, 
      title=title, 
      lon_interval=lon_interval, 
      lat_interval=lat_interval,
      label=measure_label,
      verbose=self.verbose)
    
    return self