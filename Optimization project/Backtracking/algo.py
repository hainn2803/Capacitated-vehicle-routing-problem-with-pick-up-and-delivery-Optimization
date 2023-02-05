"""
    Created by @namhainguyen2803 on 02/02/2023.
"""

import copy
import numpy as np
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

# Testing
if __name__ == "__main__":  
    matrix_distance=[[0, 3, 2, 4, 3],
                    [4, 0, 5, 3, 2],
                    [2, 1, 0, 6, 4],
                    [1, 1, 3, 0, 5],
                    [3, 4, 5, 3, 0]]  
    num_cities = len(matrix_distance) - 1
    r = optimal_path(num_cities, matrix_distance) 
    print(r)
            
            