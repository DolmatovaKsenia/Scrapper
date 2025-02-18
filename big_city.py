import os

from coord2geohash import coord2hash_transformer
import pandas as pd
import sys
import shutil


def main(resolution):
    data = pd.read_csv("городаКоординаты.csv", sep=',')
    cities = data["Город"].values
    width = data["Широта"].values
    longitude = data["Долгота"].values

    geohash_arr = []
    for i in range(len(cities)):
        geohash = coord2hash_transformer(width[i], longitude[i], int(resolution))
        geohash_arr.append(geohash)

    df = pd.DataFrame({
        "Город": cities,
        "geohash": geohash_arr
    })
    df.to_csv("big_city_hash.csv", sep=",")

    directory = "final_csv_dir"
    if not os.path.exists(directory):
        os.makedirs(directory)

    print(len(geohash_arr))

    for geohash in geohash_arr:
        for fname in os.listdir("coord2geohash_csv"):
            f = open("coord2geohash_csv/" + fname)
            if geohash in f.read():
                print("coord2geohash_csv/" + fname)
                shutil.copy(
                    "coord2geohash_csv/" + fname,
                    os.path.join(directory)
                )


if __name__ == "__main__":
    main(sys.argv[1])
