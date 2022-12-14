import io
import sys

class RawImage:
  def __init__(
    self,
    img_source):
      self.__img_buff = None
      self.__img_path = None
      if type(img_source) is io.BytesIO:
        self.__img_buff = img_source
        print('Setting image buffer', file=sys.stderr)
      else:
        print('Not buffer set', file=sys.stderr)
  

  def get_img_buff(self):
    return self.__img_buff


class ChartImage(RawImage):
  def __init__(
    self,
    img_source,
    var, 
    title, 
    lon_interval=[], 
    lat_interval=[],
    label=None,
    verbose=False):
      super().__init__(img_source)
      self.var = var
      self.title = title
      self.lon_interval = lon_interval
      self.lat_interval = lat_interval
      self.label = label
      self.verbose = verbose
