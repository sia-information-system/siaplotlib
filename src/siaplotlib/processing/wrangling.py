import numpy as np
import xarray as xr
import pandas as pd
from datetime import datetime


def slice_dice(
  dataset: xr.DataArray,
  dim_constraints: dict[str, slice|list],
  var: str | list = None,
  squeeze = True
) -> xr.DataArray:
  """
  Makes a subset by dimension contraints and a selected (and optional)
  list of variables. A single variable name can be passed as a string.
  The dimensions take the nearest values to the specified. Unique values
  in dimensions are warranteed.
  """
  # Initializing.
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
      if type(dim_constraints[dim_name]) is list:
        constraints_w_no_slices[dim_name] = dim_constraints[dim_name]
      else:
        # Make it a list.
        constraints_w_no_slices[dim_name] = [ dim_constraints[dim_name] ]
  
  # Apply dimension constraints
  subset = subset.sel(constraints_w_no_slices, method = 'nearest')#.squeeze()
  subset = subset.sel(constraints_w_slices)#.squeeze()

  # Ensure unique values in constraints.
  dims_unique_values = get_dim_unique_values(dataset=subset)
  _dim_constraints = {}
  for dim_name in dim_constraints.keys():
    _dim_constraints[dim_name] = dims_unique_values[dim_name]

  # Subsetting again but with unique values in dimensions.
  subset = dataset
  # Selecting variables of interest.
  if var is not None:
    subset = dataset[var]
  if squeeze:
    subset = subset.sel(_dim_constraints).squeeze()
  else:
    subset = subset.sel(_dim_constraints)

  return subset


def get_dims(dataset: xr.Dataset) -> list[str]:
  return list(dataset.coords)


def get_vars(dataset: xr.Dataset) -> list[str]:
  return list(dataset.data_vars)


def get_dim_unique_values(dataset: xr.Dataset):
  dim_values = {}
  for dim in get_dims(dataset=dataset):
    dim_values[dim] = np.unique(dataset[dim].data)
  return dim_values


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
  s_name = str(name)
  if name_precition >= 0:
    try:
      s_name = str(np.round(name, name_precition))
    except:
      pass
    try:
      s_name = datetime.fromisoformat(name)
      pass
    except:
      pass
    try:
      if type(name) is np.datetime64:
        date_str = np.datetime_as_string(name)
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
