import os
import pickle


def load_data(file, no):
    with open(file, 'rb') as f:
        b = pickle.load(f)

    return b, file.split("/")[-1].split("-")[:no]


def eval_ga():
    b, params = load_data(f, 2)
    fit = b.chapters['fitness'].select("min")
    total_gens = 0
    total_evals = 0
    total_fitness = 0
    for i, j in zip(b, fit):
        # print(i, j)
        total_evals += i['evals']
        if i['gen'] == 99 or j == 0:
            total_gens += i['gen'] + 1
            total_fitness += j
    return params, total_evals, total_gens, total_fitness


def eval_pso():
    b, params = load_data(f, 3)
    fit = b.chapters['fitness'].select("min")
    total_gens = 0
    total_evals = 0
    total_fitness = 0
    best = 100
    for i, j in zip(b, fit):
        #print(i, j)
        if j < best:
            best = j
            #print("new best", best)
        if i['gen'] == 99 or j == 0:
            total_fitness += best
            best = 100
            # index starts at 0 so add 1 to the number of generations
            total_gens += i['gen'] + 1
            total_evals += (i['gen'] + 1) * 100

    return params, total_evals, total_gens, total_fitness


def get_correct_iter_count(params):
    if params[1] == 20:
        return 500 - 1
    elif params[1] == 40:
        return 250 - 1
    elif params[1] == 60:
        return 167 - 1
    elif params[1] == 80:
        return 125 - 1
    else:
        return 100 - 1


def eval_tabu():
    b, params = load_data(f, 2)
    total_iter = 0
    total_evals = 0
    total_fitness = 0
    for i in b:
        # print(i, j)
        if i['iter'] == get_correct_iter_count(params[1]) or i['fit'] == 0:
            total_iter += i['iter'] + 1
            total_fitness += i['fit']

    total_evals += (total_iter * int(params[1])) + 1

    return params, total_evals, total_iter, total_fitness


def eval_aco():
    b, params = load_data(f, 3)
    #print(b)
    fit = b.chapters['fitness'].select("min")
    total_gens = 0
    total_evals = 0
    total_fitness = 0
    best = 100
    for i, j in zip(b, fit):
        # print(i, j)
        if j < best:
            best = j
            # print("new best", best)
        if i['gen'] == 99 or j == 0:
            total_fitness += best
            best = 100
            # index starts at 0 so add 1 to the number of generations
            total_gens += i['gen'] + 1
            total_evals += (i['gen'] + 1) * 100

    return params, total_evals, total_gens, total_fitness


def eval_sa():
    b, params = load_data(f, 2)
    total_gens = 0
    total_evals = 0
    total_fitness = 0
    best = 100
    for i in b:
        # print(i, j)
        if i['fit'] < best:
            best = i['fit']
            # print("new best", best)
        if i['iter'] == 9999 or i['fit'] == 0:
            total_fitness += best
            best = 100
            # index starts at 0 so add 1 to the number of generations
            total_gens += i['iter'] + 1
            total_evals += (i['iter'] + 1)

    return params, total_evals, total_gens, total_fitness


if __name__ == '__main__':
    algorithm = "ACO"
    benchmark = "P2"
    folder = "../parameter_sweep/data/" + algorithm + "/" + benchmark + "/"
    files = [os.path.join(folder, f) for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    print("Loading: " + ', '.join(files))

    i = 1
    for f in files:
        if algorithm == "GA":
            print(i, *eval_ga())
        elif algorithm == "PSO":
            print(i, *eval_pso())
        elif algorithm == "Tabu":
            print(i, *eval_tabu())
        elif algorithm == "ACO":
            print(i, *eval_aco())
        elif algorithm == "SA":
            print(i, *eval_sa())
        i+=1