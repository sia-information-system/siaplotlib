# Standard
import unittest
import sys
from pathlib import Path
# Third party
import xarray as xr
# Own
from siaplotlib.processing.parallelism import AsyncRunner
from siaplotlib.processing import wrangling

# Custom test dependencies
from lib_utils.general_utils import DATA_DIR

DATASET_NAME_1 = 'global-analysis-forecast-phy-001-024-GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS-date-2022-11-13-time-10h-31m-10s-857022ms.nc'
DATASET_NAME_2 = 'global-analysis-forecast-phy-001-024-GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS-date-2022-11-13-time-13h-27m-31s-211639ms-monthly.nc'

class TestAsyncRunner(unittest.TestCase):
  def __init__(self, methodName: str = "runTest") -> None:
    super().__init__(methodName)
    self.async_process_ok: bool = False


  def sync_fn(self, text: str):
    text_splited = text.split(' ')
    l = len(text_splited)
    return text_splited, l


  def sync_fn_success_callback(self, text_splited, length):
    print(f'\nText splited: {text_splited}. Length: {length}')
    self.async_process_ok = True
  

  def sync_fn_failure_callback(self, err):
    self.async_process_ok = False
    print(err)


  def test_async_runner(self):
    self.async_process_ok = False
    async_runner = AsyncRunner(
      sync_fn=self.sync_fn,
      sync_fn_kwargs={'text': 'hello, world!'},
      success_callback=self.sync_fn_success_callback,
      failure_callback=self.sync_fn_failure_callback)
    async_runner.run()
    async_runner.wait()
    self.assertTrue(self.async_process_ok)
  

  def sync_fn_1_return_val(self, text: str):
    text_splited = text.split(' ')
    return text_splited


  def sync_fn_1_return_val_success_callback(self, text_splited):
    print(f'\nText splited: {text_splited}.')
    self.async_process_ok = True


  def test_async_runner_1_return_val(self):
    self.async_process_ok = False
    async_runner = AsyncRunner(
      sync_fn=self.sync_fn_1_return_val,
      sync_fn_kwargs={'text': 'hello, world!'},
      success_callback=self.sync_fn_1_return_val_success_callback,
      failure_callback=self.sync_fn_failure_callback)
    async_runner.run()
    async_runner.wait()
    self.assertTrue(self.async_process_ok)
  

  def sync_fn_return_int(self, text: str):
    text_splited = text.split(' ')
    return len(text_splited)


  def sync_fn_return_int_success_callback(self, text_splited):
    print(f'\nText splited length: {text_splited}.')
    self.async_process_ok = True


  def test_async_runner_return_int(self):
    self.async_process_ok = False
    async_runner = AsyncRunner(
      sync_fn=self.sync_fn_return_int,
      sync_fn_kwargs={'text': 'hello, world!'},
      success_callback=self.sync_fn_return_int_success_callback,
      failure_callback=self.sync_fn_failure_callback)
    async_runner.run()
    async_runner.wait()
    self.assertTrue(self.async_process_ok)
  

  def sync_fn_catch_tuple(self, *tp):
    print(f'\nTuple: {tp}')
    self.async_process_ok = True

  
  def test_async_runner_catch_tupples(self):
    self.async_process_ok = False
    async_runner = AsyncRunner(
      sync_fn=self.sync_fn,
      sync_fn_kwargs={'text': 'hello, world!'},
      success_callback=self.sync_fn_catch_tuple,
      failure_callback=self.sync_fn_failure_callback)
    async_runner.run()
    async_runner.wait()
    self.assertTrue(self.async_process_ok)


class TestDatasetTransformations(unittest.TestCase):
  def test_compute_single_velocity(self):
    dataset_path = Path(DATA_DIR, DATASET_NAME_1)
    dataset = xr.open_dataset(dataset_path)
    northward_var_name = 'vo'
    eastward_var_name = 'uo'
    single_vel_var_name = 'single_velocity'
    new_ds = wrangling.calc_unique_velocity(
      dataset=dataset,
      eastward_var_name=eastward_var_name,
      northward_var_name=northward_var_name,
      unique_velocity_name=single_vel_var_name)
    print('--- NEW DATASET:', file=sys.stderr)
    print(new_ds, file=sys.stderr)
    print('--- NEW VAR ATTRS:', file=sys.stderr)
    print(new_ds[single_vel_var_name].attrs, file=sys.stderr)
    print('--- PREVIOUS DATASET:', file=sys.stderr)
    print(dataset, file=sys.stderr)


if __name__ == '__main__':
  unittest.main()
