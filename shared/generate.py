from shared.evaluation_wrapper import *
from shared.solution import *
from shared.constants import *


def generate_random_solution():
    mapping = []
    for t in range(len(tasks)):
        mapping.append(random.randint(0, CORE_NUMBER - 1))
    s = Solution()
    s.mapping = mapping
    s.cost = eval_solution(s)
    return s


def generate_random_solution_parallel(i):
    params = i.split(":")
    random.seed(int(params[1]) + (10000 * int(params[0])))
    mapping = []
    for t in range(len(tasks)):
        mapping.append(random.randint(0, CORE_NUMBER - 1))
    s = Solution()
    s.mapping = mapping
    s.cost = eval_solution(s)
    print("Iteration %s" % params[1], "Cost %i" % s.cost)
    return s