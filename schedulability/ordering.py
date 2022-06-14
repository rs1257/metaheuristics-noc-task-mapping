import operator


def sort_tasks(taskset, type):
    attrib = 'deadline_' if type == "dmpo" else 'period_'
    return sorted(taskset, key=operator.attrgetter(attrib))

def sort_tasks_priority(taskset):
    return sorted(taskset, key=operator.attrgetter('priority_'))