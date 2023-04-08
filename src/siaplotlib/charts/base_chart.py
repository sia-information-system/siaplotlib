# Standard
import sys
import io
import pathlib
# Third party
import matplotlib.pyplot as plt
# Own
from siaplotlib.charts.interfaces import ChartInterface
from siaplotlib.utils.log import LoggingFeatures


class Chart(ChartInterface, LoggingFeatures):
  def __init__(
    self,
    fig = None,
    fig_path = None,
    log_stream = sys.stderr,
    verbose = False
  ) -> None:
    # Super classes
    LoggingFeatures.__init__(self, log_stream=log_stream, verbose=verbose)
    # Own members.
    self._fig = fig
    self._fig_path = fig_path


  def plot(self) -> None:
    if self._fig is None:
      # TODO: Raise and appropriate exception class.
      raise RuntimeError('Pyplot figure has not been created.')
    self._fig.show()
  

  def save(
    self,
    filepath: str | pathlib.Path
  ) -> None:
    if self._fig is None:
      # TODO: Raise and appropriate exception class.
      raise RuntimeError('Pyplot figure has not been created.')
  
    self._fig.savefig(filepath, dpi=100, bbox_inches='tight')
    self._fig_path = filepath
    self.log(f'Image saved in: {filepath}')
  

  def close(self) -> None:
    if self._fig is not None:
      self.log('Closing pyplot figure.')
      plt.close(self._fig)
      self._fig = None
  

  def get_buffer(self) -> io.BytesIO:
    img_buff = io.BytesIO()
    self._fig.savefig(img_buff, dpi=100, bbox_inches='tight')
    return img_buff
  

  def __del__(self):
    self.log('Free chart.')
    self.close()
