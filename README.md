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

Note: if it has lots of runs it can take a very long time to complete.

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

You can change the benchmark used by altering the BENCHMARK_FOLDER variable in shared/constants

## Screenshots

An example of a boxplot where the Random Mapper (RM) produced mappings with an average of 47 unschedulable tasks.

![Alt text](screenshots/box-plot-RM.PNG?raw=true)

There is the ability to plot different metaheuristics against each other but setting run to true for multiple.

![Alt text](screenshots/box-plot-RM-GA-A.PNG?raw=true)

Shows the best task allocation produced by RM during a run.

![Alt text](screenshots/task-allocation-RM.PNG?raw=true)
