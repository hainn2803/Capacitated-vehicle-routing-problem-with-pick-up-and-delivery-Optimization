"""
    Created by @namhainguyen2803 in 02/02/2023.
"""
import copy 
import random
import numpy as np
from collections import defaultdict
import time
from collections import deque

def generate_sample(num_cities):
    matrix = list()
    for i in range(num_cities):
        lis = list()
        for j in range(num_cities):
            if i != j:
                r = random.randint(5, 9)
                lis.append(r)
            else:
                lis.append(0)
        matrix.append(lis)
    buses = random.randint(2, 5)
    return matrix, buses