# OMDEPLIB

Python library as part of the OMDEP project. Its aim is to provide an
easy to use interface for plotting oceanic and meteorological data.

## Table of content

- [Dependencies](#dependencies)
- [Tests](#tests)
- [Install](#install)
  - [Production mode](#production-mode)
  - [Development mode](#development-mode)
- [References](#references)

## Dependencies

**NOTE**: If you want to use this repository for development,
create a virtual environment named `venv` in the root directory
and install the required dependencies in there.

- xarray
- matplotlib
- cartopy
- Pillow
- netCDF4
- WindRose

## Tests

Make sure to have the following files used to create the visualizations, you can download
[here](https://drive.google.com/drive/folders/1TTOIBGoP5B0xvj9gcYnuUWBYy3rgmuCx?usp=share_link)

- global-analysis-forecast-phy-001-024-GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS-date-2022-11-13-time-10h-31m-10s-857022ms.nc
- global-analysis-forecast-phy-001-024-GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS-date-2022-11-13-time-13h-27m-31s-211639ms-monthly.nc

and place them in `tmp/data/`.

Make sure to have installed the package, eather in production or development mode.

Then run the following command to start the testing module:

``` sh
python dev_tools/test_chart_builders.py
```

See [local installation](https://pip.pypa.io/en/stable/topics/local-project-installs/) for details.

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

## References

- [Python package deployment tutorial.](https://realpython.com/pypi-publish-python-package/)
- [Build backend "setuptools" quickstart docs.](https://setuptools.pypa.io/en/stable/userguide/quickstart.html)
- [Package discovery and namespace packages for setuptools.](https://setuptools.pypa.io/en/latest/userguide/package_discovery.html#package-discovery-and-namespace-packages)
- [Local project install.](https://pip.pypa.io/en/stable/topics/local-project-installs/)
