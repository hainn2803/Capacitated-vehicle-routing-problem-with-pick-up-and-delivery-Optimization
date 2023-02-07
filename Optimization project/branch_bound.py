"""
    Created by @namhainguyen2803 in 02/02/2023.
"""
import copy 
import random
import numpy as np
from collections import defaultdict
import time
from collections import deque

def generate_schedule_for_buses(num_buses, num_passengers):
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
    Try(num_buses, num_passengers)
    ree = list()
    for r in range(len(res)):
        cnt = 0
        for b in range(1, num_buses+1):
            if b in res[r]:
                cnt += 1
        if cnt == num_buses:
            ree.append(res[r])
    schedule = list()
    for rr in range(len(ree)):
        dic = defaultdict(lambda: [0])
        for city in range(len(ree[rr])):
            dic[ree[rr][city]].append(city+1)
            dic[ree[rr][city]].append(city+1+num_passengers)
        dic[ree[rr][city]].sort()
        schedule.append(dic)  
    return schedule


def optimal_path(distance_matrix, capacity):
    res = list()
    num_cities = np.shape(distance_matrix)[0] - 1
    num_passengers = num_cities//2
    optimal_cost = 1e9
    optimal_configuration=list()
    if num_passengers == 0:
        return 0, [0]
    else:
        shortest_weight = 1e9
        for row in range(np.shape(distance_matrix)[0]):
            for col in range(np.shape(distance_matrix)[1]):
                if row != col:
                    if shortest_weight > distance_matrix[row][col]:
                        shortest_weight = distance_matrix[row][col]
        
        def optimistic_cost(cities, cost):
            return shortest_weight * (num_cities - len(cities)) + cost
        cnt = 0
        def capacitied_vehicle_routing(num_cities=num_cities, num_passengers=num_passengers, dist_matrix=distance_matrix, seen_cities=[0], configuration=[0], cost=0, prev_city=0, current_seat=0):
            nonlocal optimal_cost
            nonlocal optimal_configuration
            nonlocal cnt
            if optimal_cost < optimistic_cost(seen_cities, cost):
                cnt += 1
                return
            for city in range(1, num_cities+1):
                if city not in seen_cities: # check if the bus has seen city or not 
                    if city > num_passengers: # check if city destination location
                        pickup = city - num_passengers
                        if pickup not in seen_cities: # passenger not in bus
                            continue # configuration is dropped
                        else: # passenger in bus
                            new_cost = cost + dist_matrix[prev_city][city]
                            seen_cities.append(city)
                            configuration.append(city)
                            current_seat = current_seat - 1

                            # check for stopping condition
                            if len(configuration) == num_cities + 1:
                                configuration.append(0)
                                new_cost = new_cost + dist_matrix[city][0]
                                if optimal_cost > new_cost:
                                    optimal_cost = new_cost
                                    optimal_configuration = copy.deepcopy(configuration)
                                res.append([new_cost, configuration])
                                break

                            else:
                                new_seen_cities = copy.deepcopy(seen_cities)
                                new_configuration = copy.deepcopy(configuration)
                                capacitied_vehicle_routing(num_cities, num_passengers, dist_matrix, new_seen_cities, new_configuration, new_cost, city, current_seat)
                                seen_cities = seen_cities[:-1]
                                configuration = configuration[:-1]
                                current_seat = current_seat + 1
                                
                            
                    else: # city is pickup location
                        if current_seat >= capacity: # not enough seats for passenger
                            continue
                        else:
                            new_cost = cost + dist_matrix[prev_city][city]
                            seen_cities.append(city)
                            configuration.append(city)
                            current_seat = current_seat + 1
                            
                            # check for stopping condition
                            if len(configuration) == num_cities + 1:
                                configuration.append(0)
                                new_cost = new_cost + dist_matrix[city][0]
                                if optimal_cost > new_cost:
                                    optimal_cost = new_cost
                                    optimal_configuration = copy.deepcopy(configuration)
                                res.append([new_cost, configuration])
                                break

                            else:
                                new_seen_cities = copy.deepcopy(seen_cities)
                                new_configuration = copy.deepcopy(configuration)
                                capacitied_vehicle_routing(num_cities, num_passengers, dist_matrix, new_seen_cities, new_configuration, new_cost, city, current_seat)
                                current_seat = current_seat - 1
                                seen_cities = seen_cities[:-1]
                                configuration = configuration[:-1]

                else:
                    continue
        capacitied_vehicle_routing()
        print(cnt)
        return optimal_cost, optimal_configuration, cnt
    
if __name__ == "__main__":
    print(generate_schedule_for_buses(3, 6))