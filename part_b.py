#%%
import math
#%%

def dp_extra_contraint(m, S, max_s_var=5):
    # similar start as part a
    num_points = len(m)

    # initializing the dp
    #dp = [[[{} for i in range(S+1)] for i in r]]
    dp = []
    for i in range(num_points):
        row = []
        for j in range(S+1):
            row.append({})
        dp.append(row)
    
    # setting initial values of the dp:
    for s0 in range(max_s_var+1):
        for s1 in range(max_s_var+1):
            sum_s = s0 + s1
            if sum_s > S:
                break
            if m[1]+s1<= m[0]+s0:
                product = (1+s0)*(1+s1)
                dp[0][sum_s][(s0,s1)] = (product, None)
            #else:
                #break

    # filling in the dp
    for i in range(num_points-2):
        for sum_so_far in range(S+1):
            for a,b in dp[i][sum_so_far].items():
                (si, si_plus_1) = a
                (now_product, pred) = b

                sum_constraint = (m[i+2] - m[i+1]) - si_plus_1
                left_constraint = (m[i+1] + si_plus_1 - m[i+2])
                
                # using boundary conditions
                max_val = min(sum_constraint, left_constraint, max_s_var)
                for si_plus_2 in range(max_val+1):
                    new_sum = sum_so_far + si_plus_2
                    if new_sum > S:
                        break

                    new_product = now_product * (1 + si_plus_2)
                    key = (si_plus_1, si_plus_2)

                    old = dp[i+1][new_sum].get(key, (0, None))
                    if new_product > old[0]:
                        dp[i+1][new_sum][key] = (new_product, ((si, si_plus_1), sum_so_far))

    # finding the best solution
    final_i = num_points - 2
    optimal_product, optimal_pair, optimal_sum_so_far = 0, None, 0
    for used in range(S+1):
        for pair, (prod, pred) in dp[final_i][used].items():
            if prod > optimal_product:
                optimal_product = prod
                optimal_pair = pair
                optimal_sum_so_far = used

    if optimal_pair is None:
        return (0, None)
    
    # backtracking to find the optimal vector s
    s_solution = [0 for i in range(num_points)]
    s_solution[num_points-2], s_solution[num_points-1] = optimal_pair

    i = final_i
    now_pair = optimal_pair
    now_sum = optimal_sum_so_far
    while True:
        pred_info = dp[i][now_sum][now_pair][1]
        if pred_info is None:
            s_solution[0]  = now_pair[0]
            if num_points != 1:
                s_solution[1] = now_pair[1]
            break
        else:
            (prev_pair, prev_sum) = pred_info
            s_solution[i-1] = prev_pair[0]
            s_solution[i] = prev_pair[1]
            i, now_pair, now_sum = i-1, prev_pair, prev_sum

    return (optimal_product, s_solution)
# %%

def test_partb():

    tests = [[[3, 1], 3],[[2, 1, 2], 4],[[0, 2, 2, 1], 3],]

    for idx, (m_data, S_data) in enumerate(tests, 1):
        val, s_sol = dp_extra_contraint(m_data, S_data, max_s_var=5)
        print(f"slopes = {m_data}, max S= {S_data}")
        if s_sol is not None:
            print(f"optimal product = {val}")
            print(f"slack vector = {s_sol}")
            print(f"sum slcks = {sum(s_sol)}")
            real_product = 1
            for x in s_sol:
                real_product *= (1+x)
            print(f"Real answer: {real_product}")
        else:
            print("no possible solution")
        print()
    return

# %%
