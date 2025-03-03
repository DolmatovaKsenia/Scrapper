import os

for fname in os.listdir("coord2geohash_csv"):
    f = open("coord2geohash_csv/" + fname, encoding="utf-8")
    if "882eac5365fffff" in f.read():
        print("coord2geohash_csv/" + fname)