
#%%

import math

#%%
def dp_solution(m, max_s):
    
    num_points = len(m)
    
    # Initializing the dp
    # dp of the form: list of dictionaries
    dp = [{} for _ in range(num_points)]
    for s0 in range(max_s + 1):
        s1_max = s0 + (m[0] - m[1])
        s1_max = max_s if  s1_max > max_s else s1_max

        for s1 in range(s1_max+1):
            product = (1 + s0) * (1 + s1)
            dp[0][(s0, s1)] = (product, None)

    # Now filling in the dp
    for i in range(0, num_points-2):
        for a,b in dp[i].items():
            (si, si_plus_1) = a
            (new_product, pred) = b

            # constraints from question
            sum_constraint = (m[i+2] - m[i+1]) - si_plus_1
            left_constraint = (m[i+1] + si_plus_1 - m[i+2])

            # largest possible si_plus_2 is the smallest of the limits

            si_plus_2_max = min(si_plus_1 + sum_constraint, max_s)
            si_plus_2_min = max(left_constraint, 0)

            x = min(sum_constraint, left_constraint, max_s)


            #for si_plus_2 in range(si_plus_2_min, si_plus_2_max+1):
                #new_product = new_product * (1 + si_plus_2)
            
            for si_plus_2 in range(x+1):
                updated_prod = new_product * (1 + si_plus_2)
                key = (si_plus_1, si_plus_2)

                if key not in dp[i+1] or updated_prod > dp[i+1][key][0]:
                    dp[i+1][key] = (updated_prod, (si, si_plus_1))

    # now, we just need to return the final dp dictionary
                    
    index_answer = num_points - 2
    # no feasible answer
    if not dp[index_answer]:
        return (0, None)
    
    # there is a feasible solution:
    # find the best product:

    def find_best_val_pair(dp, index):
        optimal_product = 0
        optimal_pair = 0
        for pair, (prod, pred) in dp[index].items():
            if prod > optimal_product:
                optimal_product = prod
                optimal_pair = pair
        return optimal_product, optimal_pair

    optimal_product, optimal_pair = find_best_val_pair(dp, index_answer)


    # backtracking
    # find out the slacks by starting from the end, going towards the front
    s_vector = [0 for i in range(num_points)]

    s_vector[num_points-2], s_vector[num_points-1]=optimal_pair[0], optimal_pair[1]

    i = index_answer
    now_pair = optimal_pair
    while True:
        s_earlier = dp[i][now_pair][1]
        if s_earlier is None:
            s_vector[0] = now_pair[0]
            if num_points > 1:
                s_vector[1] = now_pair[1]
            break
        else:
            s_vector[i-1] = s_earlier[0]
            s_vector[i] = now_pair[0]
            now_pair = s_earlier
            i -= 1
    return (optimal_product, s_vector)




def test_dp_v2():
    test_cases = [[1, 1],[0, 1, 1], [2, 2, 2], [0, 0, 1, 2, 2, 3],[5,5,5,5,5,5,5,5,5],]
    
    for idx, m_test in enumerate(test_cases, 1):
        print(f"m = {m_test}")
        best_val, s_sol = dp_solution(m_test, max_s=20)
        if s_sol is not None:
            print("optimal product =", best_val)
            print("slacks =", s_sol)
        else:
            print("not possible")
        print()






    

# %%
