import os
import pandas as pd

dataframes = []

for fname in os.listdir("final_regions_csv"):
    if fname.endswith('.csv'):
        data = pd.read_csv(os.path.join("final_regions_csv", fname), sep=',')
        dataframes.append(data)

big_data = pd.concat(dataframes, ignore_index=True)

if "Unnamed: 0" in big_data.columns:
    big_data = big_data.drop("Unnamed: 0", axis=1)

big_data.reset_index(drop=False, inplace=True)
big_data.rename(columns={'index': 'row_number'}, inplace=True)

shablon = ["row_number", "region_code", "region_name", "district_id", "district_name", "geohash", "event_city", "travel_city"]

big_data.to_csv("result_union_file.csv", sep=',', index=False)

print("Данные успешно записаны в result_union_file.csv")