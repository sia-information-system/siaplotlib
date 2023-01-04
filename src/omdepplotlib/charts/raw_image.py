import io
import sys
import pathlib
import omdepplotlib.charts.interfaces as chart_interfaces


class RawImage(chart_interfaces.ChartInterface):
  def __init__(
    self,
    img_source,
    verbose: bool = False
  ) -> None:
    self.__img_buff = None
    self.__img_path = None
    self.verbose = verbose
    if type(img_source) is io.BytesIO:
      self.__img_buff = img_source
      print('Setting image buffer', file=sys.stderr)
    else:
      # Read from disk
      print('Buffer not set', file=sys.stderr)
  

  def get_buffer(self):
    return self.__img_buff
  

  def save(
    self,
    filepath: str | pathlib.Path
  ) -> None:
    with open(filepath, "wb") as f:
      f.write(self.get_buffer().getbuffer())
      if self.verbose:
        print(f'Image saved in: {filepath}', file=sys.stderr)


class ChartImage(RawImage):
  def __init__(
    self,
    img_source,
    var_name, 
    title, 
    lon_interval=[], 
    lat_interval=[],
    var_label=None,
    verbose=False
  ) -> None:
    super().__init__(
      img_source=img_source,
      verbose=verbose)
    self.var_name = var_name
    self.title = title
    self.lon_interval = lon_interval
    self.lat_interval = lat_interval
    self.var_label = var_label
