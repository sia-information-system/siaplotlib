import os


def mkdir_r(path):
  os.makedirs(path, exist_ok=True)
