# Standard
import pathlib
import sys
import unittest
import time
# Third party
import xarray as xr
# Own
from siaplotlib.chart_building import level_chart, line_chart
from siaplotlib.chart_building.base_builder import ChartBuilder
from siaplotlib.utils.log import LogStream
from siaplotlib.charts.raw_image import ChartImage
# For testing
from lib_utils.general_utils import VISUALIZATIONS_DIR, DATA_DIR
import lib_utils.general_utils as general_utils

log_stream = LogStream(callback= lambda s: print(s, end='', file=sys.stderr))
# Setup

DATASET_NAME_1 = 'global-analysis-forecast-phy-001-024-GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS-date-2022-11-13-time-10h-31m-10s-857022ms.nc'
DATASET_NAME_2 = 'global-analysis-forecast-phy-001-024-GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS-date-2022-11-13-time-13h-27m-31s-211639ms-monthly.nc'
general_utils.mkdir_r(VISUALIZATIONS_DIR)

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

#Dimensions names
lon_dim_name = 'longitude'
lat_dim_name = 'latitude'
depth_name = 'depth'
time_dim_name = 'time'


class ChartBuilderTestCase(unittest.TestCase):
  def __init__(self, methodName: str = "runTest") -> None:
    super().__init__(methodName)
    self.chart_filepath: pathlib.Path | str = '__filepath__'
    self.process_ok = False

  def success_build_callback(self, chart_builder: ChartBuilder, subset: xr.Dataset):
    print(f'-> Image built.', file=sys.stderr)
    chart_builder.save(self.chart_filepath)
    print(f'-> Image saved', file=sys.stderr)
    chart_builder.close()
    self.process_ok = True
    # del chart_builder

  def success_build_nodataset_callback(self, chart_builder: ChartBuilder):
    print(f'-> Image built.', file=sys.stderr)
    chart_builder.save(self.chart_filepath)
    print(f'-> Image saved', file=sys.stderr)
    chart_builder.close()
    self.process_ok = True


  def failure_build_callback(self, err: BaseException):
    print('--- An error ocurr while building the chart. ---', file=sys.stderr)
    print(err, file=sys.stderr)
    self.process_ok = False

# Test definitions.
class TestArrowChart(ChartBuilderTestCase):
   def test_images(self):
    self.process_ok = False
    print('\n--- Starting ArrowChart static images test. ---',
      file=sys.stderr)
    time_start = time.time()
    dataset_path = pathlib.Path(
      DATA_DIR,
      DATASET_NAME_1)
    dataset = xr.open_dataset(dataset_path)

    #min,max,jump
    depth = 0
    target_date = '2022-10-11'
    northward_var_name = 'vo'
    eastward_var_name = 'uo'
    title = 'ArrowChart'

    grouping_level = 5

    dim_constraints = {
        time_dim_name
: [target_date],
        depth_name: depth,
        lat_dim_name : slice(10, 30),
        lon_dim_name: slice(-90, -80)
      }
    
    self.chart_filepath = pathlib.Path(VISUALIZATIONS_DIR, f'ArrowChart')
    chart_builder = line_chart.StaticArrowChartBuilder(
      dataset = dataset,
      eastward_var_name = eastward_var_name,
      northward_var_name = northward_var_name,
      lat_dim_name = lat_dim_name ,
      lon_dim_name = lon_dim_name,
      depth_dim_name = depth_name,
      grouping_level = grouping_level,
      title = title,
      var_label='Velocidad (m/s)',
      time_dim_name = time_dim_name,
      dim_constraints = dim_constraints,
      log_stream=log_stream,
      verbose=True)
    chart_builder.build(success_callback=self.success_build_callback, failure_callback=self.failure_build_callback)
    chart_builder.wait() 
    self.assertTrue(self.process_ok)

    print('Finishing test.', file=sys.stderr)
    time_end = time.time()
    print(f'----> Time elapsed: {time_end - time_start}s.', file=sys.stderr)

class TestRegionMap(ChartBuilderTestCase):
  def test_images(self):
    self.process_ok = False
    print('\n--- Starting RegionMapChart static images test. ---',
      file=sys.stderr)
    time_start = time.time()

    # Max siempre debe ser mayor que min. 
    lat_max = 13.14
    lat_min = 11.42
    lon_min = 51.80
    lon_max = 54.97
    amplitud = 1

    self.chart_filepath = pathlib.Path(VISUALIZATIONS_DIR, f'MapRegion')
    chart_builder = line_chart.StaticRegionMapBuilder(
        amplitude = amplitud,
        lon_dim_min = lon_min,
        lon_dim_max = lon_max,
        lat_dim_min = lat_min,
        lat_dim_max = lat_max,
        log_stream=log_stream,
        verbose=True)
    chart_builder.build(success_callback=self.success_build_nodataset_callback, failure_callback=self.failure_build_callback)
    chart_builder.wait() 
    self.assertTrue(self.process_ok)

    print('Finishing test.', file=sys.stderr)
    time_end = time.time()
    print(f'----> Time elapsed: {time_end - time_start}s.', file=sys.stderr)


class TestWindRose(ChartBuilderTestCase):
   def test_images(self):
    self.process_ok = False
    print('\n--- Starting WindRose static images test. ---',
      file=sys.stderr)
    time_start = time.time()
    dataset_path = pathlib.Path(
      DATA_DIR,
      DATASET_NAME_1)
    dataset = xr.open_dataset(dataset_path)

    #min,max,jumps
    bin_min = 1
    bin_max = 2
    bin_jmp = 0.2

    nsector = 16 
    depth = 0
    target_date = '2022-10-11'
    northward_var_name = 'vo'
    eastward_var_name = 'uo'
    title = 'Windrose'

    dim_constraints = {
        time_dim_name
: [target_date],
        depth_name: depth,
        lat_dim_name : slice(15, 20),
        lon_dim_name: slice(-85, 82)
      }
    
    self.chart_filepath = pathlib.Path(VISUALIZATIONS_DIR, f'WindRose')
    chart_builder = level_chart.StaticWindRoseBuilder(
      dataset = dataset,
      eastward_var_name = eastward_var_name,
      northward_var_name = northward_var_name,
      lat_dim_name = lat_dim_name ,
      lon_dim_name = lon_dim_name,
      depth_dim_name=depth_name,
      title = title,
      bin_min = bin_min,
      bin_max = bin_max,
      bin_jmp = bin_jmp,
      color_palette = 'viridis',
      dim_constraints = dim_constraints,
      nsector = nsector,
      log_stream=log_stream,
      verbose=True)
    chart_builder.build(success_callback=self.success_build_callback, failure_callback=self.failure_build_callback)
    chart_builder.wait() 

    self.assertTrue(self.process_ok)
    print('Finishing test.', file=sys.stderr)
    time_end = time.time()
    print(f'----> Time elapsed: {time_end - time_start}s.', file=sys.stderr)


class TestHeatMap(ChartBuilderTestCase):
  def test_images(self):
    self.process_ok = False
    print('\n--- Starting heatmap static images test. ---',
      file=sys.stderr)
    time_start = time.time()
    dataset_path = pathlib.Path(
      DATA_DIR,
      DATASET_NAME_1)
    dataset = xr.open_dataset(dataset_path)
    
    target_date = '2022-10-11'

    for variable in variables:
      dim_constraints = {
        time_dim_name
: [target_date],
        depth_name: [0.49402499198913574]
      }
      if variable == 'zos':
        dim_constraints = {
          time_dim_name
: [target_date]
        }
      print(f'-> Heatmap static image for "{variable}" variable.',
        file=sys.stderr)
      self.chart_filepath = pathlib.Path(VISUALIZATIONS_DIR, f'heatmap-{plot_titles[variable]}')
      chart_builder = level_chart.StaticHeatMapBuilder(
        dataset=dataset,
        var_name=variable,
        title=f'{plot_titles[variable]} {target_date}',
        var_label=plot_measure_label[variable],
        dim_constraints=dim_constraints,
        lat_dim_name=lat_dim_name,
        lon_dim_name= lon_dim_name,
        color_palette=palette_colors[variable],
        log_stream=log_stream,
        verbose=True)
      chart_builder.build(success_callback=self.success_build_callback, failure_callback=self.failure_build_callback)
      chart_builder.wait() # Awaits untill the .build() async call ends.

    self.assertTrue(self.process_ok)    
    print(f'Images stored in: {VISUALIZATIONS_DIR}', file=sys.stderr)
    print('Finishing test.', file=sys.stderr)
    time_end = time.time()
    print(f'----> Time elapsed: {time_end - time_start}s.', file=sys.stderr)


  def test_gifs(self):
    self.process_ok = False
    print('\n--- Starting heatmap gifs test. ---', file=sys.stderr)
    time_start = time.time()

    dataset_path = pathlib.Path(
      DATA_DIR,
      DATASET_NAME_2)
    dataset = xr.open_dataset(dataset_path)
    
    for variable in variables:
      print(f'-> Heatmap gif for "{variable}" variable.',
        file=sys.stderr)
      dim_constraints = {
        depth_name: [0.49402499198913574]
      }
      if variable == 'zos':
        dim_constraints = {}
      chart_builder = level_chart.AnimatedHeatMapBuilder(
        dataset=dataset,
        var_name=variable,
        title=plot_titles[variable],
        var_label=plot_measure_label[variable],
        dim_constraints=dim_constraints,
        time_dim_name=time_dim_name
,
        lat_dim_name=lat_dim_name,
        lon_dim_name=lon_dim_name,
        duration=5,
        duration_unit='FRAMES_PER_SECOND',
        color_palette=palette_colors[variable],
        verbose=True)
      
      self.chart_filepath = pathlib.Path(VISUALIZATIONS_DIR,f'heatmap-{plot_titles[variable]}-ANIMATION.gif')
      chart_builder.build(success_callback=self.success_build_callback, failure_callback=self.failure_build_callback)
      chart_builder.wait() # Awaits untill the .build() async call ends.

    self.assertTrue(self.process_ok)
    print(f'Gifs stored in: {VISUALIZATIONS_DIR}', file=sys.stderr)
    print('Finishing test.', file=sys.stderr)
    time_end = time.time()
    print(f'----> Time elapsed: {time_end - time_start}s.', file=sys.stderr)


class TestContourMap(ChartBuilderTestCase):
  def test_images(self):
    self.process_ok = False
    print('\n--- Starting contour map static images test. ---', file=sys.stderr)
    time_start = time.time()
    dataset_path = pathlib.Path(
      DATA_DIR,
      DATASET_NAME_1)
    dataset = xr.open_dataset(dataset_path)

    target_date = '2022-10-11'
    for variable in variables:
      dim_constraints = {
        time_dim_name
: [target_date],
        depth_name: [0.49402499198913574]
      }
      if variable == 'zos':
        dim_constraints = {
          time_dim_name
: [target_date]
        }
      print(f'-> Contour map static image for "{variable}" variable.',
        file=sys.stderr)
      chart_builder = level_chart.StaticContourMapBuilder(
        dataset=dataset,
        var_name=variable,
        title=f'{plot_titles[variable]} {target_date}',
        var_label=plot_measure_label[variable],
        dim_constraints=dim_constraints,
        lat_dim_name=lat_dim_name,
        lon_dim_name=lon_dim_name,
        color_palette=palette_colors[variable],
        num_levels=9,
        verbose=True)
      self.chart_filepath = pathlib.Path(VISUALIZATIONS_DIR, f'contourmap-{plot_titles[variable]}')
      chart_builder.build(success_callback=self.success_build_callback, failure_callback=self.failure_build_callback)
      chart_builder.wait()
    
    self.assertTrue(self.process_ok)
    print(f'Images stored in: {VISUALIZATIONS_DIR}', file=sys.stderr)
    print('Finishing test.', file=sys.stderr)
    time_end = time.time()
    print(f'----> Time elapsed: {time_end - time_start}s.', file=sys.stderr)
  

  def test_gifs(self):
    self.process_ok = False
    print('\n--- Starting contour map gifs test. ---', file=sys.stderr)
    time_start = time.time()

    dataset_path = pathlib.Path(
      DATA_DIR,
      DATASET_NAME_2)
    dataset = xr.open_dataset(dataset_path)

    for variable in variables:
      print(f'-> Contout map gif for "{variable}" variable.',
        file=sys.stderr)
      dim_constraints = {
        depth_name: [0.49402499198913574]
      }
      if variable == 'zos':
        dim_constraints = {}
      chart_builder = level_chart.AnimatedContourMapBuilder(
        dataset=dataset,
        var_name=variable,
        title=plot_titles[variable],
        var_label=plot_measure_label[variable],
        dim_constraints=dim_constraints,
        time_dim_name=time_dim_name
,
        lat_dim_name=lat_dim_name,
        lon_dim_name=lon_dim_name,
        duration=5,
        duration_unit='FRAMES_PER_SECOND',
        num_levels=9,
        color_palette=palette_colors[variable],
        verbose=True)
      self.chart_filepath = pathlib.Path(VISUALIZATIONS_DIR, f'contourmap-{plot_titles[variable]}-ANIMATION.gif')
      chart_builder.build(success_callback=self.success_build_callback, failure_callback=self.failure_build_callback)
      chart_builder.wait()
    
    self.assertTrue(self.process_ok)
    print(f'Gifs stored in: {VISUALIZATIONS_DIR}', file=sys.stderr)
    print('Finishing test.', file=sys.stderr)
    time_end = time.time()
    print(f'----> Time elapsed: {time_end - time_start}s.', file=sys.stderr)


class TestSinglePointTimeSeries(ChartBuilderTestCase):
  def test_many_depths(self):
    self.process_ok = False
    print('\n--- Starting time series static images test with many depths. ---',
      file=sys.stderr)
    time_start = time.time()
    dataset_path = pathlib.Path(
      DATA_DIR,
      DATASET_NAME_2)
    dataset = xr.open_dataset(dataset_path)

    date_range = slice('2020-01-01', '2020-12-01')
    for variable in variables:
      grouping_dim_name=depth_name
      dim_constraints = {
        time_dim_name
: date_range,
        depth_name: [0, 100, 250, 500, 1000],
        lat_dim_name: 21,
        lon_dim_name: -86
      }
      if variable == 'zos':
        dim_constraints = {
          time_dim_name
: date_range,
          lat_dim_name: 21,
          lon_dim_name: -86
        }
        grouping_dim_name=None
      print(f'-> Static single-point time-series image for "{variable}" variable.',
        file=sys.stderr)
      chart_builder = line_chart.SinglePointTimeSeriesBuilder(
        dataset=dataset,
        var_name=variable,
        title=f'{plot_titles[variable]} time series',
        grouping_dim_label='Depth (m)',
        dim_constraints=dim_constraints,
        lat_dim_name=lat_dim_name,
        lon_dim_name=lon_dim_name,
        grouping_dim_name=grouping_dim_name,
        time_dim_name=time_dim_name
,
        var_label=plot_measure_label[variable],
        time_dim_label='Dates',
        verbose=True)
      self.chart_filepath = pathlib.Path(VISUALIZATIONS_DIR,f'single-point-time-series-{plot_titles[variable]}')
      chart_builder.build(success_callback=self.success_build_callback, failure_callback=self.failure_build_callback)
      chart_builder.wait()

    self.assertTrue(self.process_ok)
    print(f'Images stored in: {VISUALIZATIONS_DIR}', file=sys.stderr)
    print('Finishing test.', file=sys.stderr)
    time_end = time.time()
    print(f'----> Time elapsed: {time_end - time_start}s.', file=sys.stderr)
  

  def test_single_depth(self):
    self.process_ok = False
    print('\n--- Starting time series static images test with single depth. ---',
      file=sys.stderr)
    time_start = time.time()
    dataset_path = pathlib.Path(
      DATA_DIR,
      DATASET_NAME_2)
    dataset = xr.open_dataset(dataset_path)

    date_range = slice('2020-01-01', '2020-12-01')
    for variable in variables:
      grouping_dim_name=depth_name
      dim_constraints = {
        time_dim_name
: date_range,
        depth_name: [0.49402499198913574],
        lat_dim_name: 21,
        lon_dim_name: -86
      }
      if variable == 'zos':
        dim_constraints = {
          time_dim_name
: date_range,
          lat_dim_name: 21,
          lon_dim_name: -86
        }
        grouping_dim_name=None
      print(f'-> Static single-point time-series image for "{variable}" variable.',
        file=sys.stderr)
      chart_builder = line_chart.SinglePointTimeSeriesBuilder(
        dataset=dataset,
        var_name=variable,
        title=f'{plot_titles[variable]} time series',
        grouping_dim_label='Depth (m)',
        dim_constraints=dim_constraints,
        lat_dim_name=lat_dim_name,
        lon_dim_name=lon_dim_name,
        grouping_dim_name=grouping_dim_name,
        time_dim_name=time_dim_name
,
        var_label=plot_measure_label[variable],
        time_dim_label='Dates',
        verbose=True)
      self.chart_filepath = pathlib.Path(VISUALIZATIONS_DIR,f'one-depth-single-point-time-series-{plot_titles[variable]}')
      chart_builder.build(success_callback=self.success_build_callback, failure_callback=self.failure_build_callback)
      chart_builder.wait()
    
    self.assertTrue(self.process_ok)
    print(f'Images stored in: {VISUALIZATIONS_DIR}', file=sys.stderr)
    print('Finishing test.', file=sys.stderr)
    time_end = time.time()
    print(f'----> Time elapsed: {time_end - time_start}s.', file=sys.stderr)


class TestSinglePointVerticalProfile(ChartBuilderTestCase):
  def test_many_dates(self):
    self.process_ok = False
    print('\n--- Starting time series static images test with many dates. ---',
      file=sys.stderr)
    time_start = time.time()
    dataset_path = pathlib.Path(
      DATA_DIR,
      DATASET_NAME_2)
    dataset = xr.open_dataset(dataset_path)

    date_range = ['2020-03-01', '2020-03-09', '2020-09-01', '2020-12-01']
    # date_range = ['2020-03-01', '2020-06-01', '2020-09-01', '2020-12-01']
    for variable in variables:
      grouping_dim_name=time_dim_name

      dim_constraints = {
        time_dim_name
: date_range,
        lat_dim_name: 21,
        lon_dim_name: -86
      }
      if variable == 'zos':
        continue
      print(f'-> Static single-point vertical profile image for "{variable}" variable.',
        file=sys.stderr)
      chart_builder = line_chart.SinglePointVerticalProfileBuilder(
        dataset=dataset,
        var_name=variable,
        title=f'{plot_titles[variable]} by depth',
        grouping_dim_label='Dates',
        dim_constraints=dim_constraints,
        lat_dim_name=lat_dim_name,
        lon_dim_name=lon_dim_name,
        grouping_dim_name=grouping_dim_name,
        y_dim_name=depth_name,
        y_dim_label='Depth',
        var_label=plot_measure_label[variable],
        verbose=True)
      self.chart_filepath = pathlib.Path(VISUALIZATIONS_DIR,f'single-point-vertical-profile-{plot_titles[variable]}')
      chart_builder.build(success_callback=self.success_build_callback, failure_callback=self.failure_build_callback)
      chart_builder.wait()
    
    self.assertTrue(self.process_ok)
    print(f'Images stored in: {VISUALIZATIONS_DIR}', file=sys.stderr)
    print('Finishing test.', file=sys.stderr)
    time_end = time.time()
    print(f'----> Time elapsed: {time_end - time_start}s.', file=sys.stderr)


class TestVerticalSlice(ChartBuilderTestCase):
  def test_static(self):
    self.process_ok = False
    print('\n--- Starting vertical slice for static image. ---',
      file=sys.stderr)
    time_start = time.time()
    dataset_path = pathlib.Path(
      DATA_DIR,
      DATASET_NAME_2)
    dataset = xr.open_dataset(dataset_path)

    date = '2020-01-01'
    for variable in variables:
      dim_constraints = {
        time_dim_name
: date,
        lat_dim_name: slice(15, 27),
        lon_dim_name: -85
      }
      if variable == 'zos':
        continue
      print(f'-> Static vertical slice for "{variable}" variable.',
        file=sys.stderr)
      chart_builder = level_chart.StaticVerticalSliceBuilder(
        dataset=dataset,
        var_name=variable,
        x_dim_name=lat_dim_name,
        y_dim_name=depth_name,
        lat_dim_name=lat_dim_name,
        lon_dim_name=lon_dim_name,
        title=f'{plot_titles[variable]} on {date}',
        var_label=plot_measure_label[variable],
        y_label='Depth (m)',
        x_label='Latitude (°)',
        dim_constraints=dim_constraints,
        verbose=True)
      self.chart_filepath = pathlib.Path(VISUALIZATIONS_DIR,f'vertical-slice-{plot_titles[variable]}')
      chart_builder.build(success_callback=self.success_build_callback, failure_callback=self.failure_build_callback)
      chart_builder.wait()
    
    self.assertTrue(self.process_ok)
    print(f'Images stored in: {VISUALIZATIONS_DIR}', file=sys.stderr)
    print('Finishing test.', file=sys.stderr)
    time_end = time.time()
    print(f'----> Time elapsed: {time_end - time_start}s.', file=sys.stderr)

  
  def test_static_lon(self):
    self.process_ok = False
    print('\n--- Starting vertical slice for static image (longitude-). ---',
      file=sys.stderr)
    time_start = time.time()
    dataset_path = pathlib.Path(
      DATA_DIR,
      DATASET_NAME_2)
    dataset = xr.open_dataset(dataset_path)

    date = '2020-01-01'
    for variable in variables:
      dim_constraints = {
        time_dim_name
: date,
        lat_dim_name: 20,
        lon_dim_name: slice(-88, -76)
      }
      if variable == 'zos':
        continue
      print(f'-> Static vertical slice for "{variable}" variable.',
        file=sys.stderr)
      chart_builder = level_chart.StaticVerticalSliceBuilder(
        dataset=dataset,
        var_name=variable,
        x_dim_name=lon_dim_name,
        y_dim_name=depth_name,
        lat_dim_name=lat_dim_name,
        lon_dim_name=lon_dim_name,
        title=f'{plot_titles[variable]} on {date}',
        var_label=plot_measure_label[variable],
        y_label='Depth (m)',
        x_label='Longitude (°)',
        dim_constraints=dim_constraints,
        verbose=True)
      self.chart_filepath = pathlib.Path(VISUALIZATIONS_DIR,f'vertical-slice-{plot_titles[variable]}-lon')
      chart_builder.build(success_callback=self.success_build_callback, failure_callback=self.failure_build_callback)
      chart_builder.wait()
    
    self.assertTrue(self.process_ok)
    print(f'Images stored in: {VISUALIZATIONS_DIR}', file=sys.stderr)
    print('Finishing test.', file=sys.stderr)
    time_end = time.time()
    print(f'----> Time elapsed: {time_end - time_start}s.', file=sys.stderr)
  

  def test_animated(self):
    self.process_ok = False
    print('\n--- Starting vertical slice for animated image. ---',
      file=sys.stderr)
    time_start = time.time()
    dataset_path = pathlib.Path(
      DATA_DIR,
      DATASET_NAME_2)
    dataset = xr.open_dataset(dataset_path)

    for variable in variables:
      dim_constraints = {
        lat_dim_name: slice(15, 27),
        lon_dim_name: -85
      }
      if variable == 'zos':
        continue
      print(f'-> Animated vertical slice for "{variable}" variable.',
        file=sys.stderr)
      chart_builder = level_chart.AnimatedVerticalSliceBuilder(
        dataset=dataset,
        var_name=variable,
        x_dim_name=lat_dim_name,
        y_dim_name=depth_name,
        time_dim_name=time_dim_name
,
        lat_dim_name=lat_dim_name,
        lon_dim_name=lon_dim_name,
        title=f'{plot_titles[variable]}',
        var_label=plot_measure_label[variable],
        y_label='Depth (m)',
        x_label='Latitude (°)',
        dim_constraints=dim_constraints,
        duration=5,
        duration_unit='FRAMES_PER_SECOND',
        verbose=True)
      self.chart_filepath = pathlib.Path(VISUALIZATIONS_DIR,f'vertical-slice-{plot_titles[variable]}-ANIMATION.gif')
      chart_builder.build(success_callback=self.success_build_callback, failure_callback=self.failure_build_callback)
      chart_builder.wait()
    
    self.assertTrue(self.process_ok)
    print(f'Images stored in: {VISUALIZATIONS_DIR}', file=sys.stderr)
    print('Finishing test.', file=sys.stderr)
    time_end = time.time()
    print(f'----> Time elapsed: {time_end - time_start}s.', file=sys.stderr)
  

  def test_animated_lon(self):
    self.process_ok = False
    print('\n--- Starting vertical slice for animated image (longitude-). ---',
      file=sys.stderr)
    time_start = time.time()
    dataset_path = pathlib.Path(
      DATA_DIR,
      DATASET_NAME_2)
    dataset = xr.open_dataset(dataset_path)

    for variable in variables:
      dim_constraints = {
        lat_dim_name: 20,
        lon_dim_name: slice(-88, -76)
      }
      if variable == 'zos':
        continue
      print(f'-> Animated vertical slice for "{variable}" variable.',
        file=sys.stderr)
      chart_builder = level_chart.AnimatedVerticalSliceBuilder(
        dataset=dataset,
        var_name=variable,
        x_dim_name=lon_dim_name,
        y_dim_name=depth_name,
        time_dim_name=time_dim_name
,
        lat_dim_name=lat_dim_name,
        lon_dim_name=lon_dim_name,
        title=f'{plot_titles[variable]}',
        var_label=plot_measure_label[variable],
        y_label='Depth (m)',
        x_label='Longitude (°)',
        dim_constraints=dim_constraints,
        duration=5,
        duration_unit='FRAMES_PER_SECOND',
        verbose=True)
      self.chart_filepath = pathlib.Path(VISUALIZATIONS_DIR,f'vertical-slice-{plot_titles[variable]}-ANIMATION-lon.gif')
      chart_builder.build(success_callback=self.success_build_callback, failure_callback=self.failure_build_callback)
      chart_builder.wait()
    
    self.assertTrue(self.process_ok)
    print(f'Images stored in: {VISUALIZATIONS_DIR}', file=sys.stderr)
    print('Finishing test.', file=sys.stderr)
    time_end = time.time()
    print(f'----> Time elapsed: {time_end - time_start}s.', file=sys.stderr)


class TestRestoreChartBuilders(ChartBuilderTestCase):
  def test_restore_chart_builder(self):
    print('\n--- Starting test for builder restoring (png). ---',
      file=sys.stderr)
    img_path = pathlib.Path(DATA_DIR, 'time-series.png')
    chart_builder = ChartBuilder(
      dataset=None,
      log_stream=sys.stderr,
      verbose=True)
    chart_image = ChartImage(
      img_source=img_path,
      verbose=chart_builder.verbose,
      log_stream=chart_builder.log_stream)
    chart_builder._chart = chart_image
    chart_builder.save(pathlib.Path(VISUALIZATIONS_DIR, 'restored_image.png'))
  

  def test_restore_chart_builder_gif(self):
    print('\n--- Starting test for builder restoring (gif). ---',
      file=sys.stderr)
    img_path = pathlib.Path(DATA_DIR, 'heatmap.gif')
    chart_builder = ChartBuilder(
      dataset=None,
      log_stream=sys.stderr,
      verbose=True)
    chart_image = ChartImage(
      img_source=img_path,
      verbose=chart_builder.verbose,
      log_stream=chart_builder.log_stream)
    chart_builder._chart = chart_image
    chart_builder.save(pathlib.Path(VISUALIZATIONS_DIR, 'restored_image.gif'))


if __name__ == '__main__':
  unittest.main()
