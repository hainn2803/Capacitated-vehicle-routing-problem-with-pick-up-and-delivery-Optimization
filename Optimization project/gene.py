"""
    Created by @namhainguyen2803 in 03/02/2023.
"""
import copy 
import random
import numpy as np
from collections import defaultdict
import time
from collections import deque

class Genetic_Algorithm():
    def __init__(self, num_vertices, distance_matrix, capacity):
        self.num_vertices = num_vertices
        self.vertices = [i for i in range(num_vertices)]
        self.distance_matrix = distance_matrix
        self.num_passengers = (num_vertices-1)//2
        self.capacity = capacity
    
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
    
    def check_valid(self, config):
        cap = 0
        for i in range(1,len(config)):
            if config[i] > self.num_passengers:
                cap -= 1
            else:
                cap += 1
            if cap > self.capacity:
                return False
            if config[i] > self.num_passengers:
                if config[i] - self.num_passengers not in config:
                    return False
        return True
    
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
    
    def breeding(self, parent_1, parent_2):
        child = []
        childP1 = []
        childP2 = []
        geneA = np.random.choice(np.arange(1, len(parent_1)-1), 1)[0]
        geneB = np.random.choice(np.arange(1, len(parent_1)-1), 1)[0]
        if geneA < geneB :
            startGene, endGene = geneA, geneB
        else :
            endGene, startGene = geneA, geneB
        for i in range(startGene, endGene):
            childP1.append(parent_1[i])
        childP2 = [item for item in parent_2 if item not in childP1]
        child1 = childP1 + childP2
        child2 = self.satisfied_configuration(child1)
        return child1, child2
    
    def selection(self, parent):
        list_node = [i for i in range(1, self.num_vertices)]
        new_child = list()
        pos = np.random.choice(np.arange(1, len(parent)-1), 1)[0]
#         print(pos)
        for chromosome in range(pos+1):
            new_child.append(parent[chromosome])
        while len(new_child) != len(parent) - 1:
            possible_next_chromosomes = self.children(list_node, new_child)
            next_chromosomes = np.random.choice(possible_next_chromosomes, 1)[0]
#             print(possible_next_chromosomes, next_chromosomes)
            new_child.append(next_chromosomes)
        new_child.append(0)
        return new_child
    
    def mutation(self, config):
        check_list = [[0,0] for j in range(self.num_passengers)]
        new_config = [0] * len(config)
        
        for city in range(1,len(config)-1):
            city_id = config[city]
            if city_id > self.num_passengers:
                check_list[city_id - self.num_passengers-1][1] = city
            else:
                check_list[city_id-1][0] = city
#         print(f"list before: {check_list}")
        chromosome_1 = np.random.randint(0,len(check_list)-1)
        chromosome_2 = np.random.randint(0,len(check_list)-1)
        check_list = self.swap_positions(check_list, chromosome_1, chromosome_2)
#         print(f"list after: {check_list}")
        for ind_chromosome in range(len(check_list)):
            new_config[check_list[ind_chromosome][0]] = ind_chromosome + 1
            new_config[check_list[ind_chromosome][1]] = ind_chromosome + self.num_passengers + 1
        return new_config
    
        
    def children(self, list_node, state):
        current_seat = self.compute_capacity(state)
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
    
    def generate_valid_state(self):
        state = [0]
        list_node = [i for i in range(1, self.num_vertices)]
        current_seat = 0
        while len(self.children(list_node, state)) != 0:
            list_next_cities = self.children(list_node, state)
            next_city = np.random.choice(list_next_cities, 1)[0]
            if next_city != 0:
                if next_city > self.num_passengers:
                    current_seat -= 1
                else:
                    current_seat += 1
            state.append(next_city)
        state.append(0)
        return state
    
    def random_travel_2(self, max_iter=10, num_genes=40, epsilon_1=0.4, num_elites=5):
        list_genes = list()
        while len(list_genes) != num_genes:
            initial_gene = self.generate_valid_state()
            list_genes.append([initial_gene, self.compute_path(initial_gene)])
        list_elites = list()
        list_genes.sort(key=lambda x: x[1])
        list_elites = copy.deepcopy(list_genes[:num_elites])
        current_opti_cost = 0
        current_opti_config = list()
        cnt = 0
        i = 0
        while i < max_iter:
            prev_opti_cost = list_elites[0][1]
            i += 1
            j = 0
            list_new_genes = list()
            while j < num_genes//4:
                j += 1
                for elite in list_elites:
                    prob = random.random()
                    if prob >= epsilon_1:
                        new_child = self.selection(elite[0])
                        child_cost = self.compute_path(new_child)
                        list_new_genes.append([new_child, child_cost])
                    else:
                        new_child = self.mutation(elite[0])
                        child_cost = self.compute_path(new_child)
                        list_new_genes.append([new_child, child_cost])
#                     else:
#                         cnt += 1
#                         p1 = np.random.choice(np.arange(len(list_elites)), 1)[0]
#                         p2 = np.random.choice(np.arange(len(list_elites)), 1)[0]
#                         new_child1, new_child2 = self.breeding(list_elites[p1][0], list_elites[p2][0])
#                         child1_cost = self.compute_path(new_child1)
#                         child2_cost = self.compute_path(new_child2)
#                         list_new_genes.append([new_child1, child1_cost])
#                         list_new_genes.append([new_child2, child2_cost])
#                         print(f"Count {cnt}, child_2: {new_child2}, cost: {child2_cost}")
            list_new_genes.sort(key=lambda x: x[1])
            list_elites.extend(list_new_genes[:num_elites])
            list_elites.sort(key=lambda x: x[1])
            list_elites = copy.deepcopy(list_elites[:num_elites])
            
            
            current_opti_cost = list_elites[0][1]
            current_opti_config = list_elites[0][0]
            # terminal condition if max_iter is large
#             if prev_opti_cost == current_opti_cost:
#                 cnt += 1
#             if cnt == 3:
#                 break
        return current_opti_cost, current_opti_config