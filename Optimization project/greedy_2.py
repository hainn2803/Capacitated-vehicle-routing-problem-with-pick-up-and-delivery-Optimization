def min_distance(s: int,lst: list,d: list):
    """ Hàm tìm vị trí gần điểm s nhất trong tập hợp điểm lst, d là list chứa khoảng các giữa các điểm """
    index = -1
    min_val = 1000000
    for e in lst:
        if d[s][e]<min_val:
            index = e
            min_val = d[s][e]
    return (index,min_val)
def find_bus_next(lst,d, visited_lst,unvisited_lst,q_now,q_value):
    number = -1
    min_val = 1000000000
    next_point = -1
    for k in lst:
        if unvisited_lst == [[] for k in range(K)]:
            return (None,None)
        if unvisited_lst[k] == []:
            continue
        s_now = visited_lst[k][-1]
        if q_now[k] < q_value[k]:
            (index,val) = min_distance(s_now,unvisited_lst[k],d)
        else:
            lst_to_choose = []
            for i in unvisited_lst[k]:
                if i > N:
                    lst_to_choose.append(i)
            (index,val) = min_distance(s_now,lst_to_choose,d)
        if val < min_val:
            number = k
            min_val = val
            next_point = index
    if number == -1:
        return (None,None)
    return (number,next_point)

def distance(visited_lst,d):
    total_dis = 0
    for bus in visited_lst:
        for i in range(len(bus)-1):
            total_dis += d[bus[i]][bus[i+1]]
    return total_dis
def Greedy_2(num_cities,num_buses,list_capacities, matrix_distance):
    
    N = num_cities
    K = num_buses
    d = matrix_distance

    visited_lst = [[0] for k in range(K)]
    unvisited_lst = [[i for i in range(1,N+1)] for k in range(K)]
    cap_now = [0 for k in range(K)]
    for i in range(2*N+1):
        car_lst = [m for m in range(K)]
        for j in range(K):
            (k, index) = find_bus_next(car_lst,d, visited_lst,unvisited_lst,cap_now,list_capacities)
            if k == None:
                break

            visited_lst[k].append(index)
            
            if index <= N:
                unvisited_lst[k].append(index+N)
                cap_now[k] += 1
            else:
                cap_now[k] -= 1
            for lst in unvisited_lst:
                if index in lst:
                    lst.remove(index)
            car_lst.remove(k)
            
        if unvisited_lst == [[] for k in range(K)]:
            break
    for bus in visited_lst:
        bus.append(0)
    return (distance(visited_lst,d),visited_lst)

