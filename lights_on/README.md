# Lights On

## Project Introduction

Night-time luminosity as captured in satellite images has been shown to be a valid proxy for a multitude of economic indicators.
The idea of this project is to provide an easy tool for economists to explore geospatial and time-dependent luminosity data for statistical analysis.


## Technology

This tool is not a package or software, but rather a combination of different open-source projects tailored to this purpose making it as easy as possible to get started without having to do lots of setup work. _Lights On_ relies heavily on:
* [Docker](https://www.docker.com/)
* [Jupyter](http://jupyter.org/)


## Get Started

### Notes

* On mac, the ip is not localhost but can be found as follows `docker-machine ip $(docker-machine active)`
* If docker building errors with `No space left on device`, try: `docker rm $(docker ps -a -q) && docker rmi -f $(docker images -f dangling=true -q)`


## Data

* [Annual Nighttime Composites](https://ngdc.noaa.gov/eog/dmsp/downloadV4composites.html)

## Further Reading

### On Luminosity in Economics

* Henderson, V., Storeygard, A., & Weil, D. N. (2011). Measuring Economic Growth from Outer Space. American Economic Review, 102 (2012 ), 994 – 1028.


## Documentation

### User Functions

* _load_light_grid_
* _plot_light_grid_
* _animate_light_movement_
* _plot_light_diff_
* _plot_light_change_
* _plot_light_growth_
* _animate_light_diff_
* _animate_light_change_
* _animate_light_growth_
* _plot_aggregated_light_series_
* _plot_aggregated_light_sum_
* _plot_aggregated_light_mean_
* _plot_aggregated_light_series_diff_
* _plot_light_series_mean_change_
* _plot_light_series_sum_change_
* _plot_light_series_sum_growth_
