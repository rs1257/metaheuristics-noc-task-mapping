import copy
from deap.tools import Logbook
from shared.generate import *
from shared.timeit_decorator import *

def generate_candidates(best_candidate, candidate_list_size):
    candidates = []
    current = []
    while len(candidates) != candidate_list_size:
        # random search around the best so far
        pos = random.randint(0, len(best_candidate.mapping) - 1)
        core = random.randint(0, CORE_NUMBER - 1)
        new = copy.deepcopy(best_candidate)
        new.mapping[pos] = core
        # only add if its not the same as the original and its different from the others
        if new.mapping != best_candidate.mapping and new.mapping not in current:
            current.append(new.mapping)
            candidates.append(new)
    return candidates

@timeit
def run_tabu_diff(pool, NRUN, NITER, tabu_list_size, candidate_list_size):
    random.seed(64)
    log = Logbook()
    best_fitness = NRUN * [None]

    for r in range(NRUN):
        print("Start of Run %i" % r)
        s0 = generate_random_solution()
        best = copy.deepcopy(s0)
        best_candidate = copy.deepcopy(s0)
        tabu_list = [s0]

        for i in range(NITER):
            candidates = generate_candidates(best_candidate, candidate_list_size)
            costs = list(pool.map(eval_solution, candidates))
            for ind, cost in zip(candidates, costs):
                ind.cost = cost

            sorted_candidates = sorted(candidates, key=operator.attrgetter('cost'))
            for c in sorted_candidates:
                if not (c.mapping in tabu_list) and c.cost < best_candidate.cost:
                    best_candidate = c
                    break

            if best_candidate.cost < best.cost:
                best = best_candidate
            tabu_list.append(best_candidate.mapping)

            while len(tabu_list) > tabu_list_size:
                del tabu_list[0]

            log.record(run=r, iter=i, fit=best.cost[0])

            print("Iteration: %i, Cost: %i" % (i, list(best.cost)[0]))
            print(best.mapping)
            if list(best.cost)[0] == 0:
                break

        print("-- End of Run %i--" % r)
        best_fitness[r] = best.cost[0]
        #print(log)

    return best_fitness, best.mapping, log


if __name__ == '__main__':
    import multiprocessing

    pool = multiprocessing.Pool()
    #print(run_tabu(pool, 5, 100, 10, 100))

#based of http://www.cleveralgorithms.com/nature-inspired/stochastic/tabu_search.html
# this has short term memory but does not have intermediate or long term memory