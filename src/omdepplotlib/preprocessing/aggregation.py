import xarray as xr
import numpy as np

def min(
  dataset: xr.DataArray,
  rounding_precision: int = -1
) -> float | xr.DataArray:
  """
  Get valid minimun values for each variable in the dataset. The returned value 
  is float if there is a single variable in the dataset, a DataArray if not.

  A rounding precision can be set. Set it to a negative number for no rounding.
  """
  vmin = dataset.min()
  if rounding_precision >= 0:
    vmin = np.round( vmin, rounding_precision )
  try:
    vmin = float(vmin)
  except:
    pass
  return vmin

def max(
  dataset: xr.DataArray,
  rounding_precision: int = -1
) -> float | xr.DataArray:
  """
  Get valid maximun values for each variable in the dataset. The returned value 
  is float if there is a single variable in the dataset, a DataArray if not.

  A rounding precision can be set. Set it to a negative number for no rounding.
  """
  vmax = dataset.max()
  if rounding_precision >= 0:
    vmax = np.round( vmax, rounding_precision )
  try:
    vmax = float(vmax)
  except:
    pass
  return vmax
