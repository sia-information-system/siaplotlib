import io
import pathlib


class ChartInterface:
  def plot(self):
    raise NotImplementedError('ChartInterface: This is a virtual method.')


  def save(self, filepath: str | pathlib.Path):
    raise NotImplementedError('ChartInterface: This is a virtual method.')


  def close(self):
    raise NotImplementedError('ChartInterface: This is a virtual method.')


  def get_buffer(self) -> io.BytesIO:
    raise NotImplementedError('ChartInterface: This is a virtual method.')
