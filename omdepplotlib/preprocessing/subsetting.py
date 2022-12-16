import numpy as np
import xarray as xr


def slice_dice(
  dataset: xr.DataArray,
  dim_constraints: dict,
  var: str = None,
  rounding_precision: int = 3
  ) -> tuple[xr.DataArray, float | xr.DataArray, float | xr.DataArray]:
    """
    Make a subset by dimension contraints and a selected (and optional) variable.
    Also get valid minimun and maximun values for each variable. Minimun an maximun
    values are floats if a single variable was selected, or a DataArray if not.
    """
    vmin = 0
    vmax = 0
    if var is not None:
      subset = dataset[var].sel(dim_constraints, method = 'nearest').squeeze()
      vmin = np.round( subset.min().data, rounding_precision )
      vmax = np.round( subset.max().data, rounding_precision )
    else:
      subset = dataset.sel(dim_constraints, method = 'nearest').squeeze()
      vmin = np.round( subset.min(), rounding_precision )
      vmax = np.round( subset.max(), rounding_precision )
    
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
