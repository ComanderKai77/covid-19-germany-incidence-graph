import requests
import urllib.parse

# Settings
REGION_PATH = "https://raw.githubusercontent.com/jgehrcke/covid-19-germany-gae/master/ags.json"
BASE_PATH = "https://raw.githubusercontent.com/ComanderKai77/covid-19-germany-incidence-graph/master/graphics/"

def get_regions():
    return requests.get(REGION_PATH).json()

def get_header():
    return """
# Cities #

    """

def create_content(name):
    return """
### """ + name + """ ###

![""" + name + """](""" + BASE_PATH + urllib.parse.quote(name) + """.svg)
        
    """

file = get_header()
regions = get_regions()
for region in regions:
    if not "population" in regions[region]:
        continue

    file += create_content(regions[region]["name"])

f = open("cities.md", "w")
f.write(file.strip())
f.close()
