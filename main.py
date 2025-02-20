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
        abracadabra = my_file.readline()
        print(abracadabra)
        if not abracadabra:
            break
        arr = abracadabra.split()
        if len(arr) != 6:
            continue
        region_map.append(Region(arr[0], arr[1], arr[2], arr[3], arr[4], arr[5]))
        for region in region_map:
            cityReg = region.cityReg
            try:
                data = pd.read_csv("final_csv_dir/" + cityReg + ".csv", sep=',')
                h3all = data["geohash"].values

                N = len(h3all)
                region_code_arr = [region.region_code] * N
                region_name_arr = [region.region_name] * N
                district_id_arr = [None] * N
                district_name_arr = [region.district_name] * N
                geohash_arr = h3all
                event_city_arr = [region.event_city] * N
                travel_city_arr = [region.travel_city] * N
                df = pd.DataFrame({
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
                df.to_csv(new_path)
            except OSError:
                continue


if __name__ == "__main__":
    main()
