import xarray as xr
import numpy as np


def calc_bins(
    speed: np.ndarray,
    bin_min: float,
    bin_max: float,
    bin_jmp: float
    ) -> np.ndarray : 
    max_v =  speed.max()

    if bin_min >= max_v:
       bin_min = speed.min()  
    
    bins = np.arange(bin_min, bin_max, bin_jmp) 
    return bins
    

def calc_spd(
    dataset: xr.DataArray,
    eastward_var_name: str,
    northward_var_name:str
    ) -> np.ndarray :
    F =  np.sqrt(dataset[eastward_var_name]**2 + dataset[northward_var_name]**2)
    return F.values

def calc_dir(
    dataset: xr.DataArray,
    eastward_var_name: str,
    northward_var_name:str
    ) -> np.ndarray :
    F = (90-(np.arctan2(dataset[eastward_var_name], dataset[northward_var_name]) * (180 / np.pi)))
    return F.values

def calc_uniqueDir(
    dataset: xr.DataArray,
    eastward_var_name: str,
    northward_var_name:str
    ) -> tuple[np.ndarray, np.ndarray] :
    
    speed = calc_spd(dataset= dataset,
      eastward_var_name = eastward_var_name,
      northward_var_name = northward_var_name)
    
    direction = calc_dir(dataset= dataset,
      eastward_var_name = eastward_var_name,
      northward_var_name = northward_var_name)
    
    return speed, direction

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
