from omdepplotlib.charts import base_chart
import matplotlib.pyplot as plt
import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature

class SinglePointTimeSeries(base_chart.Chart):
  def __init__(
    self,
    series_names: list[str],
    series_data: list[pd.Series],
    lon: float,
    lat: float,
    lon_interval: list[float],
    lat_interval: list[float],
    title: str,
    grouping_var_label: str,
    y_label: str,
    x_label: str = None,
    show_series_names: bool = True,
    build_on_create: bool = True,
    verbose: bool = False
  ) -> None:
    super().__init__(verbose=verbose)
    self.series_names = series_names
    self.series_data = series_data
    self.lon = lon
    self.lat = lat
    self.lon_interval = lon_interval
    self.lat_interval = lat_interval
    self.title = title
    self.grouping_var_label = grouping_var_label
    self.y_label = y_label
    self.x_label = x_label
    self.show_series_names = show_series_names

    if build_on_create:
      self.build()


  def build(self):
    # Define the caracteristics of the plot
    fig = plt.figure()
    ax = fig.add_subplot(111)

    for i in range(len(self.series_names)):
      ax.plot(
        self.series_data[i].index,
        self.series_data[i].values,
        label=self.series_names[i])                                                      # plot the time serie

    ax.grid()                                                                            # add the grid lines
    ax.set_title(self.title)
    ax.set_ylabel(self.y_label)
    if self.x_label is not None:
      ax.set_xlabel(self.x_label)
    if self.show_series_names:
      ax.legend(loc='center right', title=self.grouping_var_label)
    fig.suptitle(
      f'Longitude: {self.lon}°E\nLatitude: {self.lat}°N',
      horizontalalignment='left',
      x=0.12,
      y=1.05)                                                                            # Display the coordinates on the plot
    fig.autofmt_xdate(ha='center')                                                       # format the dates in the x axis

    # Display the location of the point on a mini map
    # .add_axes: https://www.geeksforgeeks.org/how-to-add-axes-to-a-figure-in-matplotlib-with-python/
    ax_mini_map = fig.add_axes([0.74, 0.97, 0.2, 0.2], projection=ccrs.PlateCarree())    # create the minimap and define its projection
    ax_mini_map.add_feature(cfeature.LAND, zorder=1, edgecolor='k')                      # add land mask 
    ax_mini_map.set_extent(self.lon_interval + self.lat_interval, crs=ccrs.PlateCarree()) # define the extent of the map [lon_min,lon_max,lat_min,lat_max]
    ax_mini_map.scatter(self.lon, self.lat, 20, transform=ccrs.PlateCarree())                      # plot the location of the point
    gl = ax_mini_map.gridlines(draw_labels=True)                                         # add the coastlines
    gl.right_labels = False                                                              # remove latitude labels on the right
    gl.top_labels = False                                                                # remove longitude labels on the top

    self._fig = fig
    return self
