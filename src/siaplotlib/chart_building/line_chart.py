# Standard
import sys
# Third party
import xarray as xr
# Own
from siaplotlib.chart_building.base_builder import ChartBuilder
from siaplotlib.processing import wrangling
from siaplotlib.charts import line_chart
from siaplotlib.processing import computations


class StaticArrowChartBuilder(ChartBuilder):
  # Public methods.
  def __init__(
    self, 
    dataset: xr.DataArray,
    eastward_var_name: str,
    northward_var_name: str,
    grouping_level,
    title: str,
    var_label: str,
    time_dim_name: str,
    lon_dim_name: str,
    lat_dim_name: str,
    depth_dim_name: str,
    dim_constraints: dict = {},
    log_stream = sys.stderr,
    verbose: bool = False
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
     self.title = title
     self.time_dim_name = time_dim_name
     self.grouping_level = grouping_level
     self.dim_constraints = dim_constraints
     self.var_label = var_label
    
  def sync_build(self):
      
      subset = wrangling.slice_dice(
        dataset=self.dataset,
        dim_constraints=self.dim_constraints)
      
      speed = computations.calc_spd(
        dataset=subset,
        eastward_var_name= self.eastward_var_name,
        northward_var_name= self.northward_var_name)
      
      dp_nm = self.depth_dim_name
      depth = subset[dp_nm].values.max()
      depth = round(float(depth),3)

      tm_nm = self.time_dim_name
      date = subset[tm_nm].values
      date = date.astype('datetime64[D]')

      title =  self.title + f'\n Depth: {depth} \n Date: {date}'

      self._chart = line_chart.ArrowChart(
        dataset=subset,
        speed=speed,
        title=title,
        data_label=self.var_label,
        eastward_var_name=self.eastward_var_name,
        northward_var_name=self.northward_var_name,
        lat_dim_name=self.lat_dim_name,
        lon_dim_name=self.lon_dim_name,
        grouping_level=self.grouping_level,
        verbose=self.verbose)
      
      return self,subset


class StaticRegionMapBuilder(ChartBuilder):
  # Public methods.

  def __init__(
    self,
    amplitude: float,
    lon_dim_min: float,
    lon_dim_max: float,
    lat_dim_min: float,
    lat_dim_max: float,
    log_stream = sys.stderr,
    verbose: bool = False
  ) -> None:
    super().__init__(
      dataset=None,
      log_stream=log_stream,
      verbose=verbose)
    self.amplitude = amplitude
    self.lon_dim_min = lon_dim_min
    self.lon_dim_max = lon_dim_max
    self.lat_dim_min = lat_dim_min
    self.lat_dim_max = lat_dim_max

  def sync_build(self):
      self._chart = line_chart.RegionMap(
        amplitude = self.amplitude,
        lon_dim_min = self.lon_dim_min,
        lon_dim_max = self.lon_dim_max,
        lat_dim_min = self.lat_dim_min,
        lat_dim_max = self.lat_dim_max)

      return self


class SinglePointTimeSeriesBuilder(ChartBuilder):
  # Public methods.

  def __init__(
    self,
    dataset: xr.DataArray,
    var_name: str,
    lat_dim_name: str,
    lon_dim_name: str,
    time_dim_name: str,
    grouping_dim_name: str,
    title: str,
    grouping_dim_label: str,
    var_label: str,
    time_dim_label: str = None,
    dim_constraints: dict[str, list] = {},
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
    self.time_dim_name = time_dim_name
    self.grouping_dim_name = grouping_dim_name
    self.title = title
    self.grouping_dim_label = grouping_dim_label
    self.var_label = var_label
    self.time_dim_label = time_dim_label
    self.dim_constraints = dim_constraints


  def sync_build(self):
    subset = wrangling.slice_dice(
      dataset=self.dataset,
      dim_constraints=self.dim_constraints,
      var=self.var_name)
    
    lon_data, lat_data, lon_interval, lat_interval = wrangling.get_coords(
      dataset=subset,
      lon_dim_name=self.lon_dim_name,
      lat_dim_name=self.lat_dim_name)
    
    self.log('Getting groups.')
    show_series_names = True
    if self.grouping_dim_name is None:
      show_series_names = False
    
    series_list = wrangling.group_into_series(
      dataset=subset,
      x_dim_name=self.time_dim_name,
      grouping_dim_name=self.grouping_dim_name)

    lon_interval[0] -= 3
    lon_interval[1] += 3
    lat_interval[0] -= 3
    lat_interval[1] += 3
    self._chart = line_chart.SinglePointTimeSeries(
      series_data=series_list,
      lon=float(lon_data),
      lat=float(lat_data),
      lon_interval=lon_interval,
      lat_interval=lat_interval,
      title=self.title,
      grouping_var_label=self.grouping_dim_label,
      y_label=self.var_label,
      x_label=self.time_dim_label,
      show_series_names=show_series_names,
      log_stream=self.log_stream,
      verbose=self.verbose)
    
    return self, subset


class SinglePointVerticalProfileBuilder(ChartBuilder):
  # Public methods.

  def __init__(
    self,
    dataset: xr.DataArray,
    var_name: str,
    lat_dim_name: str,
    lon_dim_name: str,
    y_dim_name: str,
    grouping_dim_name: str,
    title: str,
    grouping_dim_label: str,
    y_dim_label: str,
    var_label: str = None,
    dim_constraints: dict[str, list] = {},
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
    self.y_dim_name = y_dim_name
    self.grouping_dim_name = grouping_dim_name
    self.title = title
    self.grouping_dim_label = grouping_dim_label
    self.y_dim_label = y_dim_label
    self.var_label = var_label
    self.dim_constraints = dim_constraints


  def sync_build(self):
    subset = wrangling.slice_dice(
      dataset=self.dataset,
      dim_constraints=self.dim_constraints,
      var=self.var_name)
    
    lon_data, lat_data, lon_interval, lat_interval = wrangling.get_coords(
      dataset=subset,
      lon_dim_name=self.lon_dim_name,
      lat_dim_name=self.lat_dim_name)
    
    show_series_names = True
    if self.grouping_dim_name is None:
      show_series_names = False
    
    series_list = wrangling.group_into_series(
      dataset=subset,
      x_dim_name=self.y_dim_name,
      grouping_dim_name=self.grouping_dim_name,
      reverse_axis=True)

    lon_interval[0] -= 3
    lon_interval[1] += 3
    lat_interval[0] -= 3
    lat_interval[1] += 3
    self._chart = line_chart.SinglePointVerticalProfile(
      series_data=series_list,
      lon=float(lon_data),
      lat=float(lat_data),
      lon_interval=lon_interval,
      lat_interval=lat_interval,
      title=self.title,
      grouping_var_label=self.grouping_dim_label,
      y_label=self.y_dim_label,
      x_label=self.var_label,
      show_series_names=show_series_names,
      log_stream=self.log_stream,
      verbose=self.verbose)
    
    return self, subset
