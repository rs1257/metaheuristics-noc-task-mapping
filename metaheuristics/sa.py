import copy
from shared.generate import *
from deap.tools import Logbook
from shared.timeit_decorator import *

def generate_candidate(best):
    new = copy.deepcopy(best)
    while new.mapping == best.mapping:
        # random search around the best so far
        pos = random.randint(0, len(best.mapping) - 1)
        core = random.randint(0, CORE_NUMBER - 1)
        new.mapping[pos] = core
        # only eval if its not the same as the original
        if new.mapping != best.mapping:
            new.cost = eval_solution(new)
    return new


def update(temp, cooling_rate):
    return cooling_rate * temp
    # sample this on of my papers which are open say should be between 0.5 and 0.99 I think.


def accept_bad_move(temp, s, candidate):
    if temp <= 0.5:
        return False
    else:
        prob = math.exp((-s.cost[0] - candidate.cost[0]) / temp)
        print(temp, prob, s.cost[0], candidate.cost[0])
        return np.random.choice([True, False], p=[prob, 1-prob])

@timeit
def run_sa(NRUN, NITER, t_max, cooling_rate):
    random.seed(64)
    np.random.seed(64)
    log = Logbook()
    best_fitness = NRUN * [None]
    for r in range(NRUN):
        print("Start of Run %i" % r)
        s = generate_random_solution()
        temp = t_max
        for i in range(NITER):
            print("Iteration %i" % i)
            candidate = generate_candidate(s)
            if candidate.cost < s.cost or accept_bad_move(temp, s, candidate):
                s = candidate

            print(s.cost, candidate.cost)
            log.record(run=r, iter=i, fit=s.cost[0])
            if s.cost[0] == 0:
                break
            temp = update(temp, cooling_rate)

        print("-- End of Run %i--" % r)
        best_fitness[r] = s.cost[0]
        #print(log)

    return best_fitness, s.mapping, log


if __name__ == '__main__':
    NRUN = 5
    NITER = 10000
    #10000, 1000000000
    t_max = 1000000000
    cooling_rate = 0.96
    print(run_sa(NRUN, NITER, t_max, cooling_rate))
    # i think 0.9, 0.92, 0.94, 0.96, 0.98 as I have seen it these values used here, here and here
    # 100000 has to be in range or nearby
    #0.9 - 1000000 1552