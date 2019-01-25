import re
import numpy as np
import io
import json
import plotly
import plotly.graph_objs as go

import pandas as pd

try:
    open_file = open('C:/WORK/data/deaths.csv','r+',encoding='utf-8')
    keys = tuple(open_file.readline().strip().split(','))
    keys = [key.replace("'","").replace('"',"").title() for key in keys]

    df = open_file.read().replace("'","").replace('"',"").splitlines()


except EOFError as fille_open_error:
    print("Check filepath or file: ", fille_open_error)

finally:
    open_file.close()


def get_district(s,i):
    st = re.split(r',', s, maxsplit=i + 1)
    st = st[i]
    return st

years_ = []


def neighborhood_name(s, i):
    st = re.split(r',', s, maxsplit=i + 1)
    st = st[i]
    return st

def get_year(s):
    year = re.search("20\d{2}", s).group(0)
    if year not in years_:
        years_.append(year)
    return year

def get_POPESTIMATES(s, indexs):
    row_s = re.split(r",", s)
    POPESTIMATES = [row_s[p] for p in indexs]
    return POPESTIMATES

def get_year_of_deaths(s):
    deaths_y = re.search("\d+\-\d+|>=\d+",s).group(0)
    return deaths_y

def get_number(s,i):
    number = re.split(r',', s, maxsplit=i + 1)[-1]

    return number


"""
{
    "district1": {
        "neighbourhood_1": {
            "1-4": {
                "2017": 2
            }
        }
    }
}"""


def read_data():
    data_set = {}
    for i in range(len(df)):
        row = df[i].rstrip()
        if not row:
            print("emplty row: ", i)
            continue
        district = get_district(row, list(keys).index('District.Name'))
        neighborhood = neighborhood_name(row, list(keys).index('Neighborhood.Name'))
        year = get_year(row)
        year_of_deaths = get_year_of_deaths(row)
        number = get_number(row,list(keys).index('Number'))


        if district not in data_set.keys():
            data_set[district] = {}

        if neighborhood not in data_set[district].keys():
            data_set[district][neighborhood] = {}

        if year_of_deaths not in data_set[district][neighborhood].keys():
            data_set[district][neighborhood][year_of_deaths] = {}

        if year not in data_set[district][neighborhood][year_of_deaths].keys():
            data_set[district][neighborhood][year_of_deaths][year] = int(number)





    return data_set

def dataset_to_json(data_):
    with io.open('barsa_deaf.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(data_, ensure_ascii=False))




def graph_show(scatter_,bar_,pie_,pie2):



    figure = {"data": [
        {
            "x": np.array(list(scatter_.keys())),
            "y": np.array(list(scatter_.values())),
            "type": "scatter",


        },
        {
            "x": np.array(list(bar_.keys())),
            "y": np.array(list(bar_.values())),
            "type": "bar",
            "xaxis": "x2",
            "yaxis": "y2"

        },
        {
            "labels": np.array(list(pie_.keys())),
            "values": np.array(list(pie_.values())),
            "type": "pie",
            "name": "P2",
            'domain': {'x': [0, 0.45], 'y': [0.55, 1]},
        },
        {
            "labels": np.array(list(pie2.keys())),
            "values": np.array(list(pie2.values())),
            "type": "pie",
            "name": "P3",
            'domain': {'x': [0.55, 1], 'y': [0.55, 1]},
        }
    ],
        "layout":
            {'xaxis': {'domain': [0, 0.45]},
             'xaxis2': {'domain': [0.55, 1]},
             'yaxis': {'domain': [0, 0.45]},
             'yaxis2': {'anchor': 'x2', 'domain': [0, 0.45]}
             }
    }
    plotly.offline.plot(figure, filename="plot.html")



def total_die_by_year(data):
    total_die_of_year_ = {k: 0 for k in years_}

    for district in  data.values():
        for neighborhood in district.values():
            for y in neighborhood.values():
                for ye,quantity in y.items():
                    total_die_of_year_[ye]+=quantity

    return total_die_of_year_

def dia_by_year_old(data):
    dia_by_year_old_ = dict()

    for district in  data.values():
        for neighborhood in district.values():

            for k,y in neighborhood.items():
                try:
                    dia_by_year_old_[k] += sum(y.values())
                except:
                    dia_by_year_old_[k] = sum(y.values())

    return dia_by_year_old_


def dia_by_Ciutat_Vella(data):
    dia_by_year_old_ = dict()


    for neighborhood in data['Ciutat Vella'].values():
        print('neighborhood',neighborhood)

        for k,y in neighborhood.items():
            try:
                dia_by_year_old_[k] += sum(y.values())
            except:
                dia_by_year_old_[k] = sum(y.values())

    return dia_by_year_old_


if __name__ == '__main__':
    data =read_data()

    dataset_to_json(data)

    total_die_of_year_ = total_die_by_year(data)

    dia_by_year_old_ = dia_by_year_old(data)

    dia_in_Ciutat_Vella = dia_by_Ciutat_Vella(data)


    graph_show(bar_=dia_by_year_old_, scatter_=total_die_of_year_, pie2=dia_in_Ciutat_Vella, pie_=total_die_of_year_)
