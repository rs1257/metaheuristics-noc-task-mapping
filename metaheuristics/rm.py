from shared.generate import *
from deap.tools import Logbook
from shared.timeit_decorator import *

@timeit
def run_rm(NRUNS, NITER):
    random.seed(64)
    best_solutions = []
    log = Logbook()
    for r in range(NRUNS):
        print("Start of Run %i" % r)
        best = generate_random_solution()
        for i in range(NITER):
            log.record(run=r, iter=i, fit=best.cost[0])
            print("Iteration %i" % i)
            print(best.mapping, best.cost)
            if best.cost[0] == 0:
                break
            possible = generate_random_solution()
            if possible.cost < best.cost:
                best = possible

        print("-- End of Run %i--" % r)
        best_solutions.append(best.cost[0])
        #print(log)
    return best_solutions, best.mapping, log

if __name__ == '__main__':
    print(run_rm(5, 10000))