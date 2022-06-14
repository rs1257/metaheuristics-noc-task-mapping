from shared.generate import *
from deap.tools import Logbook
from shared.constants import *
from shared.timeit_decorator import *

@timeit
def run_rm(pool, NRUNS, NITER):
    best_solutions = []
    log = Logbook()
    for r in range(NRUNS):
        print("Start of Run %i" % r)
        mappings = sorted(pool.map(generate_random_solution_parallel, [str(r) + ":" + str(i) for i in range(NITER)]), key=operator.attrgetter('cost'))
        best = mappings[0].cost[0]
        best_solutions.append(best)
        log.record(run=r, fit=best)
        print("-- End of Run %i--" % r)
        print(best)
        print(log)

    # this is not the best mapping at the moment
    return best_solutions, mappings[0].mapping, log


if __name__ == '__main__':
    import multiprocessing
    from timeit import default_timer as timer
    pool = multiprocessing.Pool()
    start = timer()
    print(run_rm(pool, 5, 10000))
    end = timer()
    print(end - start)