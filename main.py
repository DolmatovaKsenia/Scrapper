import pandas as pd
from collections import namedtuple
import os


def main():
    region_map = []
    Region = namedtuple('Region', ['region_code', 'region_name', 'district_name',
                                   'event_city', 'travel_city', 'cityReg'])
    my_file = open("final_regions.txt", 'r')
    directory = "final_regions_csv"
    if not os.path.exists(directory):
        os.makedirs(directory)
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
            if not os.path.exists("final_csv_dir/" + cityReg + ".csv"):
                cityReg.replace('_', ' ')
            data = pd.read_csv("final_csv_dir/" + cityReg + ".csv", sep=',')
            h3all = data["geohash"].values

            N = len(h3all)
            region_code_arr = [region.region_code] * N
            region_name_arr = [region.region_name.replace('_', ' ')] * N
            district_id_arr = [None] * N
            district_name_arr = [region.district_name.replace('_', ' ')] * N
            geohash_arr = h3all
            event_city_arr = [region.event_city.replace('_', ' ')] * N
            travel_city_arr = [region.travel_city.replace('_', ' ')] * N
            df = pd.DataFrame({
                "region_code": region_code_arr,
                "region_name": region_name_arr,
                "district_id": district_id_arr,
                "district_name": district_name_arr,
                "geohash": geohash_arr,
                "event_city": event_city_arr,
                "travel_city": travel_city_arr
            })
            print([region.region_code, region.region_name.replace('_', ' '),
                    region.district_name.replace('_', ' '), region.event_city.replace('_', ' '),
                    region.travel_city.replace('_', ' ')])
            file_name = f"geo_ref_{region.event_city}.csv"
            new_path = os.path.join(directory, file_name)
            df.to_csv(new_path)
        except OSError:
            if cityReg == "???":
                with open("no_geojson_found.txt", "a") as f:
                    f.write(region.event_city + "\n")
                continue
            else:
                print(f"ERROR: not correct {cityReg}!!!!")


if __name__ == "__main__":
    main()
