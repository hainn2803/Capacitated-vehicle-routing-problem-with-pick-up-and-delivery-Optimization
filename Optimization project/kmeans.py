"""
    Created by @namhainguyen2803 in 06/02/2023.
"""
import pandas as pd
import numpy as np
import random as rd
import matplotlib.pyplot as plt
import math
import preprocess_data
from mpl_toolkits.mplot3d import Axes3D
from collections import defaultdict
import random

class K_Means:
    
    def __init__(self, k=2, tolerance = 0.0001, max_iter = 1000):
        self.k = k
        self.max_iterations = max_iter
        self.tolerance = tolerance
    
    def euclidean_distance(self, point1, point2):
        return np.linalg.norm(point1-point2, ord=1, axis=0)
        
    def predict(self,data):
        distances = [np.linalg.norm(data-self.centroids[centroid]) for centroid in self.centroids]
        classification = distances.index(min(distances))
        return classification
    
    def fit(self, data):
        self.centroids = {}
        l = list()
        for i in range(self.k):
            num_examples = np.shape(data)[0]
            rand_ind = np.random.choice(np.arange(num_examples),self.k)[0]
            while rand_ind in l:
                rand_ind = np.random.choice(np.arange(num_examples),self.k)[0]
            l.append(rand_ind)
            print(rand_ind)
            self.centroids[i] = data[rand_ind]
        
        
        for i in range(self.max_iterations):
            self.classes = defaultdict(lambda: [])
                
            for point in data:
                distances = []
                for index in self.centroids:
                    distances.append(self.euclidean_distance(point,self.centroids[index]))
                cluster_index = distances.index(min(distances))
                self.classes[cluster_index].append(point)
            
            previous = dict(self.centroids)
            for cluster_index in self.classes:
                self.centroids[cluster_index] = np.average(self.classes[cluster_index], axis = 0)
            

                
            isOptimal = True
            
            for centroid in self.centroids:
                original_centroid = previous[centroid]
                curr = self.centroids[centroid]
                if np.sum((curr - original_centroid)/original_centroid * 100.0) > self.tolerance:
                    isOptimal = False
            if isOptimal:
                break
            
if __name__=="__main__":
    lst = preprocess_data.convert_4d_vectors()
    kmeans = K_Means(k=5)
    kmeans.fit(lst)
    dic = preprocess_data.convert_4d_vectors_to_passengers(kmeans.classes)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    img = ax.scatter(lst[:,0], lst[:,1], lst[:,2], c=lst[:,3], cmap=plt.hot())
    fig.colorbar(img)
    plt.show()