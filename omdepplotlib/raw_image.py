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
    limit_coord_lon=[-90, -80], 
    limit_coord_lat=[10, 30],
    has_legend=True,
    name_legend='',
    verbose=True):
      super().__init__(img_source)
      self.var = var
      self.title = title
      self.limit_coord_lon = limit_coord_lon
      self.limit_coord_lat = limit_coord_lat
      self.has_legend = has_legend
      self.name_legend = name_legend
      self.verbose = verbose
