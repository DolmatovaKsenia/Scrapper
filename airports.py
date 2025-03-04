import json
from collections import namedtuple

import pandas as pd
import h3
import os
import sys
from pathlib import Path
import shutil


def main(resolution):
    directory = "airports_temp"
    if not os.path.exists(directory):
        os.makedirs(directory)

    p = Path("airport_geojson")
    for geojson_file in p.rglob("*"):
        geojson_file_str = str(geojson_file)
        with open(geojson_file, 'r', encoding='utf-8') as j:
            contents = json.loads(j.read())

        h3all = set()


        try:
            for feature in contents['features']:
                geometry = feature['geometry']
                if geometry['type'] == 'Polygon':
                    h3index = h3.polyfill_geojson(geometry, int(resolution))
                    h3all.update(h3index)
                else:
                    print(f"Пропущено: {geometry['type']} не поддерживается.")
        except TypeError:
            err_directory = "error_geohash_csv"
            if not os.path.exists(err_directory):
                os.makedirs(err_directory)
            shutil.copy(
                geojson_file,
                os.path.join(err_directory)
            )
            continue


        if len(h3index) > 0:
            h3all = h3all.union(h3index)

        if isinstance(h3all, set):
            h3all = list(h3all)

        geohash_arr = h3all
        df = pd.DataFrame({
            "geohash": geohash_arr
        })

        file_name = f"{geojson_file_str[16:-8]}.csv"
        new_path = os.path.join(directory, file_name)
        df.to_csv(new_path, index=False)

    region_map = []
    Region = namedtuple('Region', ['region_code', 'region_name', 'district_name',
                                       'event_city', 'travel_city', 'cityReg'])
    my_file = open("airports.txt", 'r', encoding="utf-8")

    directory = "airports_temp2"
    if not os.path.exists(directory):
        os.makedirs(directory)

    start = 7192448

    while True:
        line = my_file.readline()
        if not line:
            break
        arr = line.split()
        if len(arr) != 6:
            continue
        region_map.append(Region(arr[0], arr[1], arr[2], arr[3], arr[4], arr[5]))
        region = region_map[-1]
        cityReg = region.cityReg
        cityReg = cityReg.replace(' ', '_')
        try:
            if not os.path.exists("airports_temp/" + cityReg + ".csv"):
                if "airport" not in cityReg:
                    cityReg.replace('_', ' ')
            data = pd.read_csv("airports_temp/" + cityReg + ".csv", sep=',')
            h3all = data["geohash"].values

            N = len(h3all)
            region_code_arr = [region.region_code] * N
            region_name_arr = [region.region_name.replace('_', ' ')] * N
            district_id_arr = [None] * N
            district_name_arr = [region.district_name.replace('_', ' ')] * N
            geohash_arr = h3all
            event_city_arr = [region.event_city.replace('_', ' ')] * N
            travel_city_arr = [region.travel_city.replace('_', ' ')] * N
            end = start + N
            cnt = list(range(start, end))
            start = end
            df = pd.DataFrame({
                "row_number" : cnt,
                "region_code": region_code_arr,
                "region_name": region_name_arr,
                "district_id": district_id_arr,
                "district_name": district_name_arr,
                "geohash": geohash_arr,
                "event_city": event_city_arr,
                "travel_city": travel_city_arr
            })
            file_name = f"geo_ref_{region.event_city}.csv"
            new_path = os.path.join(directory, file_name)
            df.to_csv(new_path, index=False)
        except OSError:
            if cityReg == "???":
                with open("no_geojson_found.txt", "a", encoding="utf-8") as f:
                    f.write(region.event_city + "\n")
                continue
            else:
                print(f"ERROR: not correct {cityReg}!!!!")

    dataframes = []

    for fname in os.listdir(directory):
        if fname.endswith('.csv'):
            data = pd.read_csv(os.path.join(directory, fname), sep=',')
            dataframes.append(data)

    big_data = pd.concat(dataframes, ignore_index=True)

    if "Unnamed: 0" in big_data.columns:
        big_data = big_data.drop("Unnamed: 0", axis=1)

    big_data.to_csv("airports_file.csv", sep=',', index=False)

    print("Данные успешно записаны в airports_file.csv")


def coord2hash_transformer(width, longitude, resolution):
    h3index = h3.geo_to_h3(width, longitude, int(resolution))
    return h3index


if __name__ == "__main__":
    main(sys.argv[1])