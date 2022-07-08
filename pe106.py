import math
import itertools


def multiplier(M):
    questions = 0
    non_questions = 0
    for B in itertools.combinations(range(0,M), M//2):
        C = set(range(0,M))
        for b in B:
            C.remove(b)
        # print(B, C)
        type = "none"
        for x,y in zip(B,C):
            if type == "none":
                if x < y:
                    type = "less"
                else:
                    type = "more"
            elif type == "less":
                if x >= y:
                    type = "question"
                    continue
            elif type == "more":
                if x <= y:
                    type = "question"
                    continue
        # print(type)
        if type == "question":
            questions += 1
        else:
            non_questions += 1
    # print(questions, non_questions, questions//2)
    return(questions//2)



N = 12

a = 0
for k in range(4, N+1, 2):
    a += math.comb(N, k) * multiplier(k)
print(a)