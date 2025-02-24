import os

filenames = []

for fname in os.listdir("final_regions_csv"):
    if fname.endswith('.csv'):
        filenames.append(fname)

with open('result_union_file.csv', 'w', newline='') as outfile:
    for fname in filenames:
        with open(os.path.join("final_regions_csv", fname), 'r') as infile:
            for line in infile:
                outfile.write(line)

print("Данные успешно записаны в result_union_file.csv")