from deap import base, creator, tools
from deap.tools import Logbook

from shared.bounds import *
#from metaheuristics.evaluation import *
from supertasks.super_evaluation import *
from shared.timeit_decorator import *

creator.create("FitnessMinGAA", base.Fitness, weights=(-1.0,))
creator.create("IndividualA", list, fitness=creator.FitnessMinGAA)

toolbox = base.Toolbox()
toolbox.register("attr_int", random.randint, 0, CORE_NUMBER - 1)
toolbox.register("individual", tools.initRepeat, creator.IndividualA, toolbox.attr_int, TASK_NUMBER)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

stats_fit = tools.Statistics(key=lambda ind: ind.fitness.values)
mstats = tools.MultiStatistics(fitness=stats_fit)
mstats.register("avg", np.mean)
mstats.register("std", np.std)
mstats.register("min", np.min)
mstats.register("max", np.max)

toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxOnePoint)
toolbox.register("mutate", tools.mutUniformInt, low=0, up=CORE_NUMBER - 1, indpb=0.01)
toolbox.register("select", tools.selTournament, tournsize=5)

toolbox.decorate("mate", check_bounds_ga(0, CORE_NUMBER - 1))
toolbox.decorate("mutate", check_bounds_ga(0, CORE_NUMBER - 1))

stats_fit = tools.Statistics(key=lambda ind: ind.fitness.values)
mstats = tools.MultiStatistics(fitness=stats_fit)
mstats.register("min", np.min)

@timeit
def run_ga(pool, NRUN, NGEN, CXPB, MUTPB, inds):
    toolbox.register("map", pool.map)
    random.seed(64)

    min_fitness = [None] * NRUN
    log = Logbook()
    #need to reorder the ga implementation so first pop has an effect?
    for r in range(NRUN):
        print("Start of Run %i" % r)
        hof = tools.HallOfFame(1)
        pop = toolbox.population(n=inds)
        fits = list(toolbox.map(toolbox.evaluate, pop))
        for ind, fit in zip(pop, fits):
            ind.fitness.values = fit
        invalid = inds

        for g in range(NGEN):
            print("Generation %i" % g)
            record = mstats.compile(pop)
            log.record(run=r, gen=g, **record, evals=invalid)
            hof.update(pop)

            print("  Min %s" % min(fits))
            if min(fits) == 0:
                break

            offspring = toolbox.select(pop, len(pop))
            offspring = list(toolbox.map(toolbox.clone, offspring))

            for c1, c2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < CXPB:
                    toolbox.mate(c1, c2)
                    del c1.fitness.values
                    del c2.fitness.values

            for mutant in offspring:
                if random.random() < MUTPB:
                    toolbox.mutate(mutant)
                    del mutant.fitness.values

            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)

            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit
            invalid = len(invalid_ind)
            #print("Eval %i inds" % len(invalid_ind))

            pop[:] = offspring

            fits = [ind.fitness.values[0] for ind in pop]

        print("-- End of evolution --")

        best_ind = tools.selBest(hof, 1)[0]
        print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))

        min_fitness[r] = min(fits)
        #print(log)

    return min_fitness, best_ind, log
