"""
    Created by @namhainguyen2803 on 02/02/2023.
"""

import copy

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
