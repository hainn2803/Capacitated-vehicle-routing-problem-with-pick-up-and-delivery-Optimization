import copy 
import random
import numpy as np
from collections import defaultdict
import time
from collections import deque

class Beam_Search_Graph():
    def __init__(self, num_vertices, distance_matrix, capacity):
        self.num_vertices = num_vertices
        self.edges = list()
        self.vertices = [i for i in range(num_vertices)]
        self.num_edges = None
        self.distance_matrix = distance_matrix
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
    
    def compute_path(self, config):
        for i in range(1,len(config)):
            if self.compute_capacity(config[:i]) > self.capacity:
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
        
    def compute_capacity(self, configuration):
        capp = 0
        for conf in configuration:
            if conf != 0:
                if conf > self.num_passengers:
                    capp -= 1
                else:
                    capp += 1
        return capp
    
    def compute_capacity(self, configuration):
        capp = 0
        for conf in configuration:
            if conf != 0:
                if conf > self.num_passengers:
                    capp -= 1
                else:
                    capp += 1
        return capp
    
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
                
    
    def choose_node(self, frontier):
        idx = 0
        if frontier[0][0] == 0:
            frontier.sort(key= lambda x: x[1])
            parent = frontier[0]
            return parent
        
        else:
            frontier.sort(key= lambda x: x[1])
            if self.current_seat >= self.capacity:
                i = 0
                while frontier[i][0] <= self.num_passengers:
                    i += 1

                parent = frontier[i]
                idx = i
            else:
                parent = frontier[0]
                idx = 0
            return parent
        
    def heuristic_greedy_function(self, child, parent):
        return self.distance_matrix[parent][child]
        
    def children(self, node, current_state):
        list_node = self.vertices
        current_seat = self.compute_capacity(current_state)
        res = list()
        for n in list_node:
            if n not in current_state:
                if current_seat >= self.capacity:
                    if n > self.num_passengers:
                        if n - self.num_passengers in current_state:
                            res.append(n)
                else:
                    if n > self.num_passengers:
                        if n - self.num_passengers in current_state:
                            res.append(n)
                        else:
                            continue
                    else:
                        res.append(n)
        return res
        
    def beam_search(self, num_chosen_nodes=3):
        beam_searh_cost = 1e9
        parent_frontier = list()
        parent_frontier.append([0, 0, [0]])
        children_frontier = list()
        res = list()
        
        while True:
            # print(f"Parent frontier: {parent_frontier}")
            while len(parent_frontier) != 0:
                parent = parent_frontier[0]
                parent_state = parent[2]
                if len(parent_state) == self.num_vertices:
                    res.append(parent_state)
                new_frontier = list()
                for child in self.children(parent[0], parent_state):
                    cost_child = self.heuristic_greedy_function(child, parent[0])
                    child_state = copy.deepcopy(parent_state)
                    child_state.append(child)
                    if self.check_valid(child_state) == True:
                        new_frontier.append([child, cost_child, child_state])
                    else:
                        print("hello")
                children_frontier.extend(new_frontier)
                del parent_frontier[0]
            # print(f"Children frontier 2: {children_frontier}")
            if len(children_frontier) == 0:
                break
            children_frontier.sort(key=lambda x: x[1])
            parent_frontier = copy.deepcopy(children_frontier[:num_chosen_nodes])
            children_frontier = list()
        
        for r in res:
            r.append(0)
            cost_search = self.compute_path(r)
            if beam_searh_cost > cost_search:
                beam_searh_cost = cost_search
                opti_path = r
            
        return beam_searh_cost, opti_path