"""
    Created by @namhainguyen2803 in 04/02/2023.
"""
import copy 
import random
import numpy as np
from collections import defaultdict
import time
from collections import deque
import generate_sample
# from ortools.sat.python import cp_model
import time
import preprocess_data
from main import *
import kmeans

# Import algorithms
import branch_bound
import greedy
import hill_climbing
import uniform_cost
import randomized_travel
import beam_search
import greedy_2
# import CP
import gene

if __name__ == "__main__":
    
    num_cities = 63
    # It should be less than 9 buses because of not enough color to represent the path of each bus
    num_buses = 4
    buses_capacities = [4,4,5,5]
    matrix_distance = preprocess_data.create_matrix_distance()
    num_passengers = int((len(matrix_distance) - 1) / 2)
    km = kmeans.K_Means(k=num_buses)
    lst = preprocess_data.convert_4d_vectors()
    km.fit(lst)
    dict_schedules = preprocess_data.convert_4d_vectors_to_passengers(km.classes)

    beam_cost = 0
    list_config = list()
    with open("schedule.txt", "w") as f:
        for id_bus, schedule in dict_schedules.items():
            f.write("<=============" + str(id_bus) + "=============>")
            f.write("\n")
            f.write(f"Depot: {preprocess_data.Cities[schedule[0]]}")
            f.write("\n")
            print("<=============", id_bus, "=============>")
            print(f"Depot: {preprocess_data.Cities[schedule[0]]}")
            for i in range(len(schedule)):
                if schedule[i] != 0:
                    if schedule[i] <= num_passengers:
                        f.write(str(preprocess_data.Cities[schedule[i]])+ " --> "+ str(preprocess_data.Cities[schedule[i]+num_passengers]))
                        f.write("\n")
                        print(preprocess_data.Cities[schedule[i]], "-->", preprocess_data.Cities[schedule[i]+num_passengers])
    beam_start_time = time.time()
    for id_bus, schedule in dict_schedules.items():
        print("<=============", id_bus, "=============>")
        # Generate matrix distance of id_bus
        matrix_dist_of_a_bus = generate_distance_matrix(matrix_distance, schedule)
        num_cities = np.shape(matrix_dist_of_a_bus)[0]
        # Beam search algorithm
        Beam_Search = beam_search.Beam_Search_Graph(num_cities, matrix_dist_of_a_bus, buses_capacities[id_bus-1])
        beam = Beam_Search.beam_search()
        beam_cost += beam[0]
        opti_schedule = decode_cities(schedule, beam[1])
        list_config.append(opti_schedule)
        print(f"Bus ID {id_bus}, schedule: {preprocess_data.decode_configuration_provinces(opti_schedule)}")
    time_beam = time.time() - beam_start_time
    print(f"Beam search algorithm, cost: {beam_cost}, time: {round(time_beam, 4)} second")    
    preprocess_data.plot_solution(list_config) 
    
    
    
    # dict_schedules_2 = random_configuration(num_buses, num_passengers)
    # beam_cost = 0
    # list_config = list()
    # beam_start_time = time.time()
    # for id_bus, schedule in dict_schedules_2.items():
    #     # Generate matrix distance of id_bus
    #     matrix_dist_of_a_bus = generate_distance_matrix(matrix_distance, schedule)
    #     num_cities = np.shape(matrix_dist_of_a_bus)[0]
    #     # Beam search algorithm
    #     Beam_Search = beam_search.Beam_Search_Graph(num_cities, matrix_dist_of_a_bus, buses_capacities[id_bus-1])
    #     beam = Beam_Search.beam_search()
    #     beam_cost += beam[0]
    #     opti_schedule = decode_cities(schedule, beam[1])
    #     list_config.append(opti_schedule)
    # time_beam = time.time() - beam_start_time
    # print(f"Beam search algorithm, cost: {beam_cost}, time: {round(time_beam, 4)} second")    
