import pathlib
import sys
import unittest
import time
import xarray as xr
from omdepplotlib.chart_building import level_chart, line_chart
from lib_utils.general_utils import VISUALIZATIONS_DIR, DATA_DIR
import lib_utils.general_utils as general_utils

# Setup

DATASET_NAME_1 = 'global-analysis-forecast-phy-001-024-GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS-date-2022-11-13-time-10h-31m-10s-857022ms.nc'
DATASET_NAME_2 = 'global-analysis-forecast-phy-001-024-GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS-date-2022-11-13-time-13h-27m-31s-211639ms-monthly.nc'

variables = ['thetao', 'vo', 'uo', 'so', 'zos']
plot_titles = {
  'thetao': 'Temperature',
  'vo': 'Northward velocity (vo)',
  'uo': 'Eastward velocity (uo)',
  'so': 'Salinity (so)',
  'zos': 'Sea surface height (zos)'
}
# plot_measure_label = {
#   'thetao': 'Degrees Celsius',
#   'vo': 'Meters per second',
#   'uo': 'Meters per second',
#   'so': 'Practical Salinity Unit',
#   'zos': 'Meters'
# }
plot_measure_label = {
    'thetao': 'Temperature (C°)',
    'vo': 'Northward velocity (m/s)',
    'uo': 'Eastward velocity (m/s)',
    'so': 'Salinity (PSU)',
    'zos': 'Sea surface height (m)'
}
palette_colors = {
    'thetao': 'OrRd',
    'vo': 'plasma',
    'uo': 'plasma',
    'so': 'Greens',
    'zos': 'viridis'
}

# Test definitions.
class TestWindRose(unittest.TestCase):
  def test_images(self):
    print('\n--- Starting windrose static images test. ---',
      file=sys.stderr)
    time_start = time.time()
    dataset_path = pathlib.Path(
      DATA_DIR,
      DATASET_NAME_1)
    dataset = xr.open_dataset(dataset_path)
    chart_builder = level_chart.WindRoseBuilder(
      dataset=dataset,
      verbose=True)
    
    target_date = '2022-10-11'
    depth = 0

    dim_constraints = {
        'time': [target_date],
        'depth': [0],
        'latitude': slice(15, 20),
        'longitude': slice(-85, 82)
      }
    
    lat = [15,20]
    lon = [-85,-82]

    chart_builder.build_static(
        var_ew = 'uo',
        var_nw = 'vo',
        title = f'Windrose del {target_date}\nCoordenadas\n lat: {lat} y lon: {lon}\n Depth: {depth}',
        color_palette = 'viridis',
        dim_constraints= dim_constraints,
      )
    
    print(f'-> Image built.', file=sys.stderr)
    chart_builder.save(
      pathlib.Path(
      VISUALIZATIONS_DIR,
      f'windrose-test'))
    print(f'-> Image saved', file=sys.stderr)

    print(f'Images stored in: {VISUALIZATIONS_DIR}', file=sys.stderr)
    print('Finishing test.', file=sys.stderr)
    time_end = time.time()
    print(f'----> Time elapsed: {time_end - time_start}s.', file=sys.stderr)
    self.assertTrue(True)

class TestHeatMap(unittest.TestCase):
  def test_images(self):
    print('\n--- Starting heatmap static images test. ---',
      file=sys.stderr)
    time_start = time.time()
    dataset_path = pathlib.Path(
      DATA_DIR,
      DATASET_NAME_1)
    dataset = xr.open_dataset(dataset_path)
    chart_builder = level_chart.HeatMapBuilder(
      dataset=dataset,
      verbose=True)

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
      print(f'-> Heatmap static image for "{variable}" variable.',
        file=sys.stderr)
      chart_builder.build_static(
        var_name=variable,
        title=f'{plot_titles[variable]} {target_date}',
        var_label=plot_measure_label[variable],
        dim_constraints=dim_constraints,
        lat_dim_name='latitude',
        lon_dim_name='longitude',
        color_palette=palette_colors[variable]
      )
      print(f'-> Image built.', file=sys.stderr)
      chart_builder.save(
        pathlib.Path(
          VISUALIZATIONS_DIR,
          f'heatmap-{plot_titles[variable]}'))
      print(f'-> Image saved', file=sys.stderr)
    
    print(f'Images stored in: {VISUALIZATIONS_DIR}', file=sys.stderr)
    print('Finishing test.', file=sys.stderr)
    time_end = time.time()
    print(f'----> Time elapsed: {time_end - time_start}s.', file=sys.stderr)
    self.assertTrue(True)

  def test_gifs(self):
    print('\n--- Starting heatmap gifs test. ---', file=sys.stderr)
    time_start = time.time()

    dataset_path = pathlib.Path(
      DATA_DIR,
      DATASET_NAME_2)
    dataset = xr.open_dataset(dataset_path)
    chart_builder = level_chart.HeatMapBuilder(
      dataset=dataset,
      verbose=True)

    for variable in variables:
      print(f'-> Heatmap gif for "{variable}" variable.',
        file=sys.stderr)
      dim_constraints = {
        'depth': [0.49402499198913574]
      }
      if variable == 'zos':
        dim_constraints = {}
      chart_builder.build_animation(
        var_name=variable,
        title=plot_titles[variable],
        var_label=plot_measure_label[variable],
        dim_constraints=dim_constraints,
        time_dim_name='time',
        lat_dim_name='latitude',
        lon_dim_name='longitude',
        duration=5,
        duration_unit='FRAMES_PER_SECOND',
        color_palette=palette_colors[variable])
      chart_builder.save(
        pathlib.Path(
          VISUALIZATIONS_DIR,
          f'heatmap-{plot_titles[variable]}-ANIMATION.gif'))
    
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
      DATASET_NAME_1)
    dataset = xr.open_dataset(dataset_path)
    chart_builder = level_chart.ContourMapBuilder(
      dataset=dataset,
      verbose=True)

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
      print(f'-> Contour map static image for "{variable}" variable.',
        file=sys.stderr)
      chart_builder.build_static(
        var_name=variable,
        title=f'{plot_titles[variable]} {target_date}',
        var_label=plot_measure_label[variable],
        dim_constraints=dim_constraints,
        lat_dim_name='latitude',
        lon_dim_name='longitude',
        color_palette=palette_colors[variable],
        num_levels=9
      )
      print(f'-> Image built.', file=sys.stderr)
      chart_builder.save(
        pathlib.Path(
          VISUALIZATIONS_DIR,
          f'contourmap-{plot_titles[variable]}'))
      print(f'-> Image saved', file=sys.stderr)
    
    print(f'Images stored in: {VISUALIZATIONS_DIR}', file=sys.stderr)
    print('Finishing test.', file=sys.stderr)
    time_end = time.time()
    print(f'----> Time elapsed: {time_end - time_start}s.', file=sys.stderr)
    self.assertTrue(True)
  

  def test_gifs(self):
    print('\n--- Starting contour map gifs test. ---', file=sys.stderr)
    time_start = time.time()

    dataset_path = pathlib.Path(
      DATA_DIR,
      DATASET_NAME_2)
    dataset = xr.open_dataset(dataset_path)
    chart_builder = level_chart.ContourMapBuilder(
      dataset=dataset,
      verbose=True)

    for variable in variables:
      print(f'-> Contout map gif for "{variable}" variable.',
        file=sys.stderr)
      dim_constraints = {
        'depth': [0.49402499198913574]
      }
      if variable == 'zos':
        dim_constraints = {}
      chart_builder.build_animation(
        var_name=variable,
        title=plot_titles[variable],
        var_label=plot_measure_label[variable],
        dim_constraints=dim_constraints,
        time_dim_name='time',
        lat_dim_name='latitude',
        lon_dim_name='longitude',
        duration=5,
        duration_unit='FRAMES_PER_SECOND',
        num_levels=9,
        color_palette=palette_colors[variable])
      chart_builder.save(
        pathlib.Path(
          VISUALIZATIONS_DIR,
          f'contourmap-{plot_titles[variable]}-ANIMATION.gif'))
    
    print(f'Gifs stored in: {VISUALIZATIONS_DIR}', file=sys.stderr)
    print('Finishing test.', file=sys.stderr)
    time_end = time.time()
    print(f'----> Time elapsed: {time_end - time_start}s.', file=sys.stderr)
    self.assertTrue(True)


class TestSinglePointTimeSeries(unittest.TestCase):
  def test_many_depths(self):
    print('\n--- Starting time series static images test with many depths. ---',
      file=sys.stderr)
    time_start = time.time()
    dataset_path = pathlib.Path(
      DATA_DIR,
      DATASET_NAME_2)
    dataset = xr.open_dataset(dataset_path)
    chart_builder = line_chart.SinglePointTimeSeriesBuilder(
      dataset=dataset,
      verbose=True)

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
      print(f'-> Static single-point time-series image for "{variable}" variable.',
        file=sys.stderr)
      chart_builder.build_static(
        var_name=variable,
        title=f'{plot_titles[variable]} time series',
        grouping_dim_label='Depth (m)',
        dim_constraints=dim_constraints,
        lat_dim_name='latitude',
        lon_dim_name='longitude',
        grouping_dim_name=grouping_dim_name,
        time_dim_name='time',
        var_label=plot_measure_label[variable],
        time_dim_label='Dates'
      )
      print(f'-> Image built.', file=sys.stderr)
      chart_builder.save(
        pathlib.Path(
          VISUALIZATIONS_DIR,
          f'single-point-time-series-{plot_titles[variable]}'))
      print(f'-> Image saved', file=sys.stderr)
    
    print(f'Images stored in: {VISUALIZATIONS_DIR}', file=sys.stderr)
    print('Finishing test.', file=sys.stderr)
    time_end = time.time()
    print(f'----> Time elapsed: {time_end - time_start}s.', file=sys.stderr)
    self.assertTrue(True)
  

  def test_single_depth(self):
    print('\n--- Starting time series static images test with single depth. ---',
      file=sys.stderr)
    time_start = time.time()
    dataset_path = pathlib.Path(
      DATA_DIR,
      DATASET_NAME_2)
    dataset = xr.open_dataset(dataset_path)
    chart_builder = line_chart.SinglePointTimeSeriesBuilder(
      dataset=dataset,
      verbose=True)

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
      print(f'-> Static single-point time-series image for "{variable}" variable.',
        file=sys.stderr)
      chart_builder.build_static(
        var_name=variable,
        title=f'{plot_titles[variable]} time series',
        grouping_dim_label='Depth (m)',
        dim_constraints=dim_constraints,
        lat_dim_name='latitude',
        lon_dim_name='longitude',
        grouping_dim_name=grouping_dim_name,
        time_dim_name='time',
        var_label=plot_measure_label[variable],
        time_dim_label='Dates'
      )
      print(f'-> Image built.', file=sys.stderr)
      chart_builder.save(
        pathlib.Path(
          VISUALIZATIONS_DIR,
          f'one-depth-single-point-time-series-{plot_titles[variable]}'))
      print(f'-> Image saved', file=sys.stderr)
    
    print(f'Images stored in: {VISUALIZATIONS_DIR}', file=sys.stderr)
    print('Finishing test.', file=sys.stderr)
    time_end = time.time()
    print(f'----> Time elapsed: {time_end - time_start}s.', file=sys.stderr)
    self.assertTrue(True)


class TestSinglePointVerticalProfile(unittest.TestCase):
  def test_many_dates(self):
    print('\n--- Starting time series static images test with many dates. ---',
      file=sys.stderr)
    time_start = time.time()
    dataset_path = pathlib.Path(
      DATA_DIR,
      DATASET_NAME_2)
    dataset = xr.open_dataset(dataset_path)
    chart_builder = line_chart.SinglePointVerticalProfileBuilder(
      dataset=dataset,
      verbose=True)

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
      print(f'-> Static single-point vertical profile image for "{variable}" variable.',
        file=sys.stderr)
      chart_builder.build_static(
        var_name=variable,
        title=f'{plot_titles[variable]} by depth',
        grouping_dim_label='Dates',
        dim_constraints=dim_constraints,
        lat_dim_name='latitude',
        lon_dim_name='longitude',
        grouping_dim_name=grouping_dim_name,
        y_dim_name='depth',
        y_dim_label='Depth',
        var_label=plot_measure_label[variable]
      )
      print(f'-> Image built.', file=sys.stderr)
      chart_builder.save(
        pathlib.Path(
          VISUALIZATIONS_DIR,
          f'single-point-vertical-profile-{plot_titles[variable]}'))
      print(f'-> Image saved', file=sys.stderr)
    
    print(f'Images stored in: {VISUALIZATIONS_DIR}', file=sys.stderr)
    print('Finishing test.', file=sys.stderr)
    time_end = time.time()
    print(f'----> Time elapsed: {time_end - time_start}s.', file=sys.stderr)
    self.assertTrue(True)


class TestVerticalSlice(unittest.TestCase):
  def test_static(self):
    print('\n--- Starting vertical slice for static image. ---',
      file=sys.stderr)
    time_start = time.time()
    dataset_path = pathlib.Path(
      DATA_DIR,
      DATASET_NAME_2)
    dataset = xr.open_dataset(dataset_path)
    chart_builder = level_chart.VerticalSliceBuilder(
      dataset=dataset,
      verbose=True)

    date = '2020-01-01'
    for variable in variables:
      dim_constraints = {
        'time': date,
        'latitude': slice(15, 27),
        'longitude': -85
      }
      if variable == 'zos':
        continue
      print(f'-> Static vertical slice for "{variable}" variable.',
        file=sys.stderr)
      chart_builder.build_static(
        var_name=variable,
        x_dim_name='latitude',
        y_dim_name='depth',
        lat_dim_name='latitude',
        lon_dim_name='longitude',
        title=f'{plot_titles[variable]} on {date}',
        var_label=plot_measure_label[variable],
        y_label='Depth (m)',
        x_label='Latitude (°)',
        dim_constraints=dim_constraints
      )
      print(f'-> Image built.', file=sys.stderr)
      chart_builder.save(
        pathlib.Path(
          VISUALIZATIONS_DIR,
          f'vertical-slice-{plot_titles[variable]}'))
      print(f'-> Image saved', file=sys.stderr)
    
    print(f'Images stored in: {VISUALIZATIONS_DIR}', file=sys.stderr)
    print('Finishing test.', file=sys.stderr)
    time_end = time.time()
    print(f'----> Time elapsed: {time_end - time_start}s.', file=sys.stderr)
    self.assertTrue(True)

  
  def test_static_lon(self):
    print('\n--- Starting vertical slice for static image (longitude-). ---',
      file=sys.stderr)
    time_start = time.time()
    dataset_path = pathlib.Path(
      DATA_DIR,
      DATASET_NAME_2)
    dataset = xr.open_dataset(dataset_path)
    chart_builder = level_chart.VerticalSliceBuilder(
      dataset=dataset,
      verbose=True)

    date = '2020-01-01'
    for variable in variables:
      dim_constraints = {
        'time': date,
        'latitude': 20,
        'longitude': slice(-88, -76)
      }
      if variable == 'zos':
        continue
      print(f'-> Static vertical slice for "{variable}" variable.',
        file=sys.stderr)
      chart_builder.build_static(
        var_name=variable,
        x_dim_name='longitude',
        y_dim_name='depth',
        lat_dim_name='latitude',
        lon_dim_name='longitude',
        title=f'{plot_titles[variable]} on {date}',
        var_label=plot_measure_label[variable],
        y_label='Depth (m)',
        x_label='Longitude (°)',
        dim_constraints=dim_constraints
      )
      print(f'-> Image built.', file=sys.stderr)
      chart_builder.save(
        pathlib.Path(
          VISUALIZATIONS_DIR,
          f'vertical-slice-{plot_titles[variable]}-lon'))
      print(f'-> Image saved', file=sys.stderr)
    
    print(f'Images stored in: {VISUALIZATIONS_DIR}', file=sys.stderr)
    print('Finishing test.', file=sys.stderr)
    time_end = time.time()
    print(f'----> Time elapsed: {time_end - time_start}s.', file=sys.stderr)
    self.assertTrue(True)
  

  def test_animated(self):
    print('\n--- Starting vertical slice for animated image. ---',
      file=sys.stderr)
    time_start = time.time()
    dataset_path = pathlib.Path(
      DATA_DIR,
      DATASET_NAME_2)
    dataset = xr.open_dataset(dataset_path)
    chart_builder = level_chart.VerticalSliceBuilder(
      dataset=dataset,
      verbose=True)

    for variable in variables:
      dim_constraints = {
        'latitude': slice(15, 27),
        'longitude': -85
      }
      if variable == 'zos':
        continue
      print(f'-> Animated vertical slice for "{variable}" variable.',
        file=sys.stderr)
      chart_builder.build_animation(
        var_name=variable,
        x_dim_name='latitude',
        y_dim_name='depth',
        time_dim_name='time',
        lat_dim_name='latitude',
        lon_dim_name='longitude',
        title=f'{plot_titles[variable]}',
        var_label=plot_measure_label[variable],
        y_label='Depth (m)',
        x_label='Latitude (°)',
        dim_constraints=dim_constraints,
        duration=5,
        duration_unit='FRAMES_PER_SECOND',
      )
      print(f'-> Image built.', file=sys.stderr)
      chart_builder.save(
        pathlib.Path(
          VISUALIZATIONS_DIR,
          f'vertical-slice-{plot_titles[variable]}-ANIMATION.gif'))
      print(f'-> Image saved', file=sys.stderr)
    
    print(f'Images stored in: {VISUALIZATIONS_DIR}', file=sys.stderr)
    print('Finishing test.', file=sys.stderr)
    time_end = time.time()
    print(f'----> Time elapsed: {time_end - time_start}s.', file=sys.stderr)
    self.assertTrue(True)
  

  def test_animated_lon(self):
    print('\n--- Starting vertical slice for animated image (longitude-). ---',
      file=sys.stderr)
    time_start = time.time()
    dataset_path = pathlib.Path(
      DATA_DIR,
      DATASET_NAME_2)
    dataset = xr.open_dataset(dataset_path)
    chart_builder = level_chart.VerticalSliceBuilder(
      dataset=dataset,
      verbose=True)

    for variable in variables:
      dim_constraints = {
        'latitude': 20,
        'longitude': slice(-88, -76)
      }
      if variable == 'zos':
        continue
      print(f'-> Animated vertical slice for "{variable}" variable.',
        file=sys.stderr)
      chart_builder.build_animation(
        var_name=variable,
        x_dim_name='longitude',
        y_dim_name='depth',
        time_dim_name='time',
        lat_dim_name='latitude',
        lon_dim_name='longitude',
        title=f'{plot_titles[variable]}',
        var_label=plot_measure_label[variable],
        y_label='Depth (m)',
        x_label='Longitude (°)',
        dim_constraints=dim_constraints,
        duration=5,
        duration_unit='FRAMES_PER_SECOND',
      )
      print(f'-> Image built.', file=sys.stderr)
      chart_builder.save(
        pathlib.Path(
          VISUALIZATIONS_DIR,
          f'vertical-slice-{plot_titles[variable]}-ANIMATION-lon.gif'))
      print(f'-> Image saved', file=sys.stderr)
    
    print(f'Images stored in: {VISUALIZATIONS_DIR}', file=sys.stderr)
    print('Finishing test.', file=sys.stderr)
    time_end = time.time()
    print(f'----> Time elapsed: {time_end - time_start}s.', file=sys.stderr)
    self.assertTrue(True)


if __name__ == '__main__':
  general_utils.mkdir_r(VISUALIZATIONS_DIR)
  unittest.main()
