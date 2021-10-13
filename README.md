# NCEI CDO API Wrapper
 a very simple and naive Python wrapper for the [NCEI Climate Data Online API v2](https://www.ncdc.noaa.gov/cdo-web/webservices/v2) 

## How to use
- First, obtain the API Token from the [request page](https://www.ncdc.noaa.gov/cdo-web/token)
- Requirements: [requests](https://pypi.org/project/requests/), datetime
- To start, call a NOAA object with the obtained token 
```
new_noaa = NOAA(obtained_token)
```
- If you want more information on what ID to type, most functions will provide a json containing desired information if no arguments are supplied. However, for some functions, it is desired to use ```limit``` and ```offset``` args to get more IDs.
- Other than that, if you want some additional information, like data about stations in a area defined by coordinates, the following will work:
```
station_data = new_noaa.stations(extent=[47.5204,-122.2047,47.6139,-122.1065])
print(station_data)
```
