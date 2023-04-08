import io
import pathlib


class ChartInterface:
  def plot(self) -> None:
    raise NotImplementedError('ChartInterface: This is a virtual method.')


  def save(self, filepath: str | pathlib.Path) -> None:
    raise NotImplementedError('ChartInterface: This is a virtual method.')


  def close(self) -> None:
    raise NotImplementedError('ChartInterface: This is a virtual method.')


  def get_buffer(self) -> io.BytesIO:
    raise NotImplementedError('ChartInterface: This is a virtual method.')
  

  def build(self):
    raise NotImplementedError('ChartInterface: This is a virtual method.')
