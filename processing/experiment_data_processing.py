import os
import pickle
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
import scikit_posthocs as sp
import pandas
from copy import deepcopy
import random


def load_data(file):
    with open(file, 'rb') as f:
        b = pickle.load(f)
    return b


def plot_runs_ga():
    b = load_data(f)
    fit = b.chapters['fitness'].select("min")
    runs = []
    data = []
    limit = 0
    for i, j in zip(b, fit):
        # print(i, j)
        if limit > 0:
            break
        if i['gen'] == 99 or j == 0 and i['run'] not in runs:
            runs.append(i['run'])
            data.extend([data[-1]] * (100 - len(data)))
            plt.plot(range(100), deepcopy(data), markersize=3, linewidth=1, markeredgecolor='black', markeredgewidth=0.1)
            data = []
            limit += 1
        else:
            data.append(j)
    plt.xlabel("Generations")
    plt.ylabel("Unschedulable Supertasks")
    plt.title("GA")
    plt.show()

    #plt.plot(fit, range(100), '.-', label="Test", markersize=3, linewidth=1, markeredgecolor='black', markeredgewidth=0.1)


def plot_runs_pso():
    b = load_data(f)
    fit = b.chapters['fitness'].select("min")
    data = []
    limit = 0
    for i, j in zip(b, fit):
        # print(i, j)
        if limit > 0:
            break
        if i['gen'] == 99 or j == 0:
            data.extend([data[-1]] * (100 - len(data)))
            plt.plot(range(100), deepcopy(data), markersize=3, linewidth=1, markeredgecolor='black', markeredgewidth=0.1)
            data = []
            limit += 1
        else:
            data.append(j)
    plt.xlabel("Generations")
    plt.ylabel("Unschedulable Supertasks")
    plt.title("PSO")
    plt.show()


def plot_runs_ts():
    b = load_data(f)
    data = []
    limit = 0
    for i in b:
        # print(i, j)
        if limit > 0:
            break
        if i['iter'] == 166 or i['fit'] == 0:
            data.extend([data[-1]] * (167 - len(data)))
            plt.plot(range(167), deepcopy(data), markersize=3, linewidth=1, markeredgecolor='black', markeredgewidth=0.1)
            data = []
            limit += 1
        else:
            data.append(i['fit'])
    plt.xlabel("Iterations")
    plt.ylabel("Unschedulable Supertasks")
    plt.title("TS")
    plt.show()


def plot_runs_sa():
    b = load_data(f)
    data = []
    limit = 0
    for i in b:
        # print(i, j)
        if limit > 0:
            break
        if i['iter'] == 9999 or i['fit'] == 0:
            data.extend([data[-1]] * (10000 - len(data)))
            plt.plot(range(10000), deepcopy(data), markersize=3, linewidth=1, markeredgecolor='black', markeredgewidth=0.1)
            data = []
            limit += 1
        else:
            data.append(i['fit'])
    plt.xlabel("Iterations")
    plt.ylabel("Unschedulable Supertasks")
    plt.title("SA")
    plt.show()


def plot_runs_aco():
    b = load_data(f)
    fit = b.chapters['fitness'].select("min")
    data = []
    limit = 0
    for i, j in zip(b, fit):
        # print(i, j)
        if limit > 0:
            break
        if i['gen'] == 99 or j == 0:
            data.extend([data[-1]] * (100 - len(data)))
            plt.plot(range(100), deepcopy(data), markersize=3, linewidth=1, markeredgecolor='black', markeredgewidth=0.1)
            data = []
            limit += 1
        else:
            data.append(j)
    plt.xlabel("Generations")
    plt.ylabel("Unschedulable Supertasks")
    plt.title("ACO")
    plt.show()


# for illustrative purpose
def plot_runs_rm():
    b = load_data(f)
    data = []
    for i in range(10000):
        data.append(random.randint(30, 48))
    plt.plot(range(10000), deepcopy(data), markersize=3, linewidth=1, markeredgecolor='black', markeredgewidth=0.1)
    plt.xlabel("Iterations")
    plt.ylabel("Unschedulable Supertasks")
    plt.title("RM")
    plt.show()


def eval_ga():
    b = load_data(f)
    fit = b.chapters['fitness'].select("min")
    total_gens = 0
    total_evals = 0
    total_fitness = 0
    best_fitness = []
    t_fitness = []
    runs = []
    for i, j in zip(b, fit):
        # print(i, j)
        total_evals += i['evals']
        if i['gen'] == 99 or j == 0 and i['run'] not in runs:
            total_gens += i['gen'] + 1
            total_fitness += j
            t_fitness.append(total_fitness)
            runs.append(i['run'])
            best_fitness.append(j)
            #print(i['run'], j)
    return total_evals, total_gens, total_fitness, best_fitness, t_fitness


def eval_pso():
    b = load_data(f)
    fit = b.chapters['fitness'].select("min")
    total_gens = 0
    total_evals = 0
    total_fitness = 0
    best_fitness = []
    best = 100
    t_fitness = []
    for i, j in zip(b, fit):
        #print(i, j)
        if j < best:
            best = j
            #print("new best", best)
        if i['gen'] == 99 or j == 0:
            total_fitness += best
            t_fitness.append(total_fitness)
            best_fitness.append(best)
            best = 100
            # index starts at 0 so add 1 to the number of generations
            total_gens += i['gen'] + 1
            total_evals += (i['gen'] + 1) * 100

    return total_evals, total_gens, total_fitness, best_fitness, t_fitness


def eval_tabu():
    b = load_data(f)
    total_iter = 0
    total_evals = 0
    total_fitness = 0
    best_fitness = []
    t_fitness = []
    for i in b:
        ##################Check these numbers are now correct....
        # print(i, j)
        if i['iter'] == 166 or i['fit'] == 0:
            total_iter += i['iter'] + 1
            total_fitness += i['fit']
            t_fitness.append(total_fitness)
            best_fitness.append(float(i['fit']))

    total_evals += (total_iter * 60) + 1

    return total_evals, total_iter, float(total_fitness), best_fitness, t_fitness


def eval_rm():
    b = load_data(f)
    total_iter = 0
    total_evals = 0
    total_fitness = 0
    best_fitness = []
    t_fitness = []
    for i in b:
        # print(i, j)
        if i['iter'] == 9999 or i['fit'] == 0:
            total_iter += i['iter'] + 1
            total_fitness += i['fit']
            t_fitness.append(total_fitness)
            best_fitness.append(float(i['fit']))
            #print(i['fit'])

    total_evals += total_iter
    return total_evals, total_iter, float(total_fitness), best_fitness, t_fitness


def eval_rm_parallel():
    b = load_data(f)
    total_iter = 0
    total_evals = 0
    total_fitness = 0
    best_fitness = []
    t_fitness = []
    for i in b:
        # print(i, j)
        total_iter += 10000
        total_fitness += i['fit']
        t_fitness.append(total_fitness)
        best_fitness.append(float(i['fit']))
        #print(i['fit'])

    total_evals += total_iter
    return total_evals, total_iter, float(total_fitness), best_fitness, t_fitness


def eval_aco():
    b = load_data(f)
    fit = b.chapters['fitness'].select("min")
    total_gens = 0
    total_evals = 0
    total_fitness = 0
    best_fitness = []
    t_fitness = []
    runs = []
    for i, j in zip(b, fit):
        # print(i, j)
        if i['gen'] == 99 or j == 0 and i['run'] not in runs:
            total_gens += i['gen'] + 1
            total_evals += (i['gen'] + 1) * 100
            total_fitness += j
            t_fitness.append(total_fitness)
            runs.append(i['run'])
            best_fitness.append(j)
            #print(i['run'], j)
    return total_evals, total_gens, total_fitness, best_fitness, t_fitness


def eval_sa():
    b = load_data(f)
    total_iter = 0
    total_evals = 0
    total_fitness = 0
    best_fitness = []
    t_fitness = []
    for i in b:
        # print(i, j)
        if i['iter'] == 9999 or i['fit'] == 0:
            total_iter += i['iter'] + 1
            total_fitness += i['fit']
            t_fitness.append(total_fitness)
            best_fitness.append(float(i['fit']))

    total_evals += total_iter
    return total_evals, total_iter, float(total_fitness), best_fitness, t_fitness


def stat_tests(data):
    print(data)
    print(stats.kruskal(*[alg for alg in data]))
    pandas.set_option('display.max_columns', None)
    pandas.set_option('display.float_format', lambda x: '%.2g' % x)

    with open('out' + benchmark + '.csv', 'w', newline='') as f:
        result = sp.posthoc_dunn([alg for alg in data])
        print(result)
        result.to_csv(path_or_buf=f, float_format="%.2g")

    '''The Kruskal–Wallis test by ranks, Kruskal–Wallis H test[1] (named after William Kruskal and W. Allen Wallis), 
    or one-way ANOVA on ranks[1] is a non-parametric method for testing whether samples originate from the same 
    distribution.[2][3][4] It is used for comparing two or more independent samples of equal or different sample sizes. 
    It extends the Mann–Whitney U test, which is used for comparing only two groups. The parametric equivalent of the 
    Kruskal–Wallis test is the one-way analysis of variance (ANOVA).

    A significant Kruskal–Wallis test indicates that at least one sample stochastically dominates one other sample. 
    The test does not identify where this stochastic dominance occurs or for how many pairs of groups stochastic 
    dominance obtains. For analyzing the specific sample pairs for stochastic dominance, Dunn's test,[5] pairwise 
    Mann-Whitney tests without Bonferroni correction,[6] or the more powerful but less well known Conover–Iman test[6] 
    are sometimes used.

    Since it is a non-parametric method, the Kruskal–Wallis test does not assume a normal distribution of the residuals, 
    unlike the analogous one-way analysis of variance. If the researcher can make the assumptions of an identically 
    shaped and scaled distribution for all groups, except for any difference in medians, then the null hypothesis 
    is that the medians of all groups are equal, and the alternative hypothesis is that at least one population median 
    of one group is different from the population median of at least one other group.
    
    From wikipedia
    '''


if __name__ == '__main__':
    benchmark = "B1"
    folder = "../metaheuristics/data/" + benchmark + "/"
    files = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    print("Loading: " + ', '.join(files))
    #files = ['../parameter_sweep/data/PSO/P1/1-1-1-2019-02-08-12-15-29.pkl']
    fitnesses = []
    totals = []
    for f in files:
        fitness, t, evals, itergen, totalfit = None, None, None, None, None
        if "GA" in f:
            print("GA")
            evals, itergen, totalfit, fitness, t = eval_ga()
            plot_runs_ga()
        elif "PSO" in f:
            print("PSO")
            evals, itergen, totalfit, fitness, t = eval_pso()
            plot_runs_pso()
        elif "Tabu" in f:
            print("TS")
            evals, itergen, totalfit, fitness, t = eval_tabu()
            plot_runs_ts()
        elif "ACO" in f:
            print("ACO")
            evals, itergen, totalfit, fitness, t = eval_aco()
            plot_runs_aco()
        elif "SA" in f:
            print("SA")
            evals, itergen, totalfit, fitness, t = eval_sa()
            plot_runs_sa()
        elif "RM" in f:
            print("RM")
            evals, itergen, totalfit, fitness, t = eval_rm_parallel()
            plot_runs_rm()
        if fitness or t:
            fitnesses.append(fitness)
            totals.append(t)
        print(evals, itergen, totalfit)
        print(min(fitness), max(fitness), np.median(fitness), np.mean(fitness), round(float(np.std(fitness)), 2))

    #fix minor error of 1 extra run
    for x, y in enumerate(zip(fitnesses, totals)):
        if len(y[0]) > 100:
            fitnesses[x] = y[0][:100]
            totals[x] = y[1][:100]
    #print(len(fitnesses[-1]))
    #print(len(totals[-1]))

    labels = ['ACO', 'GA-A', 'GA-B', 'PSO', 'RM', 'SA-A', 'SA-B', 'TS-A', 'TS-B']

    plt.boxplot(fitnesses, whis='range', meanline=True, showmeans=True)
    plt.xticks([i + 1 for i in range(len(labels))], labels)
    plt.xlabel("Metaheuristics")
    plt.ylabel("Unschedulable Supertasks")
    plt.show()
    stat_tests(fitnesses)
    #print(totals)
    runs = len(totals[0])

    #annotations = [(runs, i[-1]) for i in totals]
    #plt.xlim(1, 10)
    lines = []
    for count, i in enumerate(totals):
        lines.append(plt.plot([j + 1 for j in range(runs)], i, '.-', label=labels[count], markersize=3, linewidth=1, markeredgecolor='black', markeredgewidth=0.1))

    #for count, a in enumerate(annotations):
    #    print(a)
        #plt.annotate(labels[count], xy=(a[0]+(runs*0.01), a[1]), va="center", color=lines[count][0].get_color())
    #    plt.annotate(labels[count], xy=(a[0] + (runs * 0.01), a[1]), va="center", fontsize=8)

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, 1.16),
              ncol=5, fancybox=True, shadow=True)
    plt.xlabel("Runs")
    plt.ylabel("Unschedulable Supertasks")
    plt.show()