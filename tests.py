import pathlib
import sys
import unittest
import time
import xarray as xr
from omdepplotlib.chart_building import cartographic_map
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

palette_colors = {
    'thetao': 'OrRd',
    'vo': 'plasma',
    'uo': 'plasma',
    'so': 'Greens',
    'zos': 'viridis'
}

class TestHeatMap(unittest.TestCase):

  def test_images(self):
    print('\n--- Starting heatmap static images test. ---', file=sys.stderr)
    time_start = time.time()
    dataset_path = pathlib.Path(
      DATA_DIR,
      'global-analysis-forecast-phy-001-024-GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS-date-2022-11-13-time-10h-31m-10s-857022ms.nc')
    dataset = xr.open_dataset(dataset_path)
    vis = cartographic_map.HeatMapBuilder(dataset=dataset, verbose=True)

    target_date = '2022-10-11'
    for variable in variables:
      dim_constraints = {
        'time': [target_date],
        'depth': [0.49402499198913574]
      }
      if variable == 'zos':
        dim_constraints = {
          'time': [target_date]
        }
      print(f'-> Heatmap static image for "{variable}" variable.', file=sys.stderr)
      vis.build_static(
        var=variable,
        title=f'{plot_titles[variable]} {target_date}',
        label=plot_legend_names[variable],
        dim_constraints=dim_constraints,
        lat_dim_name='latitude',
        lon_dim_name='longitude',
        color_palett=palette_colors[variable]
      )
      print(f'-> Image built.', file=sys.stderr)
      vis.save(pathlib.Path(VISUALIZATIONS_DIR, f'heatmap-{plot_titles[variable]}'))
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
    vis = cartographic_map.HeatMapBuilder(dataset=dataset, verbose=True)

    for variable in variables:
      print(f'-> Heatmap gif for "{variable}" variable.', file=sys.stderr)
      dim_constraints = {
        'depth': [0.49402499198913574]
      }
      if variable == 'zos':
        dim_constraints = {}
      vis.build_gif(
        var=variable,
        title=plot_titles[variable],
        label=plot_legend_names[variable],
        dim_constraints=dim_constraints,
        time_dim_name='time',
        lat_dim_name='latitude',
        lon_dim_name='longitude',
        duration=5,
        duration_unit='FRAMES_PER_SECOND',
        color_palett=palette_colors[variable])
      vis.save(pathlib.Path(VISUALIZATIONS_DIR, f'heatmap-{plot_titles[variable]}-ANIMATION.gif'))
    print(f'Gifs stored in: {VISUALIZATIONS_DIR}', file=sys.stderr)

    print('Finishing test.', file=sys.stderr)
    time_end = time.time()
    print(f'----> Time elapsed: {time_end - time_start}s.', file=sys.stderr)
    self.assertTrue(True)


class TestContourMap(unittest.TestCase):

  def test_images(self):
    print('\n--- Starting contour map static images test. ---', file=sys.stderr)
    time_start = time.time()
    dataset_path = pathlib.Path(
      DATA_DIR,
      'global-analysis-forecast-phy-001-024-GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS-date-2022-11-13-time-10h-31m-10s-857022ms.nc')
    dataset = xr.open_dataset(dataset_path)
    vis = cartographic_map.ContourMapBuilder(dataset=dataset, verbose=True)

    target_date = '2022-10-11'
    for variable in variables:
      dim_constraints = {
        'time': [target_date],
        'depth': [0.49402499198913574]
      }
      if variable == 'zos':
        dim_constraints = {
          'time': [target_date]
        }
      print(f'-> Contour map static image for "{variable}" variable.', file=sys.stderr)
      vis.build_static(
        var=variable,
        title=f'{plot_titles[variable]} {target_date}',
        label=plot_legend_names[variable],
        dim_constraints=dim_constraints,
        lat_dim_name='latitude',
        lon_dim_name='longitude',
        color_palett=palette_colors[variable],
        num_levels=9
      )
      print(f'-> Image built.', file=sys.stderr)
      vis.save(pathlib.Path(VISUALIZATIONS_DIR, f'contourmap-{plot_titles[variable]}'))
      print(f'-> Image saved', file=sys.stderr)
    print(f'Images stored in: {VISUALIZATIONS_DIR}', file=sys.stderr)

    print('Finishing test.', file=sys.stderr)
    time_end = time.time()
    print(f'----> Time elapsed: {time_end - time_start}s.', file=sys.stderr)
    self.assertTrue(True)
  

  def test_gifs(self):
    print('\n--- Starting contour map gifs test. ---', file=sys.stderr)
    time_start = time.time()

    # depth=0.49402499198913574,
    # start_date='2020-01-01',
    # end_date='2020-12-01'

    dataset_path = pathlib.Path(
      DATA_DIR,
      'global-analysis-forecast-phy-001-024-GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS-date-2022-11-13-time-13h-27m-31s-211639ms-monthly.nc')
    dataset = xr.open_dataset(dataset_path)
    vis = cartographic_map.ContourMapBuilder(dataset=dataset, verbose=True)

    for variable in variables:
      print(f'-> Contout map gif for "{variable}" variable.', file=sys.stderr)
      dim_constraints = {
        'depth': [0.49402499198913574]
      }
      if variable == 'zos':
        dim_constraints = {}
      vis.build_gif(
        var=variable,
        title=plot_titles[variable],
        label=plot_legend_names[variable],
        dim_constraints=dim_constraints,
        time_dim_name='time',
        lat_dim_name='latitude',
        lon_dim_name='longitude',
        duration=5,
        duration_unit='FRAMES_PER_SECOND',
        num_levels=9,
        color_palett=palette_colors[variable])
      vis.save(pathlib.Path(VISUALIZATIONS_DIR, f'contourmap-{plot_titles[variable]}-ANIMATION.gif'))
    print(f'Gifs stored in: {VISUALIZATIONS_DIR}', file=sys.stderr)

    print('Finishing test.', file=sys.stderr)
    time_end = time.time()
    print(f'----> Time elapsed: {time_end - time_start}s.', file=sys.stderr)
    self.assertTrue(True)

if __name__ == '__main__':
  general_utils.mkdir_r(VISUALIZATIONS_DIR)
  unittest.main()
