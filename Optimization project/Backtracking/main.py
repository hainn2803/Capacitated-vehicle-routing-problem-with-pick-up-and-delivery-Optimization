"""
    Created by @namhainguyen2803 on 02/02/2023.
"""

import algo
import generate
import copy 
import generate_data



matrix_distance = [[0,7,7,5,7,5.6,7],
                             [7,0,10,11.2,10,10.3,14],
                             [7,10,0,5,14,2.5,10],
                             [5,11.2,5,0,11.2,2.5,5],
                             [7,10,14,11.2,0,12.5,10],
                             [5.6,10.3,2.5,2.5,12.5,0,7.5],
                             [7,14,10,5,10,7.5,0]]
num_capacity = [2,3]
num_buses = 2

# data = generate_data.generate_sample(13)
# matrix_distance = data[0]
# num_buses = data[1]

print(f"Distance matrix: {matrix_distance}")
print(f"Number of buses: {num_buses}")

num_passengers = int((len(matrix_distance) - 1) / 2)

carriages = generate.generate_carriages(num_buses, num_passengers, True)

cnt = 0
optimal_cost = 1e9
optimal_path = list()
for carriage in carriages:
    info = list()
    cnt += 1
    mat_buses = generate.generate_matrix(carriage, matrix_distance)
    # print(f"Iteration {cnt}: ")
    total_cost = 0
    for num_bus in range(len(mat_buses)):
        num_cities = len(mat_buses[num_bus]) - 1
        res = algo.optimal_path(num_cities, mat_buses[num_bus])
        total_cost = total_cost + res[0]
        priority_arrange = res[1][:-1]
        list_passengers = carriage[num_bus]
        list_cities = copy.deepcopy(list_passengers)
        for c in range(1, len(list_passengers)):
            list_cities.append(list_passengers[c] + num_passengers)
        path = [0] * len(list_cities)
        for p in range(len(priority_arrange)):
            path[p] = list_cities[priority_arrange[p]]
        path.append(0)
        # print(f"Bus number {num_bus+1} has the path: {path}, the cost is: {res[0]}")
        info.append([num_bus, path, res[0]])
    # print(f"Total cost: {total_cost}")
    if total_cost < optimal_cost:
        
        optimal_cost = total_cost
        optimal_path = copy.deepcopy(info)
        
for optimal in optimal_path:
    print(f"Bus number {optimal[0]+1} has the path: {optimal[1]}, the cost is: {optimal[2]}")
print(f"Optimal cost: {optimal_cost}")
        