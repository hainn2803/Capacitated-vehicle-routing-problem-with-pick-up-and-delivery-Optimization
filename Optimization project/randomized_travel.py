"""
    Created by @namhainguyen2803 in 02/02/2023.
"""
import copy 
import random
import numpy as np
from collections import defaultdict
import time
from collections import deque

class Randomized_Travel():
    def __init__(self, num_vertices, distance_matrix, capacity):
        self.num_vertices = num_vertices
        self.edges = list()
        self.vertices = [i for i in range(num_vertices)]
        self.num_edges = None
        self.distance_matrix = distance_matrix
        self.num_passengers = (num_vertices-1)//2
        self.capacity = capacity
        self.board_probability = np.zeros((self.num_vertices-1,self.num_vertices-1))
        self.board_count = np.ones((self.num_vertices-1,self.num_vertices-1))
        
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
    
    def children(self, list_node, current_seat, state):
#         current_seat = self.compute_capacity(current_seat)
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
        while len(self.children(list_node, current_seat, state)) != 0:
            list_next_cities = self.children(list_node, current_seat, state)
            next_city = np.random.choice(list_next_cities, 1)[0]
            if next_city > self.num_passengers:
                current_seat -= 1
            else:
                current_seat += 1
            state.append(next_city)
        state.append(0)
        return state
    
    def generate_data(self, num_samples=100):
        samples = list()
        i = 0
        while i <= num_samples:
            i += 1
            path = self.generate_valid_state()
            cost = self.compute_path(path)
            samples.append([cost, path])
        return samples
    
    def compute_capacity(self, configuration):
        capp = 0
        for conf in configuration:
            if conf != 0:
                if conf > self.num_passengers:
                    capp -= 1
                else:
                    capp += 1
        return capp
    
    def normalize_vector(self, v):
        norm = np.sum(v)
        if norm == 0: 
            return v
        else:
            return v/norm
    
    def update_probability(self):
        for state in range(self.num_vertices-1):
            state_vector = self.board_count[:,state]
            prob_vector = self.normalize_vector(state_vector)
            self.board_probability[:,state] = prob_vector
        print(self.board_probability)
        return self.board_probability
    
    def ReLU(self, vect):
        return np.sign(vect)
    
    def choose_next_generation(self, prob_brd, epsilon_1=0.1, epsilon_2=0.8):
        prob_board = copy.deepcopy(prob_brd)
        decision_prob = random.random()
        next_generation = [0]

        if decision_prob < epsilon_1:
            for state in range(self.num_vertices-2):
                prob_vect = copy.deepcopy(prob_board[:, state])
                s = np.argmax(prob_vect)
                prob_vect[s] = 0
                next_generation.append(s+1)
                prob_board[:, state+1:self.num_vertices-1] = prob_board[:, state+1:self.num_vertices-1] * np.reshape(self.ReLU(prob_vect), (-1,1))
                prob_board[:, state+1] = self.normalize_vector(prob_board[:, state+1])
            prob_vect = prob_board[:, self.num_vertices-2]
            s = np.argmax(prob_vect)
            next_generation.append(s+1)
            next_generation.append(0)
        elif epsilon_1 < decision_prob < epsilon_2:
            all_cities = np.arange(self.num_vertices-1)
            for state in range(self.num_vertices-2):
                prob_vect = copy.deepcopy(prob_board[:, state])
                s = np.random.choice(all_cities, p=prob_vect)
                prob_vect[s] = 0
                next_generation.append(s+1)
                prob_board[:, state+1:self.num_vertices-1] = prob_board[:, state+1:self.num_vertices-1] * np.reshape(self.ReLU(prob_vect), (-1,1))
                prob_board[:, state+1] = self.normalize_vector(prob_board[:, state+1])
            prob_vect = prob_board[:, self.num_vertices-2]
            s = np.argmax(prob_vect)
            next_generation.append(s+1)
            next_generation.append(0)
        else:
            next_generation = self.generate_valid_state()
        return next_generation
        
    
    def randomized_travel(self, max_iter=10, num_examples=100):
        all_samples = self.generate_data()
        i = 0
        optimal_cost = 1e9
        optimal_path = list()
        terminate = 0
        while i <= max_iter:
            i += 1
            all_samples.sort(key= lambda x: x[0])
            # terminal condition if max_iter is large
            if optimal_cost == all_samples[0][0]:
                terminate += 1
            if terminate == 5:
                optimal_cost = all_samples[0][0]
                optimal_path = all_samples[0][1]
                break
            if optimal_cost > all_samples[0][0]:
                optimal_cost = all_samples[0][0]
                optimal_path = all_samples[0][1]
            best_samples = all_samples[:5]
            for city in range(1,self.num_vertices):
                for best in best_samples:
                    most_likely_city = np.argmax(self.board_count[:, city-1])
                    if best[1][city]-1 != most_likely_city:
                        self.board_count[best[1][city]-1][city-1] += 4
                    else:
                        self.board_count[best[1][city]-1][city-1] += 3
            prob_board = self.update_probability()
            all_samples = list()
            for j in range(num_examples):
                sample = self.choose_next_generation(prob_board)
                cost_sample = self.compute_path(sample)
                all_samples.append([cost_sample, sample])
        return optimal_cost, optimal_path