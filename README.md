# SIAPLOTLIB

Python library as part of the SIA project. Its aim is to provide an
easy to use interface for plotting oceanic and meteorological data.

## Table of content

- [Dependencies](#dependencies)
- [Install](#install)
  - [Production mode](#production-mode)
  - [Development mode](#development-mode)
- [Tests](#tests)
- [References](#references)

## Dependencies

**NOTE**: If you want to use this repository for development,
create a virtual environment and install the required dependencies in there.

If your are using `virtualenv` or you don't want to use virtual environments at all,
[make sure you have the libraries to build cartopy](https://scitools.org.uk/cartopy/docs/latest/installing.html#installing).
If you use `virtualenv`, create the environtment with the name `venv` in the project's root directory.

If your are on Windows, it's recommended to use [anaconda/miniconda](https://docs.conda.io/en/latest/miniconda.html) to create a
virtual environment and install cartopy v0.21.1 first (with `conda install`). Then, install this package.

## Install

The following instructions cover a local installation.
See [local installation](https://pip.pypa.io/en/stable/topics/local-project-installs/) for details.

### Production mode

To install the package in production mode, run the following command in the
package root directory (where de `pyproject.toml` file is located):

```
pip install .
```

### Development mode

To install the package in development mode (--editable), run the following command
in the package root directory (where de `pyproject.toml` file is located):

``` sh
pip install --editable .
```

## Tests

Make sure to have the following files used to create the visualizations, you can download
[here](https://drive.google.com/drive/folders/1TTOIBGoP5B0xvj9gcYnuUWBYy3rgmuCx?usp=share_link)

- global-analysis-forecast-phy-001-024-GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS-date-2022-11-13-time-10h-31m-10s-857022ms.nc
- global-analysis-forecast-phy-001-024-GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS-date-2022-11-13-time-13h-27m-31s-211639ms-monthly.nc
- time-series.png
- heatmap.gif

and place them in `tmp/data/`.

Make sure to have installed the package, whether in production or development mode.

Then run the following command to start the testing module:

``` sh
python tests/test_chart_builders.py
```

Tests are written with `unittest` framework, so alternative ways of run the
test are described in its [documentation](https://docs.python.org/3/library/unittest.html).

## References

- [Python package deployment tutorial.](https://realpython.com/pypi-publish-python-package/)
- [Build backend "setuptools" quickstart docs.](https://setuptools.pypa.io/en/stable/userguide/quickstart.html)
- [Package discovery and namespace packages for setuptools.](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#package-discovery-and-namespace-packages)
- [Local project install.](https://pip.pypa.io/en/stable/topics/local-project-installs/)
