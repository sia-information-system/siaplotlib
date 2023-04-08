# Standard.
from pathlib import Path
from collections.abc import Callable


class ChartBuilderInterface:
  def save(
    self,
    filepath: str | Path
  ) -> None:
    raise NotImplementedError(f'{self.__class__.__name__}: This is a virtual method. Must be implemented.')

  def build(
    self,
    success_callback: Callable[[], None],
    failure_callback: Callable[[Exception], None]
  ):
    raise NotImplementedError(f'{self.__class__.__name__}: This is a virtual method. Must be implemented.')


  def sync_build(self):
    raise NotImplementedError(f'{self.__class__.__name__}: This is a virtual method. Must be implemented.')


  def verify_safe_build_process(self):
    raise NotImplementedError(f'{self.__class__.__name__}: This is a virtual method. Must be implemented.')
