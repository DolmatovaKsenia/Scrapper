import json
import pandas as pd
import h3
import os
import sys
from pathlib import Path
import shutil


def main(resolution):
    directory = "coord2geohash_csv"
    if not os.path.exists(directory):
        os.makedirs(directory)

    p = Path("geojsons_scrapped")
    for geojson_file in p.rglob("*"):
        geojson_file_str = str(geojson_file)
        with open(geojson_file, 'r', encoding='utf-8') as j:
            contents = json.loads(j.read())

        h3all = set()

        coord = contents['features'][0]['geometry']['coordinates']
        for i in coord:
            dta = {
                "coordinates": i,
                "type": "Polygon"
            }
            try:
                h3index = h3.polyfill_geojson(dta, int(resolution))
            except TypeError:
                err_directory = "error_geohash_csv"
                if not os.path.exists(err_directory):
                    os.makedirs(err_directory)
                print(geojson_file_str[18:-8])
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

        file_name = f"{geojson_file_str[18:-8]}.csv"
        print(file_name)
        new_path = os.path.join(directory, file_name)
        df.to_csv(new_path)


if __name__ == "__main__":
    main(sys.argv[1])

