"""
    Created by @namhainguyen2803 in 04/02/2023.
"""
import time
import random
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from math import sin, cos, sqrt, atan2, radians
from collections import defaultdict

df = pd.read_csv("vn.csv")[["lng", "lat", "city"]][:-1]

def modify_cities_index(old_df):
    new_df = old_df.sample(frac=1).reset_index(drop=True)
    return new_df
df = modify_cities_index(df)

Longitude, Latitude, Cities = df["lng"],df["lat"],df["city"]
num_cities = len(df["city"])

def convert_4d_vectors():
    Longitude, Latitude, Cities = df["lng"],df["lat"],df["city"]
    num_cities = len(df["city"])
    num_passengers = int((num_cities - 1) / 2)
    vect = list()
    for i in range(num_cities):
        one_vector = list()
        if i != 0:
            if i <= num_passengers:
                one_vector.append([Longitude[i], Latitude[i], Longitude[i+num_passengers], Latitude[i+num_passengers]])
                one_vector = np.array(one_vector)
                vect.append(one_vector)
    return np.squeeze(np.array(vect))

# lis is dictionary which elements are 4d numpy array
def convert_4d_vectors_to_passengers(dic):
    Longitude, Latitude, Cities = df["lng"],df["lat"],df["city"]
    num_cities = len(df["city"])
    num_passengers = int((num_cities - 1) / 2)
    d = defaultdict(lambda : [0])
    
    for bus_id, lis in dic.items():
        for i in range(len(lis)):
            ind_1 = Longitude.values.tolist().index(lis[i][0])
            ind_2 = Latitude.values.tolist().index(lis[i][1])
            if ind_1 == ind_2:
                d[bus_id+1].append(ind_1)
                d[bus_id+1].append(ind_1+num_passengers)
            else:
                if Longitude[ind_1] == Longitude[ind_2]:
                    d[bus_id+1].append(ind_2)
                elif Latitude[ind_1] == Latitude[ind_2]:
                    d[bus_id+1].append(ind_2)
        d[bus_id+1].sort()
    return d

def show_map():
    Longitude, Latitude, Cities = df["lng"],df["lat"],df["city"]
    num_cities = len(df["city"])
    sns.set_style("darkgrid")
    plt.figure(figsize = (15,8))
    for x, y in zip(Longitude, Latitude):
        rgb = np.random.rand(3,)
        plt.scatter(x, y, c=[rgb], alpha = 0.7, s=3)
    plt.axis([100,100,8,20])
    plt.axis("equal")
    title = "Vietnam's " + str(num_cities) + " Cities"
    plt.title(title, color = "red",fontsize = 15, alpha = 1)
    plt.xlabel("Longitude", fontsize = 10)
    plt.ylabel("Latitude", fontsize = 10)
    # for i in range(len(Province)):
    #     # fontsize to change the size of name of cities
    #     plt.text(Longitude[i],Latitude[i],Province[i],color = "black", fontsize = 4,alpha = 1)
    plt.show();

def encode_decode_dict():
    Longitude, Latitude, Cities = df["lng"],df["lat"],df["city"]
    num_cities = len(df["city"])
    dict_encode={}
    dict_decode={}
    for i in range(len(Cities)):
        dict_encode[Cities[i].strip()] = i
        dict_decode[i] = Cities[i].strip()
    return dict_encode, dict_decode

def calculate_distance(la1, lo1, la2, lo2):
    Longitude, Latitude, Province = df["lng"],df["lat"],df["city"]
    num_cities = len(df["city"])
    Radius_earth = 6373.0
    lat1 = radians(la1)
    lon1 = radians(lo1)
    lat2 = radians(la2)
    lon2 = radians(lo2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = Radius_earth * c
    return distance

def create_matrix_distance():
    Longitude, Latitude, Cities = df["lng"],df["lat"],df["city"]
    num_cities = len(df["city"])
    mat_dist = np.zeros((num_cities, num_cities))
    for i in range(num_cities):
        for j in range(num_cities):
            if i != j:
                mat_dist[i][j] = calculate_distance(Latitude[i], Longitude[i], Latitude[j], Longitude[j])
    return mat_dist

def decode_configuration_provinces(config):
    Longitude, Latitude, Cities = df["lng"],df["lat"],df["city"]
    num_cities = len(df["city"])
    decode_config = list()
    dict_decode = encode_decode_dict()[1]
    for i in range(len(config)):
        province = config[i]
        decode_config.append(dict_decode[province])
    return decode_config

def plot_solution(list_config):
    Longitude, Latitude, Cities = df["lng"],df["lat"],df["city"]
    num_cities = len(df["city"])
    sns.set_style("darkgrid")
    plt.figure(figsize = (15,8))
    for x, y in zip(Longitude, Latitude):
        rgb = np.random.rand(3,)
        plt.scatter(x, y, c=[rgb], linewidths = 4, alpha = 0.7, s=3)
    plt.axis([100,100,8,20])
    plt.axis("equal")
    title = "Vietnam's " + str(num_cities) + " Cities"
    plt.title(title, color = "red",fontsize = 15, alpha = 1)
    plt.xlabel("Longitude", fontsize = 10)
    plt.ylabel("Latitude", fontsize = 10)
    
    j = 0
    co = ['b','g','r','c','m','y','k','w']
    for config in list_config:
        lat = list()
        lon = list()
        name_bus = "Bus" + str(j+1)
        j += 1
        for i in config:
            lat.append(Longitude[i])
            lon.append(Latitude[i])
        # for i in range(len(Cities)):
        #     # fontsize to change the size of name of cities
        #     plt.text(Longitude[i],Latitude[i],Cities[i],color = "black", fontsize = 4,alpha = 1)
        
        plt.plot(lat, lon, color = co[j], label=name_bus) 
    plt.legend(loc="upper left")
    plt.show();
        

if __name__ == "__main__":
    print(print(df))
    print(len(df))
    show_map()