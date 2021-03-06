# Metaheuristics NoC Task Mapping

Implemented Metaheuristics for the Task Mapping problem over Real-Time Networks-on-Chip. I have implemented the metaheuristics Genetic Algorithms, Particle Swarm optimisation, Simulated Annealing, Tabu Search and Ant Colony Optimisation. As well as Random Mapping to compare how these metaheuristics perform.

## Requirements

Python 3.7 (I know that Python 3.10 currently doesn't work but I have not tested others)

You need the following packages installed:

- deap==1.3.1
- matplotlib==3.5.2
- numpy==1.21.6
- pygame==2.1.2

Alternatively use the requirements.txt to install these `pip install -r requirements.txt`

## Running

Note: if you set runs (times to run an algorithm), number of generations or iterations (depending on the algorithm) to a large number it can take a very long time to complete.

`python main.py`

## Changing Algorithm to run

Go the main.py and there is a list that lets you choose which to run, it more than one is true then you will run more than one metaheuristic and they will be plotted to the same graph.

E.g. Runs the first two metaheuristics which are RM and GA-A

```python
run = [True, True, False, False, False, False, False, False, False]
```

E.g. This will only run RM

```python
run = [True, False, False, False, False, False, False, False, False]
```

It would be good in the future to allow you to specify these via the command line.

## Changing the Benchmark

The same benchmark is used and run across all of the metaheuristics, they can be found in the benchmarks folder. They are of varying difficulty, the more unschedulabled tasks at the end means its a harder benchmark.

You can change the benchmark used by altering the BENCHMARK_FOLDER variable in shared/constants.py

## Metaheuristic variants

There are some variants to the metaheuristics, if you look in the metaheuristics folder you can see some have diff, parallel or a number after their name, these are modified versions to see if some changes produce better results. Some of these variants are not run by main.py but it would not be difficult to add them (except the original RM, the parallel version was developed so it could be run the same way as the other algorithms and reduce the time it took to complete).

## Screenshots

An example of a boxplot where the Random Mapper (RM) produced mappings with an average of 47 unschedulable tasks.

![Alt text](screenshots/box-plot-RM.PNG?raw=true)

There is the ability to plot different metaheuristics against each other but setting run to true for multiple.

![Alt text](screenshots/box-plot-RM-GA-A.PNG?raw=true)

Shows the best task allocation produced by RM during a run.

![Alt text](screenshots/task-allocation-RM.PNG?raw=true)
