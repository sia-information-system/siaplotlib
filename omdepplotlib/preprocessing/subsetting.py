import numpy as np
import xarray as xr


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
