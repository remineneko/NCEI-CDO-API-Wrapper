# NCEI CDO API Wrapper
 a very simple and naive Python wrapper for the [NCEI Climate Data Online API v2](https://www.ncdc.noaa.gov/cdo-web/webservices/v2) 

## How to use
- First, obtain the API Token from the [request page](https://www.ncdc.noaa.gov/cdo-web/token)
- Requirements: [requests](https://pypi.org/project/requests/), [tabulate](https://pypi.org/project/tabulate/)
- To start, call a NOAA object with the obtained token 
```
new_noaa = NOAA(obtained_token)
```
- If you want more information on what ID to type, most functions will provide a json containing desired information if no arguments are supplied. However, for some functions, it is desired to use ```limit``` and ```offset``` args to get more IDs.
- Other than that, if you want some additional information, like data about stations in an area defined by coordinates, the following will work:
```
station_data = new_noaa.stations(extent=[47.5204,-122.2047,47.6139,-122.1065])
print(station_data)
```
The result will be
```
  elevation  mindate     maxdate       latitude  name                            datacoverage  id                 elevationUnit      longitude
-----------  ----------  ----------  ----------  ----------------------------  --------------  -----------------  ---------------  -----------
      199.6  2008-06-01  2016-09-18     47.5503  EASTGATE 1.7 SSW, WA US               0.8814  GHCND:US1WAKG0016  METERS              -122.15
      240.8  2010-05-01  2017-09-03     47.5604  EASTGATE 1.1 SW, WA US                0.9996  GHCND:US1WAKG0024  METERS              -122.151
       85.6  2008-07-01  2016-07-16     47.5916  BELLEVUE 0.8 S, WA US                 0.9999  GHCND:US1WAKG0032  METERS              -122.155
      104.2  2008-06-01  2021-06-04     47.5211  NEWPORT HILLS 1.9 SSE, WA US          1       GHCND:US1WAKG0042  METERS              -122.161
       58.5  2008-08-01  2009-04-12     47.6138  BELLEVUE 2.3 ENE, WA US               1       GHCND:US1WAKG0048  METERS              -122.108
      199.9  2008-06-01  2009-11-22     47.5465  NEWPORT HILLS 1.4 E, WA US            0.9998  GHCND:US1WAKG0049  METERS              -122.144
       27.1  2008-07-01  2021-10-10     47.6046  BELLEVUE 1.8 W, WA US                 0.9999  GHCND:US1WAKG0065  METERS              -122.193
      159.4  2008-11-01  2021-10-08     47.5694  BELLEVUE 2.3 SSE, WA US               1       GHCND:US1WAKG0094  METERS              -122.127
       82.3  2008-12-01  2010-09-17     47.6095  BELLEVUE 0.6 NE, WA US                1       GHCND:US1WAKG0102  METERS              -122.146
      109.4  2017-03-31  2021-10-02     47.594   BELLEVUE 1.1 SE, WA US                0.377   GHCND:US1WAKG0231  METERS              -122.136

```
Of course, printing is made to be more easy to look at, but you can still interact with the returned data normally as a ```dict```.
