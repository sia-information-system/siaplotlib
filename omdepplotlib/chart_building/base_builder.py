from omdepplotlib.charts.interfaces import ChartInterface
import xarray as xr
import numpy as np
from PIL import Image
import pathlib
import sys
import io


class ChartBuilder:
  # Public methods.

  def __init__(
    self,
    dataset: xr.DataArray,
    verbose: bool = False
  ) -> None:
    self._chart: ChartInterface = None
    self.dataset = dataset
    self.verbose = verbose


  def save(
    self,
    filepath: str | pathlib.Path
  ) -> None:
    self._chart.save(filepath)

  # Private Methods.

  def _make_gif(
    self,
    charts: list,
    duration: float = 0.5,
    duration_unit: str = 'SECONDS_PER_FRAME'
  ) -> io.BytesIO:
    if self.verbose:
      print('Making gif.', file=sys.stderr)
    
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
    if self.verbose:
      print(f'Gif created.', file=sys.stderr)
    return img_buff
