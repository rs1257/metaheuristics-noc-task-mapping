from schedulability.end_to_end_response_time import *
from schedulability.computation_response_time import *
from schedulability.communication_latency import *
import copy
from tasks.gen import *

#tasks = load_tasks("benchmarks/Tasks.txt")
tasks = load_tasks_ava_simple("benchmarks/ava.txt")
grid = populate_topology(GRID_SIZE)

TASK_NUMBER = len(tasks)


def evaluate(individual):
    global tasks
    current = copy.deepcopy(tasks)

    # create a list for each core
    mapping = [[] for _ in range(CORE_NUMBER)]

    # for each core append which tasks are assigned to it
    for task, core in enumerate(individual):
        mapping[core].append(task)

    # calculate unschedulable tasks now we know the allocations
    for i in mapping:
        taskset = [current[a] for a in i]
        computational_response_time(taskset)

    for t in current:
        hops = calculate_hops(grid, individual[t.get_id()], individual[t.get_task_dest()])
        t.set_latency(calculate_latency(hops, math.ceil(t.get_message_size() / FLIT_SIZE)))
    communication_latency(current, grid, individual)

    return unschedulable_tasks(current)


def reset():
    global tasks, grid, TASK_NUMBER

    tasks = load_tasks("benchmarks/Tasks.txt")
    grid = populate_topology(GRID_SIZE)

    TASK_NUMBER = len(tasks)