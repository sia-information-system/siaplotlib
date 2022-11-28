import pathlib
import sys
import unittest
import time
import xarray as xr
from omdepplotlib.preprocessing import dataframe
from omdepplotlib.chart_building import heatmap
import tools.general_utils as general_utils

VISUALIZATIONS_DIR = pathlib.Path(pathlib.Path(__file__).parent.absolute(), 'tmp', 'visualizations')
DATA_DIR = pathlib.Path(pathlib.Path(__file__).parent.absolute(), 'tmp', 'data')

variables = ['thetao', 'vo', 'uo', 'so', 'zos']

plot_titles = {
  'thetao': 'Temperature',
  'vo': 'Northward velocity (vo)',
  'uo': 'Eastward velocity (uo)',
  'so': 'Salinity (so)',
  'zos': 'Sea surface height (zos)'
}

plot_legend_names = {
  'thetao': 'Degrees Celsius',
  'vo': 'Meters per second',
  'uo': 'Meters per second',
  'so': 'Practical Salinity Unit',
  'zos': 'Meters'
}

class TestDataVisualization(unittest.TestCase):

  def test_images(self):
    print('\n--- Starting heatmap static images test. ---', file=sys.stderr)
    time_start = time.time()
    dataset_path = pathlib.Path(
      DATA_DIR,
      'global-analysis-forecast-phy-001-024-GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS-date-2022-11-13-time-10h-31m-10s-857022ms.nc')
    dataset = xr.open_dataset(dataset_path)

    prep = dataframe.DataframePreprocessor(dataset)
    vis = heatmap.HeatMapBuilder(prep)

    for variable in variables:
      print(f'-> Heatmap static image for "{variable}" variable.', file=sys.stderr)
      vis.build_static(
        var=variable,
        chart_title=plot_titles[variable],
        name_legend=plot_legend_names[variable],
        dim_constraints={
          'time': ['2022-10-11'],
          'depth': [0.49402499198913574]
        }
      )
      print(f'-> Image built.', file=sys.stderr)
      vis.save(pathlib.Path(VISUALIZATIONS_DIR, plot_titles[variable]))
      print(f'-> Image saved', file=sys.stderr)
    print(f'Images stored in: {VISUALIZATIONS_DIR}', file=sys.stderr)

    print('Finishing test.', file=sys.stderr)
    time_end = time.time()
    print(f'----> Time elapsed: {time_end - time_start}s.', file=sys.stderr)
    self.assertTrue(True)

  def test_gifs(self):
    print('\n--- Starting heatmap gifs test. ---', file=sys.stderr)
    time_start = time.time()

    # depth=0.49402499198913574,
    # start_date='2020-01-01',
    # end_date='2020-12-01'

    dataset_path = pathlib.Path(
      DATA_DIR,
      'global-analysis-forecast-phy-001-024-GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS-date-2022-11-13-time-13h-27m-31s-211639ms-monthly.nc')
    dataset = xr.open_dataset(dataset_path)

    prep = dataframe.DataframePreprocessor(dataset)
    vis = heatmap.HeatMapBuilder(prep)

    for variable in variables:
      print(f'-> Heatmap gif for "{variable}" variable.', file=sys.stderr)
      vis.build_gif(
        var=variable,
        chart_title=plot_titles[variable],
        name_legend=plot_legend_names[variable],
        dim_constraints={
          'depth': [0.49402499198913574]
        })
      vis.save(pathlib.Path(VISUALIZATIONS_DIR, f'{plot_titles[variable]}-ANIMATION.gif'))
    print(f'Gifs stored in: {VISUALIZATIONS_DIR}', file=sys.stderr)

    print('Finishing test.', file=sys.stderr)
    time_end = time.time()
    print(f'----> Time elapsed: {time_end - time_start}s.', file=sys.stderr)
    self.assertTrue(True)

if __name__ == '__main__':
  general_utils.mkdir_r(VISUALIZATIONS_DIR)
  unittest.main()
