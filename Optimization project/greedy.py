"""
    Created by @namhainguyen2803 in 02/02/2023.
"""
import copy 
import random
import numpy as np
from collections import defaultdict
import time
from collections import deque

class Greedy_Search_Graph():
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
    
    
    def heuristic_greedy_function(self, child, parent):
        return self.distance_matrix[parent][child]
    
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
    
    
    def greedy_search(self):
        greedy_cost = 0
        frontier = list()
        frontier.append([self.vertices[0], 0])
        
        while len(frontier) != 0:
            # choose node
            parent = self.choose_node(frontier)
            greedy_cost += parent[1]
            self.visited[parent[0]] = True
            self.explored_set.append(parent[0])

            new_frontier = list()
            # print(f"Parent: {parent[0]}, Children: {self.children(parent[0])}")
            for child in self.children(parent[0]):
                self.ancestor[child] = parent[0]
                # choose heuristic function
                self.cost[child] = self.heuristic_greedy_function(child, parent[0])
                new_frontier.append([child, self.cost[child]])
            frontier = copy.deepcopy(new_frontier)

        greedy_cost += self.distance_matrix[parent[0]][0]
        self.explored_set.append(0)
        return greedy_cost, self.explored_set  
    