# Standard
import io
import sys
from pathlib import Path
from collections.abc import Callable
# Third party
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
# Own
from siaplotlib.charts.interfaces import ChartInterface
from siaplotlib.chart_building.interfaces import ChartBuilderInterface
from siaplotlib.processing.parallelism import AsyncRunner, AsyncRunnerManager
from siaplotlib.utils.log import LoggingFeatures, LogStream

# TODO: Analysis if should I make clasess for a single type of graphic and have
# a single method ".build()". It would mean that will have separated clases for static
# and animated (gif) charts.


class ChartBuilder(ChartBuilderInterface, LoggingFeatures):
  def __init__(
    self,
    dataset: xr.DataArray,
    log_stream = sys.stderr,
    verbose: bool = False
  ) -> None:
    # Super class constructors.
    LoggingFeatures.__init__(self, log_stream=log_stream, verbose=verbose)
    # Own attributes.
    self._chart: ChartInterface = None
    self.dataset = dataset
    # Async processes
    self.async_runner_manager = AsyncRunnerManager()
    self.async_runner_manager.add_runner('build', AsyncRunner(sync_fn=self.sync_build))


  def save(
    self,
    filepath: str | Path
  ) -> None:
    self._chart.save(filepath)


  def _make_gif(
    self,
    charts: list,
    duration: float = 0.5,
    duration_unit: str = 'SECONDS_PER_FRAME'
  ) -> io.BytesIO:
    self.log('Making gif.')
    
    frame_duration = None
    if duration_unit == 'SECONDS_PER_FRAME':
      frame_duration = np.round(duration * 1000)
    elif duration_unit == 'FRAMES_PER_SECOND':
      frame_duration = np.round(1000 / duration)
    else:
      raise RuntimeError(f'Unit "{duration_unit}" is not supported.')
    
    img_buff = io.BytesIO()
    frames = [Image.open(chart.get_buffer()) for chart in charts]
    frame_one = frames.pop(0)
    frames.append(frames[-1]) # Duplicate last frame to simulate a small stop at the end.
    # Image docs: https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.Image.save
    # GIF docs: https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#gif
    # Durations is defined in milliseconds.
    frame_one.save(
      img_buff, format='GIF', append_images=frames,
      save_all=True, duration=frame_duration, loop=0)
    # Closes all file and destroys the core images object.
    frame_one.close()
    for frame in frames:
        frame.close()
    self.log('Gif created.')
    return img_buff
  

  def build(
    self,
    success_callback: Callable[[], None],
    failure_callback: Callable[[Exception], None]
  ):
    # Links about whis statement:
    # 1: https://stackoverflow.com/questions/49921721/runtimeerror-main-thread-is-not-in-main-loop-with-matplotlib-and-flask
    # 2: https://stackoverflow.com/questions/14694408/runtimeerror-main-thread-is-not-in-main-loop
    # 3: https://stackoverflow.com/questions/10556479/running-a-tkinter-form-in-a-separate-thread/10556698#10556698
    # 4: https://stackoverflow.com/questions/27147300/matplotlib-tcl-asyncdelete-async-handler-deleted-by-the-wrong-thread
    plt.switch_backend('agg')
    runner = self.async_runner_manager.get_runner('build')
    runner.success_callback = success_callback
    runner.failure_callback = failure_callback
    runner.run()
  

  def close(self):
    if self._chart is not None:
      self.log('Closing builder.')
      self._chart.close()
      self._chart = None
  

  def wait(self, seconds: float = None):
    self.async_runner_manager.get_runner('build').wait(seconds=seconds)
  

  def still_working(self):
    return self.async_runner_manager.get_runner('build').still_working()
  

  def __del__(self):
    self.log('Free builder.')
    self.close()
