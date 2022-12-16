from omdepplotlib.charts.interfaces import ChartInterface
import matplotlib.pyplot as plt
import sys
import io
import pathlib


class Chart(ChartInterface):
  def __init__(
    self,
    fig = None,
    fig_path = None,
    verbose = False) -> None:
      self._fig = fig
      self._fig_path = fig_path
      self.verbose = verbose
      pass


  def plot(self):
    if self._fig is None:
      # TODO: Raise and appropriate exception class.
      raise RuntimeError('Heatmap figure has not been created.')
    self._fig.show()
  

  def save(self, filepath: str | pathlib.Path):
    if self._fig is None:
      # TODO: Raise and appropriate exception class.
      raise RuntimeError('Heatmap figure has not been created.')
  
    self._fig.savefig(filepath, dpi=100, bbox_inches='tight')
    self._fig_path = filepath
    if self.verbose:
      print(f'Image saved in: {filepath}', file=sys.stderr)
  

  def close(self):
    if self._fig is not None:
      if self.verbose:
        print('Closing pyplot figure.', file=sys.stderr)
      plt.close(self._fig)
      self._fig = None
  

  def get_buffer(self) -> io.BytesIO:
    img_buff = io.BytesIO()
    self._fig.savefig(img_buff, dpi=100, bbox_inches='tight')
    return img_buff
  
  
  def build(self):
    raise NotImplementedError('This is a virtual method.')
