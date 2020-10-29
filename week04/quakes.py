"""A script to find the biggest earthquake in an online dataset."""

# At the top of the file, import any libraries you will use.
# import ...
import requests
import json
import os
import math


def request_map_at(lat, long, zoom=10, satellite=True):
    base_url = "https://mt0.google.com/vt?"

    x_coord, y_coord = deg2num(lat, long, zoom)

    params = dict(
        x=int(x_coord),
        y=int(y_coord),
        z=zoom
    )
    if satellite:
        params['lyrs'] = 's'

    return requests.get(base_url, params=params)


def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)


def get_data():
    quakes = requests.get("http://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
                          params={
                              'starttime': "2000-01-01",
                              "maxlatitude": "58.723",
                              "minlatitude": "50.008",
                              "maxlongitude": "1.67",
                              "minlongitude": "-9.756",
                              "minmagnitude": "1",
                              "endtime": "2018-10-11",
                              "orderby": "time-asc"}
                          )
    return quakes


def max_magnitude(features):
    max_mag = 0
    coord_max_mag = []
    for feature in features:
        magnitude = feature["properties"]["mag"]
        coordinates = feature["geometry"]["coordinates"]
        if max_mag < magnitude:
            max_mag = magnitude
            if max_mag == magnitude:
                coord_max_mag.append(coordinates)
            else:
                coord_max_mag = coordinates
    return max_mag, coord_max_mag


def main():
    # getting earthquake data from URL
    quakes = get_data()
    # parsing data
    earthquake_data = json.loads(quakes.text)
    # extracting features from data (where earthquake mag and coordinates located)
    features = earthquake_data["features"]
    # looking for coordinates where max magnitude occurs
    max_mag, coord_max_mag = max_magnitude(features)
    # generating URLs for map
    for coordinate in coord_max_mag:
        map_response = request_map_at(coordinate[0], coordinate[1])
        url = map_response.url
        print(url[0:])

    # Image(map_png.content)

    print(f"The maximum magnitude is {max_mag} "
          f"and it occured at coordinates {coord_max_mag}.")


if __name__ == "__main__":
    main()

    #print(json.dumps(earthquake_data, indent=4))
