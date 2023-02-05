from ortools.sat.python import cp_model
#Hàm tính tổng của nested_list
def nested_sum(L):
    total = 0  
    for i in L:
        if isinstance(i, list):  
            total += nested_sum(i)
        else:
            total += i
    return total
def CP_algorithm(num_cities,num_buses,list_capacities, matrix_distance):
    
    
          #Tạo list xác định điểm đón và trả khách
    a_value = [0]
    a_value+= [1]*num_cities
    a_value += [-1]*num_cities
    
    
      #Đổi tên biến ngắn gọn
    N = num_cities
    K = num_buses
    d = matrix_distance
    
    
      #Tạo model
    model = cp_model.CpModel()

    
    
      #Thêm biến vào model x[s][e][k][t]
    x = []
    for sp in range(2*N+1):
        sp_lst = []
        for ep in range(2*N+1):
            ep_lst = []
            for k in range(K):
                k_lst = []
                for t in range(2*N+1):
                    k_lst.append(model.NewIntVar(0,1,f'x[{sp}][{ep}][{k}][{t}]'))
                ep_lst.append(k_lst)
            sp_lst.append(ep_lst)
        x.append(sp_lst)
      
      
      #Constrain 1: Kiểm tra mỗi điểm đến chỉ được đến một lần bởi 1 xe 
    for ep in range(1,2*N+1):
        model.Add((nested_sum([[[x[sp][ep][k][t] for t in range(2*N+1)] for k in range(K)] for sp in range(2*N+1)])) == 1)
      
      
      #Constrain 2: Kiểm tra mỗi điểm xuất phát chỉ được đến một lần bởi 1 xe 

    for sp in range(1,2*N+1):
        model.Add((nested_sum([[[x[sp][ep][k][t] for t in range(2*N+1)] for k in range(K)] for ep in range(2*N+1)])) == 1)
      
      
      # Constrain 3: Mỗi xe ở mỗi iteration t chỉ được đi 1 đường
    for t in range(2*N+1):
        for k in range(K):
            model.Add(nested_sum([[x[sp][ep][k][t] for ep in range(2*N+1)] for sp in range(2*N+1)]) == 1)
        
      
      #Constrain 4: Kiểm tra số lượng khách trên xe tại mỗi thời điểm không vượt quá giới hạn
    for k in range(K):
        for t_now in range(2*N+1):
            model.Add(nested_sum([[[x[sp][ep][k][t]*a_value[ep] for t in range(t_now+1)] for ep in range(2*N+1)] for sp in range(2*N+1)]) <= list_capacities[k])
      
      
      #Constrain 5: Kiểm tra mỗi cặp điểm (đón và trả của 1 khách) được đến bởi 1 xe theo đúng thứ tự
    for p in range (N+1,2*N+1):
        for k in range(K):
            for t_now in range(2*N+1):
                b = model.NewBoolVar('b')
                model.Add(nested_sum([[x[sp][p][k][t_now]]  for sp in range(2*N+1)]) == 1).OnlyEnforceIf(b)
                model.Add(nested_sum([[x[sp][p][k][t_now]]  for sp in range(2*N+1)]) != 1).OnlyEnforceIf(b.Not())
                model.Add(nested_sum([[[x[sp][p-N][k][t]] for t in range(t_now)] for sp in range(2*N+1)]) == 1).OnlyEnforceIf(b)
      
      
      # Constrain 6: Kiểm tra tính liên tục: điểm đến của iteration t là điểm đi của iteration t+1
    for p in range(2*N+1):
        for k in range(K):
            for t_now in range(2*N):
                b = model.NewBoolVar('b')
                model.Add(nested_sum([x[sp][p][k][t_now] for sp in range(2*N+1)]) == 1).OnlyEnforceIf(b)
                model.Add(nested_sum([x[sp][p][k][t_now] for sp in range(2*N+1)]) != 1).OnlyEnforceIf(b.Not())
                model.Add(nested_sum([x[p][ep][k][t_now+1] for ep in range(2*N+1)]) == 1).OnlyEnforceIf(b)
      
      
      #Constrain 7: Kiểm tra rằng mỗi xe ở iteration 0 đều xuất phát đến 1 điểm đón khách
    model.Add(nested_sum([[x[0][ep][k][0] for k in range(K)] for ep in range(1,N+1)] ) == K)

    
    #Bỏ ngõ constrain này vì có quãng đường không cần constrain này thì quãng đường ngắn hơn

    #Contrain 8: Kiểm tra rằng xe hoàn thành hành trình trước khi quay lại bến vị trí 0
    for k in range(K):
        for t_now in range(2*N+1):
            c = model.NewBoolVar('c')
            model.Add(nested_sum([x[sp][0][k][t_now] for sp in range(1,2*N+1)]) == 1).OnlyEnforceIf(c)
            model.Add(nested_sum([x[sp][0][k][t_now] for sp in range(1,2*N+1)]) != 1).OnlyEnforceIf(c.Not())
            model.Add(nested_sum([[[x[sp][ep][k][next_t] for next_t in range(t_now+1,2*N+1)] for ep in range(1,2*N+1)] for sp in range(2*N+1)]) == 0).OnlyEnforceIf(c)


    #Objective function
    model.Minimize(nested_sum([[[[x[sp][ep][k][t]*d[sp][ep] for t in range(2*N+1)] for k in range(K)] for ep in range(2*N+1)] for sp in range(2*N+1)]))

    
    #Giải model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    route = [[0] for k in range(K)]
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        # print(f'Maximum of objective function: {solver.ObjectiveValue()}\n')
        for t in range(2*N+1):
            for k in range(K):
                for sp in range(2*N+1):
                    for ep in range(2*N+1):
                        if solver.Value(x[sp][ep][k][t]) == 1:
                            if sp != 0:
                              route[k].append(sp)
                            # print(f'x[{sp}][{ep}][{k}][{t}] = ', solver.Value(x[sp][ep][k][t]))

    
    elif status == cp_model.INFEASIBLE:
        print('No solution')
    return (solver.ObjectiveValue(), route)

