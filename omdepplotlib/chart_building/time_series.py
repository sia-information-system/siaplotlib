from omdepplotlib.chart_building import base_builder
from omdepplotlib.preprocessing import subsetting
from omdepplotlib.charts import time_series
import xarray as xr
import numpy as np
import pandas as pd
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
    subset, _, _ = subsetting.slice_dice(
      dataset=self.dataset,
      dim_constraints=dim_constraints,
      var=var)
    
    lon_data, lat_data, lon_interval, lat_interval = subsetting.get_coords(
      dataset=subset,
      lon_dim_name=lon_dim_name,
      lat_dim_name=lat_dim_name)
    
    if self.verbose:
      print('Getting groups.', file=sys.stderr)
    show_series_names = True
    groups = None
    if grouping_dim_name is not None:
      groups = subset[grouping_dim_name].data
    else:
      if self.verbose:
        print('No grouped. Series labels will not be displayed.', file=sys.stderr)
      groups = np.array(None)
      show_series_names = False
    series_list = []
    series_names = []

    if self.verbose:
      print('Evaluating how many series to create.', file=sys.stderr)
    if len(groups.shape) == 0:
      if self.verbose:
        print('Creating a single series.', file=sys.stderr)
      series, s_name = self.__make_series(
        group=groups,
        values=subset.data,
        indexes=subset[time_dim_name].data)
      series_names.append(s_name)
      series_list.append(series)
    else:
      if self.verbose:
        print('Creating multiple series.', file=sys.stderr)
      dates = subset[time_dim_name].data
      for group in groups:
        series, s_name = self.__make_series(
          group=group,
          values=subset.sel({
            grouping_dim_name: group
          }).data,
          indexes=dates)
        series_names.append(s_name)
        series_list.append(series)

    lon_interval[0] -= 3
    lon_interval[1] += 3
    lat_interval[0] -= 3
    lat_interval[1] += 3
    self._chart = time_series.SinglePointTimeSeries(
      series_names=series_names,
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
  

  def __make_series(self, group, values, indexes):
    s_name = group
    try:
      s_name = str(np.round(group, 3))
    except:
      pass
    series = pd.Series(values, index=indexes)
    return series, s_name
