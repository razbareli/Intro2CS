######################################
# FILE:ex3.py
# WRITER:Raz_Bareli  unixraz 203488747
# EXERCISE:intro2cs1 ex3 2021
# DESCRIPTION: Functions Using Loops
######################################

def input_list():
    """creates a list of inputs as floats and sums all numbers"""
    sum = 0
    lst = []
    n = 0
    while True:
        n = input()
        if n == "":
            break
        n = float(n)
        lst.append(n)
    for i in lst:
        sum += i
    lst.append(sum)
    return (lst)

def inner_product(vec_1, vec_2):
    """calculates the inner product of 2 vectors"""
    if len(vec_1) != len(vec_2):
        return None
    if len(vec_1) == len(vec_2) == 0:
        return 0
    else:
        sum = 0
        for i in range(len(vec_1)):
            sum += vec_1[i] * vec_2[i]
        return (sum)

def sequence_monotonicity(sequence):
    """determines what kind of sequence the input is"""
    ans = [True, True, True, True]
    if len(sequence) == 0 or len(sequence) == 1:
        return ans
    else:
        l = []
        for i in range(1, len(sequence)):
            if sequence[i-1] == sequence[i]:
                ans[1] = ans[3] = False
            if sequence[i-1] < sequence[i]:
                ans[2] = ans[3] = False
            if sequence[i - 1] > sequence[i]:
                ans[0] = ans[1] = False
    return (ans)

def monotonicity_inverse(def_bool):
    """creates a sequence that qulifies the conditions"""
    lst = []
    for i in def_bool:
        if i == True:
            lst.append(1)
        else:
            lst.append(0)
    if lst == [0, 0, 0, 0]:
        return [1, 3, 2, 4]
    if lst == [0, 0, 1, 1]:
        return [4, 3, 2, 1]
    if lst == [1, 1, 0, 0]:
        return [1, 2, 3, 4]
    if lst == [1, 0, 0, 0]:
        return [1, 2, 2, 3]
    if lst == [0, 0, 1, 0]:
        return [4, 3, 3, 1]
    if lst == [1, 0, 1, 0]:
        return [2, 2, 2, 2]
    return None

def primes_for_asafi(n):
    """returns all prime numbers from 2 to n"""
    ans = []
    num = 2
    while len(ans) < n:
        for i in range(2, num):
            if num % i == 0:
                break
        else:
            ans.append(num)
        num += 1
    return (ans)

def sum_of_vectors(vec_lst):
    """calculates the sum of the vectors"""
    ans = []
    sum = 0
    if len(vec_lst) == 0:
        return None
    for i in range(len(vec_lst[0])):
        for j in range(len(vec_lst)):
            sum += vec_lst[j][i]
        ans.append(sum)
        sum = 0
    return(ans)

def num_of_orthogonal(vectors):
    """returns how many orthogonal vectors are in the argument"""
    ans = 0
    for i in range(len(vectors)):
        for j in range(len(vectors)):
            if i == j:
                continue
            else:
                product = inner_product(vectors[i], vectors[j])
            if product == 0:
                ans += 1
    return int(ans/2)


