from metaheuristics.rm_parallel import *
from metaheuristics.ga import *
from metaheuristics.ga_diff import *
from metaheuristics.pso import *
from metaheuristics.aco import *
from metaheuristics.sa import *
from metaheuristics.sa_diff import *
from metaheuristics.tabu import *
from metaheuristics.tabu_diff import *
from timeit import default_timer as timer
from visualisation.display_mapping import *
import matplotlib.pyplot as plt
import pickle
import datetime
from parameter_sweep.after_sweep import hibernate
from shared.timeit_decorator import times

def pickle_result(filename, result):
    with open(filename, 'wb') as f:
        pickle.dump(result, f, protocol=pickle.HIGHEST_PROTOCOL)


def get_directory(benchmark):
    directory = "data\\" + benchmark + "\\"
    if not os.path.exists(directory):
        os.mkdir(directory)
    return directory


def get_filename(alg_type):
    return get_directory(BENCHMARK_FOLDER) + alg_type + "-" + str(SIZEX) + "x" + str(SIZEY) + "-" + str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) + ".pkl"

def main():
    NRUN, NGEN, iterations, tabuiter = 100, 100, 10000, 167
    fitnesses = []
    mappings = []
    labels = []
    run = [False, False, False, False, False, False, False, False, True]
    ''' RM mapping '''
    if run[0]:
        print("RM Started")
        fitness_rm, mapping_rm, log = run_rm(pool, NRUN, iterations)
        fitnesses.append(fitness_rm)
        mappings.append(mapping_rm)
        labels.append('RM')
        pickle_result(get_filename("RM"), log)

    ''' GA parameters and mapping '''
    if run[1]:
        print("GA-A Started")
        CXPB, MUTPB = 0.8, 1
        inds = 100
        fitness_ga, mapping_ga, log = run_ga(pool, NRUN, NGEN, CXPB, MUTPB, inds)
        fitnesses.append(fitness_ga)
        mappings.append(mapping_ga)
        labels.append('GA-A')
        pickle_result(get_filename("GA-A"), log)

    if run[2]:
        print("GA-B Started")
        CXPB, MUTPB = 0.8, 1
        inds = 100
        fitness_ga_diff, mapping_ga_diff, log = run_ga_diff(pool, NRUN, NGEN, CXPB, MUTPB, inds)
        fitnesses.append(fitness_ga_diff)
        mappings.append(mapping_ga_diff)
        labels.append('GA-B')
        pickle_result(get_filename("GA-B"), log)

    ''' PSO parameters and mapping '''
    if run[3]:
        print("PSO Started")
        inds = 100
        phi1, phi2, smin, smax, pmin, pmax = 3, 3, -2, 2, 0, CORE_NUMBER - 1
        fitness_pso, mapping_pso, log = run_pso(pool, NRUN, NGEN, phi1, phi2, smin, smax, pmin, pmax, inds)
        fitnesses.append(fitness_pso)
        mappings.append(mapping_pso)
        labels.append('PSO')
        pickle_result(get_filename("PSO"), log)

    ''' ACO parameters and mapping '''
    if run[4]:
        print("ACO Started")
        alpha, beta, evaprate = 1, 1, 0.2
        ants = 100
        fitness_aco, mapping_aco, log = run_aco(pool, NRUN, NGEN, alpha, beta, evaprate, ants)
        fitnesses.append(fitness_aco)
        mappings.append(mapping_aco)
        labels.append('ACO')
        pickle_result(get_filename("ACO"), log)

    ''' Tabu parameters and mapping '''
    if run[5]:
        print("Tabu-A Started")
        candidates = 60
        tabu_size = 60
        fitness_tabu, mapping_tabu, log = run_tabu(pool, NRUN, tabuiter, tabu_size, candidates)
        fitnesses.append(fitness_tabu)
        mappings.append(mapping_tabu)
        labels.append('Tabu-A')
        pickle_result(get_filename("Tabu-A"), log)

    if run[6]:
        print("Tabu-B Started")
        candidates = 60
        tabu_size = 60
        fitness_tabu_diff, mapping_tabu_diff, log = run_tabu_diff(pool, NRUN, tabuiter, tabu_size, candidates)
        fitnesses.append(fitness_tabu_diff)
        mappings.append(mapping_tabu_diff)
        labels.append('Tabu-B')
        pickle_result(get_filename("Tabu-B"), log)

    ''' SA parameters and mapping '''
    if run[7]:
        print("SA-A Started")
        temp_max, cooling_rate = 10000, 0.96
        fitness_sa, mapping_sa, log = run_sa(NRUN, iterations, temp_max, cooling_rate)
        fitnesses.append(fitness_sa)
        mappings.append(mapping_sa)
        labels.append('SA-A')
        pickle_result(get_filename("SA-A"), log)

    if run[8]:
        print("SA-B Started")
        temp_max, cooling_rate = 10000, 0.96
        fitness_sa_diff, mapping_sa_diff, log = run_sa_diff(NRUN, iterations, temp_max, cooling_rate)
        fitnesses.append(fitness_sa_diff)
        mappings.append(mapping_sa_diff)
        labels.append('SA-B')
        pickle_result(get_filename("SA-B"), log)

    hibernate(100)
    ''' Metaheuristic boxplots '''
    print(fitnesses)
    print(times)
    plt.boxplot(fitnesses)
    plt.xticks([i + 1 for i in range(len(labels))], labels)
    plt.xlabel("Metaheuristics")
    plt.ylabel("Unschedulable Tasks")
    plt.show()

    for m in mappings:
        show_task_mapping(m)


if __name__ == '__main__':
    import multiprocessing

    pool = multiprocessing.Pool()
    main()
