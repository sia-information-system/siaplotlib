# Standard
import io
import sys
from pathlib import Path
# Third party
from PIL import Image
# Own
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
      # Just asign the buffer
      self._img_buff = img_source
      self.log('Setting image buffer')
    elif type(img_source) is str or type(img_source) is Path or issubclass(type(img_source), Path):
      # Read from disk and convert to a buffered stream.
      self._img_buff = io.BytesIO()
      img = Image.open(img_source)
      img.save(self._img_buff, format='PNG')
      img.close()
    else:
      raise RuntimeError(f'img_source is {type(img_source)} and must be: BytesIO | Path | str')
  

  def get_buffer(self):
    return self._img_buff
  

  def close(self) -> None:
    self.log('Dropping image buffer reference.')
    self._img_buff = None
  

  def save(
    self,
    filepath: str | Path
  ) -> None:
    with open(filepath, "wb") as f:
      # f.write(self.get_buffer().getbuffer())
      fname_splited = str(filepath).split('.')
      if fname_splited[-1].lower() not in { 'png', 'jpg', 'jpeg', 'gif' }:
        filepath = str(filepath) + '.png'
      img = Image.open(self.get_buffer())
      img.save(filepath, format='PNG')
      img.close()
      self.log(f'Image saved in: {filepath}')


class ChartImage(RawImage):
  def __init__(
    self,
    img_source,
    var_name = '', 
    title = '', 
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
