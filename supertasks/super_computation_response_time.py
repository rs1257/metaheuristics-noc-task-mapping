import operator
import numpy as np
from tasks.task import Task
from schedulability.ordering import *


def computational_response_time(taskset):
    sorted_tasks = sort_tasks_priority(taskset)
    hp = []
    for t in sorted_tasks:
        result = t.get_comp_time()
        last = -1
        while result != last:
            c = t.get_comp_time()
            interference = 0
            for h in hp:
                if h.get_period() > 0:
                    interference += np.ceil(result / float(h.get_period())) * h.get_comp_time()
                else:
                    interference += 0
            if interference > (t.get_period()):  # if its way over the limit skip useless iterations
                t.set_rta(100000000)
                break
            last = result
            result = c + interference
            t.set_rta(result)
        hp.append(t)
