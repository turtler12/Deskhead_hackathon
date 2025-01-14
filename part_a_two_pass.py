#%%

import math
#%%

def two_pass(m:list):
    num_points = len(m)
    # same base cases as dp
    if num_points <= 1:
        return [0 for i in range(num_points)]
    
    # forward pass - finds the max possible s_i+1 (from constraint 1)
    max_s = [0 for i in range(num_points)]
    for i in range(num_points-1):
        max_s[i+1] = max(0, max_s[i] + m[i]-m[i+1])
    
    # backward pass - finds the minimum possible (from constraint 2)
    min_s = [0 for i in range(num_points)]
    # move backwards from the end to beginning
    for i in range(num_points-1, 0, -1):
        min_s[i-1] = max(0, m[i]-m[i-1]-min_s[i])
    
    #finding the optimal s:
    s_vector = [0 for i in range(num_points)]
    for i in range(num_points):
        s_vector[i] = min(max_s[i], min_s[i])
    
    # calculating the optimal objective function
    product = 1
    for i in s_vector:
        product *= (1+i)
    return s_vector, product
# %%

def test_two_pass():
    test_cases = [[0,0], [1,1], [1,2,3,5]]
    answers = [1, 1, 1]
    for i in range(len(test_cases)):
        p = two_pass(test_cases[i])[1]
        if p != answers[i]:
            print("wrong!", test_cases[i])


# %%
