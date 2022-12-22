from omdepplotlib.chart_building import base_builder
from omdepplotlib.preprocessing import munging
from omdepplotlib.charts import line_chart
import xarray as xr
import sys


class SinglePointTimeSeriesBuilder(base_builder.ChartBuilder):
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
    time_dim_name: str,
    grouping_dim_name: str,
    title: str,
    grouping_dim_label: str,
    y_label: str,
    x_label: str = None,
    dim_constraints: dict[str, list] = {},
  ):
    subset = munging.slice_dice(
      dataset=self.dataset,
      dim_constraints=dim_constraints,
      var=var)
    
    lon_data, lat_data, lon_interval, lat_interval = munging.get_coords(
      dataset=subset,
      lon_dim_name=lon_dim_name,
      lat_dim_name=lat_dim_name)
    
    if self.verbose:
      print('Getting groups.', file=sys.stderr)
    show_series_names = True
    if grouping_dim_name is None:
      show_series_names = False
    
    series_list = munging.group_into_series(
      dataset=subset,
      x_dim_name=time_dim_name,
      grouping_dim_name=grouping_dim_name)

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
      title=title,
      grouping_var_label=grouping_dim_label,
      y_label=y_label,
      x_label=x_label,
      show_series_names=show_series_names,
      verbose=self.verbose)
    
    return self


class SinglePointVerticalProfileBuilder(base_builder.ChartBuilder):
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
    y_dim_name: str,
    grouping_dim_name: str,
    title: str,
    grouping_dim_label: str,
    y_label: str,
    x_label: str = None,
    dim_constraints: dict[str, list] = {},
  ):
    subset = munging.slice_dice(
      dataset=self.dataset,
      dim_constraints=dim_constraints,
      var=var)
    
    lon_data, lat_data, lon_interval, lat_interval = munging.get_coords(
      dataset=subset,
      lon_dim_name=lon_dim_name,
      lat_dim_name=lat_dim_name)
    
    show_series_names = True
    if grouping_dim_name is None:
      show_series_names = False
    
    series_list = munging.group_into_series(
      dataset=subset,
      x_dim_name=y_dim_name,
      grouping_dim_name=grouping_dim_name,
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
      title=title,
      grouping_var_label=grouping_dim_label,
      y_label=y_label,
      x_label=x_label,
      show_series_names=show_series_names,
      verbose=self.verbose)
    
    return self
