from metaheuristics.ga import run_ga
from metaheuristics.pso import run_pso
from metaheuristics.tabu import run_tabu
from metaheuristics.sa import run_sa
from metaheuristics.aco import run_aco
from tasks.gen import CORE_NUMBER
import itertools
import pickle
import datetime
from shared.constants import BENCHMARK_FOLDER
import os
from parameter_sweep.after_sweep import *

def parameter_sweep(NRUN, NGEN, POP, parameters, alg_type):
    print("Parameter Sweep Started")

    pool = multiprocessing.Pool()
    options = []
    print(parameters)
    for p in parameters:
        l = []
        current = p[0]
        while current <= p[1]:
            if alg_type == "SA":
                if p[1] > 100:
                    l.append(current)
                    current *= p[2]
                    current = round(current, 1)
                else:
                    l.append(current)
                    current += float(p[2])
                    current = round(current, 2)
            else:
                l.append(current)
                current += p[2]
                current = round(current, 1)

        options.append(l)
    permutations = list(itertools.product(*options))
    # This means the solution will not change and only applies to GAs at the moment
    print(permutations)

    for perm in permutations:
        print(perm)
        if alg_type == "GA":
            # need to save the data and say what params were in their name
            print("Starting algorithm with CXPB: %.1f, MUTPB: %.1f" % (perm[0], perm[1]))
            _, _, result = run_ga(pool, NRUN, NGEN, perm[0], perm[1], POP)
            filename = get_directory(alg_type) + str(perm[0]) + "-" + str(perm[1]) + "-" + str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) + ".pkl"
            pickle_result(filename, result)
        elif alg_type == "PSO":
            print("Starting algorithm with Phi1: %.1f, Phi2: %.1f, Smin: %i, Smax: %i" % (perm[0], perm[1], -perm[2], perm[2]))
            _, _, result = run_pso(pool, NRUN, NGEN, perm[0], perm[1], -perm[2], perm[2], 0, CORE_NUMBER - 1, POP)
            filename = get_directory(alg_type) + str(perm[0]) + "-" + str(perm[1]) + "-" + str(perm[2]) + "-" + str(
            datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) + ".pkl"
            pickle_result(filename, result)
        elif alg_type == "Tabu":
            print("Starting algorithm with Tabu List Size: %.1f, Candidates: %.1f" % (perm[0], perm[1]))
            _, _, result = run_tabu(pool, NRUN, NGEN, perm[0], perm[1])
            filename = get_directory(alg_type) + str(perm[0]) + "-" + str(perm[1]) + "-" + str(
                datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) + ".pkl"
            pickle_result(filename, result)
        elif alg_type == "SA":
            print("Starting algorithm with Max Temp: %.1f, Cooling Rate: %.1f" % (perm[0], perm[1]))
            _, _, result = run_sa(NRUN, NGEN, perm[0], perm[1])
            filename = get_directory(alg_type) + str(perm[0]) + "-" + str(perm[1]) + "-" + str(
                datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) + ".pkl"
            pickle_result(filename, result)
        elif alg_type == "ACO":
            print("Starting algorithm with Pheromone Info: %.1f, Heuristic Info: %.1f, Evaporate: %.1f" % (perm[0], perm[1], perm[2]))
            _, _, result = run_aco(pool, NRUN, NGEN, perm[0], perm[1], perm[2], POP)
            filename = get_directory(alg_type) + str(perm[0]) + "-" + str(perm[1]) + "-" + str(perm[2]) + "-" + str(
                datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) + ".pkl"
            pickle_result(filename, result)
        else:
            print("Error Invalid Permutations")
    print("Parameter Sweep Ended")


def pickle_result(filename, result):
    with open(filename, 'wb') as f:
        pickle.dump(result, f, protocol=pickle.HIGHEST_PROTOCOL)


def get_directory(alg_type):
    directory = "data\\" + alg_type + "\\" + BENCHMARK_FOLDER + "\\"
    if not os.path.exists(directory):
        os.mkdir(directory)
    return directory


if __name__ == '__main__':
    import multiprocessing
    NRUN, NGEN, POP = 30, 100, 100
    # format [min, max, step]
    GA_PARAMS = [[0.2, 1, 0.2], [0.2, 1, 0.2]]
    PSO_PARAMS = [[1, 5, 1], [1, 5, 1], [1, 5, 1]]
    TABU_PARAMS = [[20, 100, 20], [20, 100, 20]] # needs different generations for each search .etc
    SA_PARAMS = [[10000, 100000000, 10], [0.8, 0.96, 0.04]]
    ACO_PARAMS = [[1, 9, 2], [1, 9, 2], [0.0, 0.8, 0.2]] # if i did 1 then it will always be 1 solution .etc
    PARAMS = ACO_PARAMS
    TYPE = "ACO" #iterations needs to be 10000
    # I want to also be able to specify the benchmarks
    parameter_sweep(NRUN, NGEN, POP, PARAMS, TYPE)
    # 20 - 500, 40 - 250, 60 - 167, 80 - 125, 100 - 100
    hibernate(100)