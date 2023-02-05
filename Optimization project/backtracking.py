import copy 
import random
import numpy as np
from collections import defaultdict
import time
from collections import deque

res = list()
def Try(num_buses, num_passengers, configuration = list()):
    for bus in range(1, num_buses + 1):
        configuration.append(bus)
        
        if len(configuration) == num_passengers:
            # print(f"Configuration: {configuration}")
            res.append(configuration)
            configuration = configuration[:-1]
        else:
            new_configuration = copy.deepcopy(configuration)
            Try(num_buses, num_passengers, new_configuration)
            configuration = configuration[:-1]


def generate_carriages(num_buses, num_passengers, not_lack_buses = True):
    Try(num_buses, num_passengers)
    list_carriages = list()
    for i in range(len(res)):
        list_carriage = list()
        mark = False
        for bus in range(1, num_buses + 1):
            carriage = [0]
            for passenger in range(len(res[i])):
                if res[i][passenger] == bus:
                    carriage.append(passenger + 1)
            if len(carriage) == 1:
                mark = True
            list_carriage.append(carriage)
        if not_lack_buses == False:
            list_carriages.append(list_carriage)
        else:
            if mark == False:
                list_carriages.append(list_carriage)
    return list_carriages

def generate_matrix(list_carriage, matrix):
    res = list()
    num_buses = len(list_carriage)
    num_passengers = int((len(matrix) - 1) / 2)
    for bus in range(num_buses):
        carri = list_carriage[bus]
        carriage = copy.deepcopy(carri)
        for c in range(1, len(carri)):
            carriage.append(carri[c] + num_passengers)
        mat_bus = list()
        if len(carriage) != 1:
            carriage.sort(key = lambda x: x)
            # print(f"Carriage: {carriage}")
            for row in carriage:
                lis = list()
                for col in carriage:
                    lis.append(matrix[row][col])
                mat_bus.append(lis)
                
        res.append(mat_bus)
    return res


def optimal_path(num_cities, matrix):
    res = list()
    num_startcities = int(num_cities / 2)

    def invariant_TSP(num_cities, num_startcities, mat, seen_cities = list(), prev_city = 0, configuration = [0], cost = 0):
        for city in range(1, num_cities+1):
            if city not in seen_cities: # check if bus has seen the city or not
                if city > num_startcities: # check if city is depot or not
                    start_city = city - num_startcities
                    if start_city not in seen_cities:
                        # check if starting point in seen_cities or not
                        continue
                
                new_cost = cost + mat[prev_city][city]
                seen_cities.append(city)
                configuration.append(city)
                
                if len(configuration) == num_cities + 1:
                    configuration.append(0)
                    new_cost = new_cost + mat[city][0]
                    # print(f"Configuration: {configuration}")
                    res.append([new_cost, configuration])
                    break
                
                else:
                    new_seen_cities = copy.deepcopy(seen_cities)
                    new_configuration = copy.deepcopy(configuration)
                    invariant_TSP(num_cities, num_startcities, mat, new_seen_cities, city, new_configuration, new_cost)
                    seen_cities = seen_cities[:-1]
                    configuration = configuration[:-1]
                
    invariant_TSP(num_cities, num_startcities, matrix)
    res.sort(key = lambda x: x[0])
    return res[0]