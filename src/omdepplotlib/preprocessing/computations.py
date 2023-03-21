import xarray as xr
import numpy as np

def calc_spd(
    dataset: xr.DataArray,
    var_ew: str,
    var_nw:str
    ) -> np.ndarray :
    F =  np.sqrt(dataset[var_ew]**2 + dataset[var_nw]**2)
    return F.values

def calc_dir(
    dataset: xr.DataArray,
    var_ew: str,
    var_nw:str
    ) -> np.ndarray :
    F = (90-(np.arctan2(dataset[var_ew], dataset[var_nw]) * (180 / np.pi)))
    return F.values

def corr_cord(
    dataset: np.ndarray 
    ) -> np.ndarray :
    return xr.where(dataset < 0, dataset + 360, dataset)

def drop_nan(
    dataset: np.ndarray 
) -> np.ndarray :
    nan_indices = np.isnan(dataset)
    dataset = dataset[~nan_indices]
    return dataset
