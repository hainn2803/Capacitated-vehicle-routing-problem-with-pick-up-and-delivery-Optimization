"""
    Created by @namhainguyen2803 in 02/02/2023.
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

def random_configuration(num_buses, num_passengers):
    
    def random_conf(num_buses, num_passengers):
        configuration = defaultdict(lambda: [0])
        for passenger in range(num_passengers):
            bus = np.random.choice(num_buses, 1)[0]
            configuration[bus+1].append(passenger+1)
            configuration[bus+1].append(passenger+1+num_passengers)
        return configuration
    
    def uniform_random_conf(num_buses, num_passengers):
        
        configuration = defaultdict(lambda: [0])
        arr = np.arange(1, num_passengers+1)
        np.random.shuffle(arr)
        split_passengers = np.array_split(arr, num_buses)
        for bus in range(num_buses):
            single_conf = split_passengers[bus].tolist()
            for passenger in split_passengers[bus]:
                single_conf.append(passenger + num_passengers)
            configuration[bus+1].extend(sorted(single_conf))
        return configuration
            
    
    confs = random_conf(num_buses, num_passengers)
    uniform_confs = uniform_random_conf(num_buses, num_passengers)
    
    return uniform_confs

def generate_distance_matrix(matrix_dist, list_passengers):
    
    return matrix_dist[list_passengers, :][:, list_passengers]

def decode_cities(list_passengers, config):
    new_config = list()
    for c in range(len(config)):
        new_config.append(list_passengers[config[c]])
    return new_config

# Data sample
# matrix_distance = np.array([[0, 7, 7, 7, 6, 7, 7, 9, 7, 7, 9],
#                             [5, 0, 6, 5, 8, 7, 5, 5, 8, 8, 8], 
#                             [7, 8, 0, 8, 9, 7, 8, 7, 7, 6, 9], 
#                             [8, 8, 9, 0, 6, 8, 9, 5, 8, 8, 5], 
#                             [5, 6, 6, 9, 0, 7, 6, 9, 5, 8, 9],
#                             [6, 9, 8, 6, 5, 0, 6, 7, 6, 5, 9], 
#                             [8, 9, 7, 7, 6, 6, 0, 7, 6, 9, 5], 
#                             [5, 6, 7, 8, 8, 8, 7, 0, 9, 5, 6], 
#                             [6, 5, 9, 8, 7, 8, 6, 8, 0, 9, 7], 
#                             [6, 6, 9, 5, 8, 5, 6, 5, 8, 0, 8], 
#                             [7, 6, 9, 7, 5, 5, 5, 8, 7, 5, 0]])


if __name__ == "__main__":
    num_cities = 15
    num_buses = 3
    buses_capacities = [2,3,3]

    matrix_distance = np.array(generate_sample.generate_sample(num_cities)[0])
    num_passengers = int((len(matrix_distance) - 1) / 2)

    dict_schedules = random_configuration(num_buses, num_passengers)
    print(f"Number of cities: {num_cities}")
    print(f"Number of passengers: {num_passengers}")
    print(f"Number of buses: {num_buses}")
    opti_cost = 1e9
    lst_cost = list()
    opti_start_time = time.time()
    lst_schedule = branch_bound.generate_schedule_for_buses(num_buses, num_passengers)
    for i in range(len(lst_schedule)):
        schedule = lst_schedule[i]
        sub_opti_cost = 0
        for bus in range(num_buses):
            dist_matr = generate_distance_matrix(matrix_distance, schedule[bus+1])
            sub_opti_cost += branch_bound.optimal_path(dist_matr, buses_capacities[bus])[0]
        lst_cost.append(sub_opti_cost)
        if opti_cost > sub_opti_cost:
            opti_cost = sub_opti_cost
    opti_end_time = time.time()
    print(f"Optimal cost: {opti_cost}, time: {round(opti_end_time - opti_start_time, 4)}")
    # print(f"List cost: {lst_cost}")
    branch_bound_cost = 0
    greedy_cost = 0
    hill_climbing_cost = 0
    uc_cost = 0
    randomized_travel_cost = 0
    beam_cost = 0
    ga_cost = 0

    branch_bound_start_time = time.time()
    for id_bus, schedule in dict_schedules.items():
        # Generate matrix distance of id_bus
        matrix_dist_of_a_bus = generate_distance_matrix(matrix_distance, schedule)
        num_cities = np.shape(matrix_dist_of_a_bus)[0]
        # Branching bound algorithm
        bb = branch_bound.optimal_path(matrix_dist_of_a_bus, buses_capacities[id_bus-1])
        branch_bound_cost += bb[0]
        opti_schedule = decode_cities(schedule, bb[1])
        # print(f"Bus ID {id_bus}, schedule: {opti_schedule}")
    time_branch_bound = time.time() - branch_bound_start_time
    print(f"Branch and bound (modified version) algorithm, cost: {branch_bound_cost}, time: {round(time_branch_bound, 4)} second")    

    greedy_start_time = time.time()
    for id_bus, schedule in dict_schedules.items():
        # Generate matrix distance of id_bus
        matrix_dist_of_a_bus = generate_distance_matrix(matrix_distance, schedule)
        num_cities = np.shape(matrix_dist_of_a_bus)[0]
        # Greedy algorithm
        Greedy = greedy.Greedy_Search_Graph(num_cities, matrix_dist_of_a_bus, buses_capacities[id_bus-1])
        gd = Greedy.greedy_search()
        greedy_cost += gd[0]
        opti_schedule = decode_cities(schedule, gd[1])
        # print(f"Bus ID {id_bus}, schedule: {opti_schedule}")
    time_greedy = time.time() - greedy_start_time
    print(f"Greedy algorithm, cost: {greedy_cost}, time: {round(time_greedy, 4)} second")    

    hl_start_time = time.time()
    for id_bus, schedule in dict_schedules.items():
        # Generate matrix distance of id_bus
        matrix_dist_of_a_bus = generate_distance_matrix(matrix_distance, schedule)
        num_cities = np.shape(matrix_dist_of_a_bus)[0]
        # (Metaheuristic) Hill Climbing algorithm
        Hill_Climbing = hill_climbing.Graph_Hill_Climbing(num_cities, matrix_dist_of_a_bus, buses_capacities[id_bus-1])
        hl = Hill_Climbing.Metaheuristic_Hill_Climbing()
        hill_climbing_cost += hl[0]
        opti_schedule = decode_cities(schedule, hl[1])
        # print(f"Bus ID {id_bus}, schedule: {opti_schedule}")
    time_hl = time.time() - hl_start_time
    print(f"Metaheuristic Hill Climbing algorithm, cost: {hill_climbing_cost}, time: {round(time_hl, 4)} second")    
        
    uc_start_time = time.time()
    for id_bus, schedule in dict_schedules.items():
        # Generate matrix distance of id_bus
        matrix_dist_of_a_bus = generate_distance_matrix(matrix_distance, schedule)
        num_cities = np.shape(matrix_dist_of_a_bus)[0]
        # Uniform cost algorithm
        Uniform_Cost = uniform_cost.Uniform_Cost_Search_Graph(num_cities, matrix_dist_of_a_bus, buses_capacities[id_bus-1])
        uc = Uniform_Cost.uniform_cost_search()
        uc_cost += uc[0]
        opti_schedule = decode_cities(schedule, uc[1])
        # print(f"Bus ID {id_bus}, schedule: {opti_schedule}")
    time_uc = time.time() - uc_start_time
    print(f"Uniform cost search algorithm, cost: {uc_cost}, time: {round(time_uc, 4)} second")    

    beam_start_time = time.time()
    for id_bus, schedule in dict_schedules.items():
        # Generate matrix distance of id_bus
        matrix_dist_of_a_bus = generate_distance_matrix(matrix_distance, schedule)
        num_cities = np.shape(matrix_dist_of_a_bus)[0]
        # Beam search algorithm
        Beam_Search = beam_search.Beam_Search_Graph(num_cities, matrix_dist_of_a_bus, buses_capacities[id_bus-1])
        beam = Beam_Search.beam_search()
        beam_cost += beam[0]
        opti_schedule = decode_cities(schedule, beam[1])
        # print(f"Bus ID {id_bus}, schedule: {opti_schedule}")
    time_beam = time.time() - beam_start_time
    print(f"Beam search algorithm, cost: {beam_cost}, time: {round(time_beam, 4)} second")    
        
    randomize_start_time = time.time()
    for id_bus, schedule in dict_schedules.items():
        # Generate matrix distance of id_bus
        matrix_dist_of_a_bus = generate_distance_matrix(matrix_distance, schedule)
        num_cities = np.shape(matrix_dist_of_a_bus)[0]
        # Randomized travel algorithm
        Randomize = randomized_travel.Randomized_Travel(num_cities, matrix_dist_of_a_bus, buses_capacities[id_bus-1])
        rt= Randomize.randomized_travel(num_examples=100)
        randomized_travel_cost += rt[0]
        opti_schedule = decode_cities(schedule, rt[1])
        # print(f"Bus ID {id_bus}, schedule: {opti_schedule}")
    time_randomize = time.time() - randomize_start_time
    print(f"Randomized travel algorithm, cost: {randomized_travel_cost}, time: {round(time_randomize, 4)} second")    
        
    ga_start_time = time.time()
    for id_bus, schedule in dict_schedules.items():
        # Generate matrix distance of id_bus
        matrix_dist_of_a_bus = generate_distance_matrix(matrix_distance, schedule)
        num_cities = np.shape(matrix_dist_of_a_bus)[0]
        # Genetic algorithm
        ga = gene.Genetic_Algorithm(num_cities, matrix_dist_of_a_bus, buses_capacities[id_bus-1])
        GA = ga.random_travel_2()
        ga_cost += GA[0]
        opti_schedule = decode_cities(schedule, GA[1])
        # print(f"Bus ID {id_bus}, schedule: {opti_schedule}")
    time_ga = time.time() - ga_start_time
    print(f"Genetic algorithm, cost: {ga_cost}, time: {round(time_ga, 4)} second")    
        
        
    # print(f"Branch and bound algorithm: {branch_bound_cost}")
    # print(f"Greedy algorithm: {greedy_cost}")
    # print(f"Metaheuristic hill climbing: {hill_climbing_cost}")
    # print(f"Uniform cost search: {uc_cost}")
    # print(f"Beam search: {beam_cost}")
    # print(f"Randomized travel: {randomized_travel_cost}")
    # print(f"Genetic algorithm: {ga_cost}")
    # print(CP.CP_algorithm(num_cities, num_buses, buses_capacities, matrix_distance))