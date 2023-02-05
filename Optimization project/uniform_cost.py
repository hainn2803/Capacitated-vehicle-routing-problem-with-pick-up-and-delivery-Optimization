"""
    Created by @namhainguyen2803 in 02/02/2023.
"""
import copy 
import random
import numpy as np
from collections import defaultdict
import time
from collections import deque

class Uniform_Cost_Search_Graph():
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
        self.current_seat = 0
        
    def update_edges(self):
        for row in range(np.shape(self.distance_matrix)[0]):
            row_edges = list()
            for col in range(np.shape(self.distance_matrix)[1]):
                if row == col:
                    row_edges.append([row, col, 1e9])
                else:
                    row_edges.append([row, col, self.distance_matrix[row][col]])
            self.edges.append(row_edges)
    
    def children(self, node):
        if node == 0: # depot point
            res = list()
            for n in self.vertices:
                if self.visited[n] == False:
                    if n > self.num_passengers:
                        if self.visited[n - self.num_passengers] == True:
                            res.append(n)
                        else:
                            continue
                    else:
                        res.append(n)
            return res
        
        elif node <= self.num_passengers: # pickup point
            res = list()
            for n in self.vertices:
                if self.visited[n] == False:
                    if n > self.num_passengers:
                        if self.visited[n - self.num_passengers] == True:
                            res.append(n)
                        else:
                            continue
                    else:
                        res.append(n)
            return res
            
        else: # destination point
            res = list()
            for n in self.vertices:
                if self.visited[n] == False:
                    if n > self.num_passengers: # n is destination point
                        if self.visited[n - self.num_passengers] == True: # if have visited pickup point yet
                            res.append(n)
                        else:
                            continue
                    else:
                        res.append(n)
            return res
    
    def compute_path(self):
        cost = 0
        for city in range(len(self.explored_set)-1):
            cost += self. distance_matrix[self.explored_set[city]][self.explored_set[city+1]]
        return cost
    
    def choose_node(self, frontier):
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
            else:
                parent = frontier[0]

            if parent[0] > self.num_passengers:
                self.current_seat -= 1
            else:
                self.current_seat += 1
            return parent
    
    def uniform_cost_children(self, node):
        if node == 0: # depot point
            res = list()
            for n in self.vertices:
                if n != node and n not in self.explored_set:
                    if n > self.num_passengers:
                        if n - self.num_passengers in self.explored_set:
                            res.append(n)
                        else:
                            continue
                    else:
                        res.append(n)
            return res
        
        elif node <= self.num_passengers: # pickup point
            res = list()
            for n in self.vertices:
                if n != node and n not in self.explored_set:
                    if n > self.num_passengers:
                        if n - self.num_passengers in self.explored_set:
                            res.append(n)
                        else:
                            continue
                    else:
                        res.append(n)
            return res
            
        else: # destination point
            res = list()
            for n in self.vertices:
                if n != node and n not in self.explored_set:
                    if n > self.num_passengers: # n is destination point
                        if n - self.num_passengers in self.explored_set: # if have visited pickup point yet
                            res.append(n)
                        else:
                            continue
                    else:
                        res.append(n)
            return res
        
        
    def heuristic_uc_function(self, child, parent, cost):
        return self.distance_matrix[parent][child] + cost
    
    def uniform_cost_search(self):
        self.explored_set = list()
        self.visited = [False for i in range(self.num_vertices)]
        uc_cost = 0
        frontier = list()
        frontier.append([self.vertices[0], 0])
        self.visited[0] = True
        while len(self.explored_set) != self.num_vertices:

#             print(f"Explored set: {self.explored_set}")
            parent = self.choose_node(frontier)
#             print(f"Frontier: {frontier}")
            frontier = list(filter(lambda x: x[0] != parent[0], frontier))
            uc_cost = parent[1]
#             print(f"UC_Cost: {uc_cost}")
            self.explored_set.append(parent[0])
#             print(f"Parent: {parent[0]}, children: {self.uniform_cost_children(parent[0])}")
            for child in self.uniform_cost_children(parent[0]):
                # choose heuristic function
                if self.visited[child] == False: # not in frontier or explored_set
                    self.cost[child] = self.heuristic_uc_function(child, parent[0], uc_cost)
                    self.visited[child] = True
                    frontier.append([child, self.cost[child]])
                    self.ancestor[child] = parent[0]
                elif self.visited[child] == True and child not in self.explored_set:
                    if self.cost[child] > self.heuristic_uc_function(child, parent[0], uc_cost):
                        self.cost[child] = self.heuristic_uc_function(child, parent[0], uc_cost)
                        frontier = list(filter(lambda x: x[0] != child, frontier))
                        frontier.append([child, self.heuristic_uc_function(child, parent[0], uc_cost)])
                        self.ancestor[child] = parent[0]
            
        self.explored_set.append(0)
        uc_cost += self.distance_matrix[parent[0]][0]
        
        _cost = self.compute_path()
        
        return _cost, self.explored_set
    
