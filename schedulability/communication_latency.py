import numpy as np
from shared.constants import *
from schedulability.ordering import *


def populate_topology(grid_size):
    grid = np.empty([grid_size[0], grid_size[1]])
    count = 0
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            grid[i][j] = count
            count += 1

    return grid


def calculate_latency(hops, flits):
    return 0 if hops == 0 else (hops * LINK_LATENCY) + ((hops - 1) * ROUTER_LATENCY) + (flits * LINK_LATENCY)


def calculate_hops(grid, src, des):
    # this checks if its on the same core so no hops
    if src == des:
        return 0

    x0, y0 = np.where(grid == src)
    target = des

    positions = np.where(grid == target)
    x, y = positions

    dx = abs(x0 - x)  # Horizontal distance
    dy = abs(y0 - y)  # Vertical distance

    return (dx + dy) + 2  # add 2 to get to src router and des cpu


def common_link(src1, des1, src2, des2, grid):
    #  assume x then y for routing
    values1 = calc_nodes_visited(src1, des1, grid)
    values2 = calc_nodes_visited(src2, des2, grid)

    return len(set(values1).intersection(values2)) > 0


def calc_nodes_visited(src, des, grid):
    values = [src, des]
    x0, y0 = np.where(grid == src)
    x, y = np.where(grid == des)
    x0, y0, x, y = int(x0), int(y0), int(x), int(y)
    x1, y1 = x0, y0
    # do x
    while x1 != x:
        x1 += -1 if x1 > x else 1
        values.append(int(grid[x1][y1]))
    # then do y
    while y1 != y:
        y1 += -1 if y1 > y else 1
        values.append(int(grid[x1][y1]))

    return set(values)


def communication_latency(taskset, grid, ind, type="dmpo"):
    sorted_tasks = sort_tasks(taskset, type)
    interf = []
    for t in sorted_tasks:
        result = t.get_latency()
        last = -1
        while result != last:
            c = t.get_latency()
            interference = 0
            for i in interf:
                if common_link(ind[t.get_id()], ind[t.get_task_dest()], ind[i.get_id()], ind[i.get_task_dest()], grid):
                    if i.get_period() > 0:
                        interference += np.ceil(
                            (result + i.get_rta() + i.get_ki()) / float(i.get_period())) * i.get_latency()
                    else:
                        interference += 0
            if interference > (t.get_deadline() * 10):  # if its way over the limit skip useless iterations
                t.set_comm_latency(1000000)
                break
            last = result
            result = c + interference
            t.set_comm_latency(result)
            t.set_ki(t.get_comm_latency() - t.get_latency())
        interf.append(t)
