import os.path

from bs4 import BeautifulSoup
import requests


def parser(reg):
    lin = reg.find('a').get('href')
    new_l = "https://tools.paintmaps.com/" + lin
    resp = requests.get(new_l).text
    ms = BeautifulSoup(resp, 'html.parser')
    block2 = ms.find_all('div', class_='col-md-12')[1]
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
    if " " in name_geo:
        name_geo = name_geo.replace(" ", "_")
    if name_geo in regions_cnt:
        regions_cnt[name_geo] = regions_cnt[name_geo] + 1
        name_geo = name_geo[:-8] + str(regions_cnt[name_geo]) + ".geojson"
    else:
        regions_cnt[name_geo] = 1
    with open(os.path.join(directory, name_geo), 'wb') as f:
        f.write(geo_response.content)
    print(f"Скачан файл: {name_geo}")


link = "https://tools.paintmaps.com/map-cropping/RU"
directory = 'geojsons_scrapped'
if not os.path.exists(directory):
    os.makedirs(directory)

response = requests.get(link).text
main_soup = BeautifulSoup(response, 'html.parser')

regions_cnt = dict()

big_block = main_soup.find('div', id='fh5co-page')
row_arr = big_block.find_all('div', class_='row')[5:]
for r in row_arr:
    reg_3 = r.find_all('div', class_="col-md-4")
    for reg in reg_3:
        if reg.find('a') is None:
            continue
        parser(reg)
    if "Zabaykalsky" in r.text:
        break


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
            if " " in name_geo:
                name_geo = name_geo.replace(" ", "_")
            if name_geo in regions_cnt:
                regions_cnt[name_geo] = regions_cnt[name_geo] + 1
                name_geo = name_geo[:-8] + str(regions_cnt[name_geo]) + ".geojson"
            else:
                regions_cnt[name_geo] = 1
            with open(os.path.join(directory, name_geo), 'wb') as f:
                f.write(geo_response.content)
            print(f"Скачан файл: {name_geo}")
print(len(regions))
