"""
    Created by @namhainguyen2803 on 02/02/2023.
"""

import random

def generate_sample(num_passengers):
    matrix = list()
    for i in range(num_passengers):
        lis = list()
        for j in range(num_passengers):
            if i != j:
                r = random.randint(10, 100)
                lis.append(r)
            else:
                lis.append(0)
        matrix.append(lis)
    buses = random.randint(2, 5)
    return matrix, buses