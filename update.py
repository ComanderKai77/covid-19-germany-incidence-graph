import dateutil.parser as dp
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import requests
from io import StringIO
import sys
import time as t

# Settings
REGION_PATH = "https://raw.githubusercontent.com/jgehrcke/covid-19-germany-gae/master/ags.json"
DATA_PATH = "https://raw.githubusercontent.com/jgehrcke/covid-19-germany-gae/master/cases-rki-by-ags.csv"

def get_regions():
    return requests.get(REGION_PATH).json()

def get_data():
    return str(requests.get(DATA_PATH).content)

def calc(data, region, region_id):
    if not "population" in region:
        return None, None

    factor = 100000 / region["population"]
    row_id = None

    rows = data.split("\\n")
    for i, cell in enumerate(rows[0].split(",")):
        if cell == region_id:
            row_id = i

    time_list = []
    date_list = []
    for i in range(len(rows)-2):
        row = rows[i+1].split(",")
        time_list.append(row[0])
        date_list.append(row[row_id])

    new_per_day = []
    for i, d in enumerate(date_list):
        prev_day = int(date_list[i - 1])
        if i == 0:
            prev_day = 0

        new_per_day.append(int(date_list[i]) - prev_day)

    new_per_7_day = []
    for i, d in enumerate(new_per_day):
        week = 0
        for j in range(7):
            if i - j >= 0:
                week += new_per_day[i - j]
        new_per_7_day.append(week)

    incidence = []
    for week in new_per_7_day:
        incidence.append(week * factor)

    return time_list, incidence

def generate_chart(name, time, incidence, save_path):
    datetime_list = list(map(lambda x:dp.parse(x),time))

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d.%m.%Y"))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=len(datetime_list) // 9))
    plt.rc("grid", linestyle="--", color="gray")
    plt.grid(True)
    plt.plot(datetime_list, incidence)
    fig = plt.gcf()
    plt.gcf().autofmt_xdate()

    fig.suptitle("Inzidenzverlauf " + name, fontsize=18)
    # plt.xlabel("Zeit", fontsize=10)
    plt.ylabel("Inzidenz pro 7 Tage pro 100.000 Einwohner", fontsize=10)

    fig.savefig(save_path)
    plt.clf()

start_time = t.time()

regions = get_regions()
data = get_data()

for region in regions:
    time, incidence = calc(data, regions[region], region)
    if not time:
        continue

    generate_chart(regions[region]["name"], time, incidence, "graphics/" + regions[region]["name"] + ".svg")
end_time = t.time()

print("Took " + str(end_time - start_time) + "s")
