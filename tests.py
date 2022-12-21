import pathlib
import sys
import unittest
import time
import xarray as xr
from omdepplotlib.chart_building import cartographic_map, line_chart
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

# plot_legend_names = {
#     'thetao': 'Temperature (C°)',
#     'vo': 'Northward velocity (m/s)',
#     'uo': 'Eastward velocity (m/s)',
#     'so': 'Salinity (PSU)',
# }

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
      vis.build_animation(
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
      vis.build_animation(
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


class TestSinglePointTimeSeries(unittest.TestCase):
  def test_many_depths(self):
    print('\n--- Starting time series static images test with many depths. ---', file=sys.stderr)
    time_start = time.time()
    dataset_path = pathlib.Path(
      DATA_DIR,
      'global-analysis-forecast-phy-001-024-GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS-date-2022-11-13-time-13h-27m-31s-211639ms-monthly.nc')
    dataset = xr.open_dataset(dataset_path)
    vis = line_chart.SinglePointTimeSeriesBuilder(dataset=dataset, verbose=True)

    date_range = slice('2020-01-01', '2020-12-01')
    for variable in variables:
      grouping_dim_name='depth'
      dim_constraints = {
        'time': date_range,
        'depth': [0, 100, 250, 500, 1000],
        'latitude': 21,
        'longitude': -86
      }
      if variable == 'zos':
        dim_constraints = {
          'time': date_range,
          'latitude': 21,
          'longitude': -86
        }
        grouping_dim_name=None
      print(f'-> Static single-point time-series image for "{variable}" variable.', file=sys.stderr)
      vis.build_static(
        var=variable,
        title=f'{plot_titles[variable]} time series',
        grouping_dim_label='Depth (m)',
        dim_constraints=dim_constraints,
        lat_dim_name='latitude',
        lon_dim_name='longitude',
        grouping_dim_name=grouping_dim_name,
        time_dim_name='time',
        y_label=plot_legend_names[variable],
        x_label='Dates'
      )
      print(f'-> Image built.', file=sys.stderr)
      vis.save(pathlib.Path(VISUALIZATIONS_DIR, f'single-point-time-series-{plot_titles[variable]}'))
      print(f'-> Image saved', file=sys.stderr)
    
    print(f'Images stored in: {VISUALIZATIONS_DIR}', file=sys.stderr)
    print('Finishing test.', file=sys.stderr)
    time_end = time.time()
    print(f'----> Time elapsed: {time_end - time_start}s.', file=sys.stderr)
    self.assertTrue(True)
  

  def test_single_depth(self):
    print('\n--- Starting time series static images test with single depth. ---', file=sys.stderr)
    time_start = time.time()
    dataset_path = pathlib.Path(
      DATA_DIR,
      'global-analysis-forecast-phy-001-024-GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS-date-2022-11-13-time-13h-27m-31s-211639ms-monthly.nc')
    dataset = xr.open_dataset(dataset_path)
    vis = line_chart.SinglePointTimeSeriesBuilder(dataset=dataset, verbose=True)

    date_range = slice('2020-01-01', '2020-12-01')
    for variable in variables:
      grouping_dim_name='depth'
      dim_constraints = {
        'time': date_range,
        'depth': [0.49402499198913574],
        'latitude': 21,
        'longitude': -86
      }
      if variable == 'zos':
        dim_constraints = {
          'time': date_range,
          'latitude': 21,
          'longitude': -86
        }
        grouping_dim_name=None
      print(f'-> Static single-point time-series image for "{variable}" variable.', file=sys.stderr)
      vis.build_static(
        var=variable,
        title=f'{plot_titles[variable]} time series',
        grouping_dim_label='Depth (m)',
        dim_constraints=dim_constraints,
        lat_dim_name='latitude',
        lon_dim_name='longitude',
        grouping_dim_name=grouping_dim_name,
        time_dim_name='time',
        y_label=plot_legend_names[variable],
        x_label='Dates'
      )
      print(f'-> Image built.', file=sys.stderr)
      vis.save(pathlib.Path(VISUALIZATIONS_DIR, f'one-depth-single-point-time-series-{plot_titles[variable]}'))
      print(f'-> Image saved', file=sys.stderr)
    
    print(f'Images stored in: {VISUALIZATIONS_DIR}', file=sys.stderr)
    print('Finishing test.', file=sys.stderr)
    time_end = time.time()
    print(f'----> Time elapsed: {time_end - time_start}s.', file=sys.stderr)
    self.assertTrue(True)


class TestSinglePointVerticalProfile(unittest.TestCase):
  def test_many_dates(self):
    print('\n--- Starting time series static images test with many dates. ---', file=sys.stderr)
    time_start = time.time()
    dataset_path = pathlib.Path(
      DATA_DIR,
      'global-analysis-forecast-phy-001-024-GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS-date-2022-11-13-time-13h-27m-31s-211639ms-monthly.nc')
    dataset = xr.open_dataset(dataset_path)
    vis = line_chart.SinglePointVerticalProfileBuilder(dataset=dataset, verbose=True)

    date_range = ['2020-03-01', '2020-06-01', '2020-09-01', '2020-12-01']
    for variable in variables:
      grouping_dim_name='time'
      dim_constraints = {
        'time': date_range,
        'latitude': 21,
        'longitude': -86
      }
      if variable == 'zos':
        continue
      print(f'-> Static single-point vertical profile image for "{variable}" variable.', file=sys.stderr)
      vis.build_static(
        var=variable,
        title=f'{plot_titles[variable]} by depth',
        grouping_dim_label='Dates',
        dim_constraints=dim_constraints,
        lat_dim_name='latitude',
        lon_dim_name='longitude',
        grouping_dim_name=grouping_dim_name,
        depth_dim_name='depth',
        y_label='Depth',
        x_label=plot_legend_names[variable]
      )
      print(f'-> Image built.', file=sys.stderr)
      vis.save(pathlib.Path(VISUALIZATIONS_DIR, f'single-point-vertical-profile-{plot_titles[variable]}'))
      print(f'-> Image saved', file=sys.stderr)
    
    print(f'Images stored in: {VISUALIZATIONS_DIR}', file=sys.stderr)
    print('Finishing test.', file=sys.stderr)
    time_end = time.time()
    print(f'----> Time elapsed: {time_end - time_start}s.', file=sys.stderr)
    self.assertTrue(True)


if __name__ == '__main__':
  general_utils.mkdir_r(VISUALIZATIONS_DIR)
  unittest.main()
