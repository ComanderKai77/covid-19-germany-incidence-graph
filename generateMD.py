import requests
import urllib.parse

# Settings
REGION_PATH = "https://raw.githubusercontent.com/jgehrcke/covid-19-germany-gae/master/ags.json"
BASE_PATH = "https://raw.githubusercontent.com/ComanderKai77/covid-19-germany-incidence-graph/master/graphics/"

def get_regions():
    return requests.get(REGION_PATH).json()

def get_header():
    return "# Cities \n"

def create_content(name, population):
    return "### {0} (Einwohner: {1})\n\n![{0}]({2}.svg)\n\n".format(name, population, BASE_PATH + urllib.parse.quote(name))

def get_cities_list():
    cities = []
    regions = get_regions()
    for region in regions:
        if not "population" in regions[region]:
            continue
        cities.append([regions[region]["name"], regions[region]["population"]])

    cities.sort(key=lambda city: city[0])
    return cities

def generate_file():
    file = get_header()

    cities = get_cities_list()
    for city in cities:
        file += create_content(*city)

    f = open("cities.md", "w")
    f.write(file)
    f.close()

generate_file()
