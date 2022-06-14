from deap import base
from deap import creator
from deap import tools
from deap.tools import Logbook

from shared.bounds import *
# from metaheuristics.evaluation import *
from supertasks.super_evaluation import *
from shared.timeit_decorator import *

# Default parameters
PHI1, PHI2 = 1, 5
SMIN, SMAX = -CORE_NUMBER/2, CORE_NUMBER/2
PMIN, PMAX = 0, CORE_NUMBER - 1

creator.create("FitnessMinPSO", base.Fitness, weights=(-1.0,))
creator.create("Particle", list, fitness=creator.FitnessMinPSO, speed=list,
               smin=None, smax=None, best=None)


def generate(size, pmin, pmax, smin, smax):
    part = creator.Particle(random.randint(pmin, pmax) for _ in range(size))
    part.speed = [random.randint(smin, smax) for _ in range(size)]
    part.smin = smin
    part.smax = smax
    return part


def update_particle(part, best, phi1, phi2):
    u1 = (random.randint(0, phi1) for _ in range(len(part)))
    u2 = (random.randint(0, phi2) for _ in range(len(part)))
    v_u1 = map(operator.mul, u1, map(operator.sub, part.best, part))
    v_u2 = map(operator.mul, u2, map(operator.sub, best, part))
    part.speed = list(map(operator.add, part.speed, map(operator.add, v_u1, v_u2)))
    for i, speed in enumerate(part.speed):
        if speed < part.smin:
            part.speed[i] = part.smin
        elif speed > part.smax:
            part.speed[i] = part.smax
    part[:] = list(map(operator.add, part, part.speed))
    return part


# smin and smax need to be small due to the nature of the problem (small changes have large effects)
toolbox = base.Toolbox()
#toolbox.register("particle", generate, size=TASK_NUMBER, pmin=PMIN, pmax=PMAX, smin=SMIN, smax=SMAX)
#toolbox.register("population", tools.initRepeat, list, toolbox.particle)
#toolbox.register("update", update_particle, phi1=PHI1, phi2=PHI2)
toolbox.register("evaluate", evaluate)

#toolbox.decorate("update", check_bounds_pso(PMIN, PMAX))

stats_fit = tools.Statistics(key=lambda ind: ind.fitness.values)
mstats = tools.MultiStatistics(fitness=stats_fit)
mstats.register("min", np.min)

@timeit
def run_pso(pool, NRUN, NGEN, phi1, phi2, smin, smax, pmin, pmax, inds):
    global PHI1, PHI2, SMIN, SMAX, PMIN, PMAX

    PHI1, PHI2, SMIN, SMAX, PMIN, PMAX = phi1, phi2, smin, smax, pmin, pmax
    # Register the current values
    toolbox.register("particle", generate, size=TASK_NUMBER, pmin=PMIN, pmax=PMAX, smin=SMIN, smax=SMAX)
    toolbox.register("population", tools.initRepeat, list, toolbox.particle)
    toolbox.register("update", update_particle, phi1=PHI1, phi2=PHI2)
    toolbox.decorate("update", check_bounds_pso(PMIN, PMAX))
    toolbox.register("map", pool.map)
    random.seed(64)
    log = Logbook()
    min_fitness = [None] * NRUN

    for r in range(NRUN):
        print("Start of Run %i" % r)
        hof = tools.HallOfFame(1)
        pop = toolbox.population(n=inds)
        best = None
        for g in range(NGEN):
            print("Generation %i" % g)
            fitnesses = list(toolbox.map(toolbox.evaluate, pop))
            for part, fit in zip(pop, fitnesses):
                part.fitness.values = fit
                if not part.best or part.best.fitness < part.fitness:
                    part.best = creator.Particle(part)
                    part.best.fitness.values = part.fitness.values
                if not best or best.fitness < part.fitness:
                    best = creator.Particle(part)
                    best.fitness.values = part.fitness.values

            record = mstats.compile(pop)
            log.record(run=r, gen=g, **record)
            hof.update(pop)
            [toolbox.update(part, best) for part in pop]

            fits = [ind.fitness.values[0] for ind in pop]

            print("  Min %s" % min(fits))
            if min(fits) == 0:
                break

        print("-- End of swarm --")

        best_ind = tools.selBest(hof, 1)[0]
        print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))

        min_fitness[r] = best_ind.fitness.values[0]
        #print(log)
    return min_fitness, best_ind, log
