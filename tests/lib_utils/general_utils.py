import os
import pathlib

VISUALIZATIONS_DIR = pathlib.Path(pathlib.Path(__file__).parent.absolute(), '..', '..', 'tmp', 'visualizations')
DATA_DIR = pathlib.Path(pathlib.Path(__file__).parent.absolute(), '..', '..', 'tmp', 'data')

def mkdir_r(path):
  os.makedirs(path, exist_ok=True)
