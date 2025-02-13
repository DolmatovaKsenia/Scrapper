import os.path

from bs4 import BeautifulSoup
import requests

link = "https://tools.paintmaps.com/map-cropping/RU"
directory = 'geojsons_scrapped'
if not os.path.exists(directory):
    os.makedirs(directory)

response = requests.get(link).text
main_soup = BeautifulSoup(response, 'html.parser')

regions_cnt = dict()

block = main_soup.find('div', class_='panel-group')
regions = block.find_all('div', class_='panel panel-default')
for reg in regions:
    pod_regions = reg.find_all('div', class_='panel-body')
    for elem in pod_regions:
        linker = elem.find_all('a')
        href = [lin.get('href') for lin in linker]
        for i in href:
            new_link = "https://tools.paintmaps.com/" + i
            new_response = requests.get(new_link).text
            main_soup2 = BeautifulSoup(new_response, 'html.parser')
            block2 = main_soup2.find_all('div', class_='col-md-12')[1]
            li = block2.find('a').get('href')
            newest_link = "https://tools.paintmaps.com/" + li
            new_response2 = requests.get(newest_link).text
            soup = BeautifulSoup(new_response2, 'html.parser')
            bl = soup.find_all('div', class_='row')
            bloc = ''
            for el in bl:
                if "(geojson format)" in el.text:
                    bloc = el
            name_geo = bloc.find('a').text
            geojson = bloc.find('a').get('href')
            geo_url = "https://tools.paintmaps.com/" + geojson
            geo_response = requests.get(geo_url)
            if name_geo in regions_cnt:
                regions_cnt[name_geo] = regions_cnt[name_geo] + 1
                name_geo = name_geo[:-8] + str(regions_cnt[name_geo]) + ".geojson"
            else:
                regions_cnt[name_geo] = 1
            with open(os.path.join(directory, name_geo), 'wb') as f:
                f.write(geo_response.content)
            print(f"Скачан файл: {name_geo}")
print(len(regions))
