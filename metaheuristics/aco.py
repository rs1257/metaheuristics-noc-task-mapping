from supertasks.super_evaluation import *
from shared.constants import *

from deap import base, creator, tools
from deap.tools import Logbook
from shared.timeit_decorator import *

creator.create("FitnessMinACO", base.Fitness, weights=(-1.0,))
creator.create("Ant", list, fitness=creator.FitnessMinACO)

# Default parameters
ALPHA = 2 # > 0 importance of pheromone value
BETA = 2 # > 0 importance of heuristic information
EVAPORATION_RATE = 0.2 # between 0-1


def generate_ant(p, h, alpha, beta):
    return creator.Ant(construct_solution(p, h, alpha, beta, [i for i in range(CORE_NUMBER)]))


def pheromone_update_rule(ind1, ind2, value, best):
    deposited = 1 / best.fitness.values[0] if ind2 == best[ind1] else 0
    updated_p = (1 - EVAPORATION_RATE) * value + deposited
    if updated_p > 1:  updated_p = 1 # can make it better
    return updated_p # can round for similar results


def update_pheromones(p, best):
    return [[pheromone_update_rule(c1, c2, j, best) for c2, j in enumerate(i)] for c1, i in enumerate(p)]


# this version shows the best cost with this core to task assignment
def update_heuristic_info(best, info):
    for i, j in zip(best, info):
        value = best.fitness.values[0]
        if value < j[i] or j[i] == 0:
            j[i] = value


def initialise_pheromones():
    """ A list for each task containing a list for each core initialised to the value of 1 """
    return [[1 for _ in range(CORE_NUMBER)] for _ in range(TASK_NUMBER)]


def calculate_new_probability(task, info, alpha, beta):
    modified = [(i ** alpha) * (1/j ** beta) if j > 0 else (i ** alpha) * (1 ** beta) for i, j in zip(task, info)]
    return [j / sum(modified) for j in modified]


def construct_solution(p, h, alpha, beta, options):
    return [np.random.choice(options, p=calculate_new_probability(task, info, alpha, beta)) for task, info in zip(p, h)]


toolbox = base.Toolbox()
toolbox.register("update", update_pheromones, p=initialise_pheromones(), best=None)
toolbox.register("evaluate", evaluate)

stats_fit = tools.Statistics(key=lambda ind: ind.fitness.values)
mstats = tools.MultiStatistics(fitness=stats_fit)
mstats.register("min", np.min)

@timeit
def run_aco(pool, NRUN, NGEN, alpha, beta, evaporation_rate, ants):
    global ALPHA, BETA, EVAPORATION_RATE

    ALPHA, BETA, EVAPORATION_RATE = alpha, beta, evaporation_rate

    toolbox.register("map", pool.map)
    np.random.seed(64)

    log = Logbook()
    min_fitness = [None] * NRUN

    for r in range(NRUN):
        print("Start of Run %i" % r)
        pheromones = initialise_pheromones()
        heuristic_info = [[0 for _ in range(CORE_NUMBER)] for _ in range(TASK_NUMBER)]
        best = None
        pop = [generate_ant(pheromones, heuristic_info, ALPHA, BETA) for _ in range(ants)]

        for g in range(NGEN):
            print("Generation %i" % g)

            fitnesses = list(toolbox.map(toolbox.evaluate, pop))
            for ind, fit in zip(pop, fitnesses):
                ind.fitness.values = fit

            best_ind = tools.selBest(pop, 1)[0]
            if best is None or best_ind.fitness.values < best.fitness.values:
                best = best_ind

            print("Best individual is %s, %s, Best in gen %s" % (best, best.fitness.values, best_ind.fitness.values))

            record = mstats.compile(pop)
            log.record(run=r, gen=g, **record)

            if best.fitness.values[0] == 0:
                break

            update_heuristic_info(best, heuristic_info)
            #print(heuristic_info)
            pheromones = toolbox.update(p=pheromones, best=best_ind)

            # create new ants with updated pheromone values
            pop = [generate_ant(pheromones, heuristic_info, ALPHA, BETA) for _ in range(ants)]
            ######################### Biggest Problem is diversity if I fix that then it is a good algorithm

        print("-- End of ants --")
        min_fitness[r] = best.fitness.values[0]
        #print(log)

    return min_fitness, best, log


if __name__ == '__main__':
    import multiprocessing
    pool = multiprocessing.Pool()

    print(run_aco(pool, 1, 100, 1, 1, 0.0, 100))
    # 2 and 2 seems to do well

