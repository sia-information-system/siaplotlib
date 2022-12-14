# OMDEPLIB

Python library as part of the OMDEP project. Its aim is to provide an
easy to use interface for plotting oceanic and meteorological data.

## Table of content

- [Dependencies](#dependencies)
- [Tests](#tests)

## Dependencies

**NOTE**: If you want to use this repository for development,
create a virtual environment named `venv` in the root directory
and install the required dependencies in there.

- xarray
- matplotlib
- cartopy
- Pillow

## Tests

Make sure to have the following files used to create the visualizations, you can download [here](https://drive.google.com/drive/folders/1TTOIBGoP5B0xvj9gcYnuUWBYy3rgmuCx?usp=share_link)

- global-analysis-forecast-phy-001-024-GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS-date-2022-11-13-time-10h-31m-10s-857022ms.nc
- global-analysis-forecast-phy-001-024-GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS-date-2022-11-13-time-13h-27m-31s-211639ms-monthly.nc

and place them in `tmp/data/`.

Run the following command to start the testing module:

``` sh
python tests.py
```