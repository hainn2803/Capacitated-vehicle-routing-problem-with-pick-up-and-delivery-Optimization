"""
    Created by @namhainguyen2803 in 02/02/2023.
"""
import copy 
import random
import numpy as np
from collections import defaultdict
import time
from collections import deque

class Graph_Hill_Climbing():
    def __init__(self, num_vertices, distance_matrix, capacity):
        self.num_vertices = num_vertices
        self.edges = list()
        self.vertices = [i for i in range(num_vertices)]
        self.num_edges = None
        self.frontier = list()
        self.explored_set = list()
        self.distance_matrix = distance_matrix
        self.visited = [False for i in range(num_vertices)]
        self.cost = [0 for i in range(num_vertices)]
        self.ancestor = [0 for i in range(num_vertices)]
        self.num_passengers = (num_vertices-1)//2
        self.capacity = capacity
        
    def update_edges(self):
        for row in range(np.shape(self.distance_matrix)[0]):
            row_edges = list()
            for col in range(np.shape(self.distance_matrix)[1]):
                if row == col:
                    row_edges.append([row, col, 1e9])
                else:
                    row_edges.append([row, col, self.distance_matrix[row][col]])
            self.edges.append(row_edges)
    
    def check_capacity(self, config):
        cap = 0
        for i in range(1,len(config)):
            if config[i] > self.num_passengers:
                cap -= 1
            else:
                cap += 1
            if cap > self.capacity:
                return False
        return True
    
    def compute_path(self, config):
        if self.check_capacity(config) == False:
            return 1e9
        else:
            cost = 0
            explore = list()
            for city in range(len(config)-1):
                explore.append(config[city+1])
                cost += self.distance_matrix[config[city]][config[city+1]]
                if config[city+1] > self.num_passengers:
                    if config[city+1] - self.num_passengers not in explore:
                        return 1e9
            return cost
    
    def initialize_configuration(self):
        init_config = np.arange(1, self.num_vertices)
        np.random.shuffle(init_config)
        init_c = init_config.tolist()
        init_c.insert(0, 0)
        init_c.append(0)
        self.explored_set = init_c
        return init_c
    
    def swap_positions(self, lis, pos1, pos2):
        lis[pos1], lis[pos2] = lis[pos2], lis[pos1]
        return lis
    
    def compute_capacity(self, configuration):
        capp = 0
        for conf in configuration:
            if conf != 0:
                if conf > self.num_passengers:
                    capp -= 1
                else:
                    capp += 1
        return capp
    
    def satisfied_configuration(self, config):
        check_list = [[0,0] for j in range(self.num_passengers)]
        new_config = copy.deepcopy(config)
        
        for city in range(1,len(config)-1):
            city_id = config[city]
            if city_id > self.num_passengers:
                check_list[city_id - self.num_passengers-1][1] = city
            else:
                check_list[city_id-1][0] = city

        for location in check_list:
            if location[0] > location[1]: # swap
                new_config = self.swap_positions(new_config, location[0], location[1])
        return new_config
    
    def get_neighbours(self, init_config):
        neighbours = []
        for i in range(1,len(init_config)-1):
            for j in range(i + 1, len(init_config)-1):
                neighbour = init_config.copy()
                neighbour[i] = init_config[j]
                neighbour[j] = init_config[i]
                neighbour = self.satisfied_configuration(neighbour)
                if self.check_capacity(neighbour) == True:
                    neighbours.append(neighbour)
        return neighbours
    
    def Hill_Climbing(self, max_iter=10):
        init_state = self.generate_valid_state()
        neighbours = self.get_neighbours(init_state)
        best_cost = 1e9
        best_neighbour = init_state
        i = 0
        while i < max_iter:
            i += 1
            prev_cost = best_cost
            neighbours = self.get_neighbours(best_neighbour)
            for neighbour in neighbours:
                current_cost = self.compute_path(neighbour)
                if current_cost < best_cost:
                    best_cost = current_cost
                    best_neighbour = neighbour
                    
            if prev_cost == best_cost and best_cost < 1e9:
                break
        
        return best_cost, best_neighbour
    
    def Metaheuristic_Hill_Climbing(self, num_play=2, max_iter=10):
        sub_opt_cost = 1e9
        sub_opt_config = list()
        while sub_opt_cost >= 1e9:
            for play in range(num_play):
                cost, config = self.Hill_Climbing(max_iter)
                if cost < sub_opt_cost:
                    sub_opt_cost = cost
                    sub_opt_config = config
                # print(f"Iteration {play + 1}, cost: {cost}")
            
        return sub_opt_cost, sub_opt_config
    
    
    def generate_valid_state(self):
        state = [0]
        list_node = [i for i in range(1, self.num_vertices)]
        current_seat = 0
        def children(node, list_node, current_seat):
            res = list()
            for n in list_node:
                if n not in state:
                    if current_seat == self.capacity:
                        if n > self.num_passengers:
                            if n - self.num_passengers in state:
                                res.append(n)
                    else:
                        if n > self.num_passengers:
                            if n - self.num_passengers in state:
                                res.append(n)
                            else:
                                continue
                        else:
                            res.append(n)
            return res
        while len(children(state[-1], list_node, current_seat)) != 0:
            list_next_cities = children(state[-1], list_node, current_seat)
#             print(f"Current city: {state[-1]}, list next possible cities: {list_next_cities}")
            next_city = np.random.choice(list_next_cities, 1)[0]
            if next_city > self.num_passengers:
                current_seat -= 1
            else:
                current_seat += 1
            state.append(next_city)
        state.append(0)
        return state