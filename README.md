# SIAPLOTLIB

**Version: 0.2.1**

Python library as part of the SIA project. Its aim is to provide an
easy to use interface for plotting oceanic data.

Page of the project: https://sia-information-system.github.io/sia-website

## Table of content

- [Install](#install)
  - [Requirements before installation](#requirements-before-installation)
  - [Production mode](#production-mode)
  - [Development mode](#development-mode)
- [Tests](#tests)
- [Documentation](#documentation)
- [Contributions](#contributions)

## Install

### Requirements before installation

This package depends on [Cartopy](https://scitools.org.uk/cartopy/docs/latest/) v0.21.1,
which is a package that in order to be installed by `pip` needs to have some C/C++ libraries available in
the host operating system, which it's not a problem in Linux or MacOS, but it is on Windows.
See the [Cartopy installation docs](https://scitools.org.uk/cartopy/docs/latest/installing.html)
to see how to install required dependencies on Linux and MacOS.

If you are on Windows, in order to simplify the installation of this package, we recommend to
use the pre-built Cartopy binaries distributed by `conda` (`anaconda`/`miniconda`). Once you have
`conda`, you can install Cartopy with the following command:

``` bash
conda install cartopy=0.21.1
```

Before install this package make sure you have the C/C++ library installed
on your operating system to build Cartopy, or have the pre-built binaries
installed on the environment you are going to use.

### Production mode

You can install this package from PyPI using:

``` bash
pip install siaplotlib
```

To install the package from source code, clone the repo from GitHub and
run the following command in the package root directory 
(where the `pyproject.toml` file is located):

``` bash
pip install .
```

See [local installation](https://pip.pypa.io/en/stable/topics/local-project-installs/) for details.


### Development mode

**NOTE**: For development it's recommended to use an isolated environment.
You can use tools like `anaconda` / `minionda` or `virtualenv` to create
this kind of environments. On Windows, due to the reasons exposed in the
[Requirements before installation](#requirements-before-installation) section,
we highly recommend to use `conda` as environments manager. If you are on
other operating systen, you don't use conda and you decide to store the
environment in the root directory of the project, name the environment as
`venv` since this name of directory is ignored by git.

To install the package in development mode (--editable), run the following command
in the package root directory (where de `pyproject.toml` file is located):

``` sh
pip install --editable .[dev]
```

See [local installation](https://pip.pypa.io/en/stable/topics/local-project-installs/) for details.

To increase the version number, the package `bumpver` is used.
[Read the docs](https://github.com/mbarkhau/bumpver#reference)
to see how to use it.

## Tests

Make sure to have the following files used to create the visualizations, you can download them
[here](https://drive.google.com/drive/folders/1TTOIBGoP5B0xvj9gcYnuUWBYy3rgmuCx?usp=share_link).

- global-analysis-forecast-phy-001-024-GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS-date-2022-11-13-time-10h-31m-10s-857022ms.nc
- global-analysis-forecast-phy-001-024-GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS-date-2022-11-13-time-13h-27m-31s-211639ms-monthly.nc
- time-series.png
- heatmap.gif

Once done, place them in `tmp/data/`.

Make sure to have installed the package, whether in production or development mode.

Then go to the test directory and run the following command to start the testing module:

``` sh
python test_chart_builders.py
```

Tests are written with `unittest` framework, so alternative ways of running the
test are described in its [documentation](https://docs.python.org/3/library/unittest.html).

## Documentation

Read the documentation for this package [here](./docs/README.md).

## Contributions

Rules are:

- First ask to maintainers if the new proposed feature can be added. You can open an issue on GitHub.
- Document every new feature added.
- Add tests for each new feature.
