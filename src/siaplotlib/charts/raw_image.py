import io
import sys
import pathlib
import siaplotlib.charts.interfaces as chart_interfaces
from siaplotlib.utils.log import LoggingFeatures


class RawImage(chart_interfaces.ChartInterface, LoggingFeatures):
  def __init__(
    self,
    img_source,
    log_stream = sys.stderr,
    verbose: bool = False
  ) -> None:
    LoggingFeatures.__init__(self, log_stream=log_stream, verbose=verbose)
    self._img_buff = None
    self._img_path = None
    if type(img_source) is io.BytesIO:
      self._img_buff = img_source
      self.log('Setting image buffer')
    else:
      # Read from disk
      self.log('Buffer not set')
  

  def get_buffer(self):
    return self._img_buff
  

  def close(self) -> None:
    self.log('Dropping image buffer reference.')
    self._img_buff = None
  

  def save(
    self,
    filepath: str | pathlib.Path
  ) -> None:
    with open(filepath, "wb") as f:
      f.write(self.get_buffer().getbuffer())
      self.log(f'Image saved in: {filepath}')


class ChartImage(RawImage):
  def __init__(
    self,
    img_source,
    var_name, 
    title, 
    lon_interval=[], 
    lat_interval=[],
    var_label=None,
    log_stream = sys.stderr,
    verbose=False
  ) -> None:
    super().__init__(
      img_source=img_source,
      log_stream=log_stream,
      verbose=verbose)
    self.var_name = var_name
    self.title = title
    self.lon_interval = lon_interval
    self.lat_interval = lat_interval
    self.var_label = var_label