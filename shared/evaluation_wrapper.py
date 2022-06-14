from supertasks.super_evaluation import *


# wrapper around eval function to get solution in correct format
def eval_solution(solution):
    return evaluate(solution.mapping)
