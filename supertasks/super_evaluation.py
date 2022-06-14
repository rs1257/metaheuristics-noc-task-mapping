from supertasks.super_end_to_end_response_time import *
from supertasks.super_communication_latency import *
from supertasks.super_computation_response_time import *
from tasks.gen import *
from supertasks.supertask import *
from shared.constants import BENCHMARK
import copy
import itertools
tasks = convert_tasks_to_supertasks(BENCHMARK)
grid = populate_topology(GRID_SIZE)
TASK_NUMBER = len(tasks)


def evaluate(individual):
    global tasks
    [t.set_core(individual[index]) for index, t in enumerate(tasks)]
    all_tasks = list(itertools.chain(*[i.get_subtasks() for i in tasks]))

    for i in all_tasks:
        index = i.get_task_dest()
        result = [x.get_core() for x in all_tasks if x.get_id() == index]
        result = -1 if result == [] else result[0]
        i.set_dest_core(result)

    # create a list for each core
    mapping = [[] for _ in range(CORE_NUMBER)]

    # for each core append which tasks are assigned to it
    for t in all_tasks:
        mapping[int(t.get_core())].append(t)

    # calculate unschedulable tasks now we know the allocations
    for core in mapping:
        taskset = [task for task in core]
        computational_response_time(taskset)

    for t in all_tasks:
        hops = calculate_hops(grid, t.get_core(), t.get_dest_core())
        t.set_latency(calculate_latency(hops, math.ceil(t.get_message_size() / FLIT_SIZE)))
    communication_latency(all_tasks, grid)

    return unschedulable_supertasks(all_tasks)


def test():
    ind = [8, 6, 7, 6, 2, 2, 7, 2, 5, 0, 1, 5, 6, 4, 3, 5, 3, 7, 8, 1, 4, 6, 8, 4, 0, 2, 2, 6, 8, 8, 7, 5]
    print(evaluate(ind))


if __name__ == '__main__':
    test()