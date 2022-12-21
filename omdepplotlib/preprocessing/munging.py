import numpy as np
import xarray as xr
import pandas as pd
from datetime import datetime


def slice_dice(
  dataset: xr.DataArray,
  dim_constraints: dict,
  var: str | list = None,
  rounding_precision: int = 3
) -> tuple[xr.DataArray, float | xr.DataArray, float | xr.DataArray]:
  """
  Make a subset by dimension contraints and a selected (and optional) variable.
  Also get valid minimun and maximun values for each variable. Minimun an maximun
  values are floats if a single variable was selected, or a DataArray if not.

  It returns: subset, vmin, vmax
  """
  # Initializing.
  vmin = 0
  vmax = 0
  subset = dataset

  # Selecting variables of interest.
  if var is not None:
    subset = dataset[var]
  
  constraints_w_slices = {}
  constraints_w_no_slices = {}
  for dim_name in dim_constraints.keys():
    if type(dim_constraints[dim_name]) is slice:
      constraints_w_slices[dim_name] = dim_constraints[dim_name]
    else:
      constraints_w_no_slices[dim_name] = dim_constraints[dim_name]
  
  # Apply dimension constraints
  subset = subset.sel(constraints_w_no_slices, method = 'nearest').squeeze()
  subset = subset.sel(constraints_w_slices).squeeze()

  # Minimun and maximun.
  if(len(subset) > 0):
    vmin = np.round( subset.min(), rounding_precision )
    vmax = np.round( subset.max(), rounding_precision )
    try:
      vmin = float(vmin)
      vmax = float(vmax)
    except:
      pass
  
  return subset, vmin, vmax


def get_coords(
  dataset: xr.DataArray,
  lon_dim_name: str,
  lat_dim_name: str,
  rounding_precision: int = 3
) -> tuple[np.ndarray, np.ndarray, list, list]:
  """
  Get the coordinates of a given dataset. Also get the minimun and
  maximun values for each dimension.

  It returns: lon_data, lat_data, lon_interval, lat_interval
  """
  lon_data = dataset[lon_dim_name]
  lat_data = dataset[lat_dim_name]
  lon_interval = [
    np.round( float(lon_data.min().data), rounding_precision ),
    np.round( float(lon_data.max().data), rounding_precision )
  ]
  lat_interval = [
    np.round( float(lat_data.min().data), rounding_precision ),
    np.round( float(lat_data.max().data), rounding_precision )
  ]
  return lon_data.data, lat_data.data, lon_interval, lat_interval


def make_series(
  data: np.ndarray,
  index: np.ndarray,
  name: str,
  name_precition: int = 3
):
  """
  Create an instance of a pandas.Series with a name. If the name is a number,
  it can be rounded with a certain name_precition (by default name_precition=3).
  If name_precition < 0, then no rounding is done.
  """
  s_name = name
  if name_precition >= 0:
    try:
      s_name = str(np.round(name, name_precition))
    except:
      pass
    try:
      s_name = datetime.fromisoformat(s_name)
      pass
    except:
      pass
    try:
      if type(s_name) is np.datetime64:
        date_str = np.datetime_as_string(s_name)
        s_name = datetime.strptime(date_str,'%Y-%m-%dT%H:%M:%S.%f000').strftime("%Y-%m-%d %H:%M:%S")
    except:
      pass
  series = pd.Series(data, index=index, name=s_name)
  return series


def group_into_series(
  dataset: xr.DataArray,
  x_dim_name: str,
  grouping_dim_name: str,
  reverse_axis: bool = False
) -> list[pd.Series]:
  """
  Generate a list of series from a xarray.DataArray using
  a selected dimension as index and the only variable in the
  xarray.DataArray as data. The axes can be reversed to use
  the dimension as data and the only variable as index.
  Each series is determined by the grouping variable.
  """
  groups = None
  if grouping_dim_name is not None:
    groups = dataset[grouping_dim_name].data
  else:
    groups = np.array(None)
  series_list = []

  if len(groups.shape) == 0:
    data = dataset.data
    index = dataset[x_dim_name].data
    if reverse_axis:
      data = dataset[x_dim_name].data
      index = dataset.data
    series = make_series(
      name=groups,
      data=data,
      index=index)
    series_list.append(series)
  else:
    for group in groups:
      data = dataset.sel({
        grouping_dim_name: group
      }).data
      index = dataset[x_dim_name].data
      if reverse_axis:
        data = dataset[x_dim_name].data
        index = dataset.sel({
          grouping_dim_name: group
        }).data
      series = make_series(
        name=group,
        data=data,
        index=index)
      series_list.append(series)
  return series_list
