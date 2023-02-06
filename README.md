# Capacitated-vehicle-routing-problem-with-pick-up-and-delivery-Optimization-project

## Problem statement:
There are N passengers whose are at places $1,2,...,N$ respectively. The $i$ passenger, who is currently at place $i$, wants to go to place $i+N$. There are $K$ buses are currently at place $0$. Bus $k$ can only contains $q_{k}$ number of passengers at the same time. Given the 2-dimensional array distance matrix $d$, where $d[i][j]$ is the distance of place $i$ to place $j$. Make an optimal route plan so that the total distance traveled by all buses is the shortest.

### Input data:
* number of passengers: $N$
* number of buses: $K$
* distance matrix: 2D matrix __d__, where $d[i][j]$ = *distance*( $i$  $\rightarrow$ $j$ )  $\forall i , j$
* list of buses' capacity: 1D matrix __q__, where $q[k]$ is the number capacity of bus $k$

### Ouput data:
* Route plan for $K$ buses
* Total cost

### Terminology:
* place $0$: __depot__
* places $1$  $\rightarrow$ $N$: __pickup places__
* places $N+1$  $\rightarrow$ $2N$: __destination places__

## Algorithms:
In this project, I use several algorithms to solve the problem:
  * Branch and bound algorithm (Backtracking)
  * Constraint programming (using ortools)
  * Greedy search
  * Uniform cost search
  * Beam search
  * Metaheuristic Hill Climbing (Hill Climbing)
  * Randomized travel algorithm
  * Genetic algorithm

# Case study:
## Description of dataset

I use [ dataset 609 cities of Vietnam](https://simplemaps.com/data/vn-cities). Hence, there are __304__ pickup points and __304__ destination points, each of them correspond to a passenger.  

The dataset contains the name, latitude, longitude of 609 cities.  

Here is the visualization of 609 cities of Vietnam:  
<img src="https://user-images.githubusercontent.com/121554894/216872620-13f854f9-eddf-4ab6-8069-c8fa9afe27c4.png" width="400" height="300">. 
