def unschedulable_tasks(taskset):
    failed = 0
    for t in taskset:
        if t.get_rta() + t.get_comm_latency() <= t.get_deadline() and t.get_rta() >= 0 and t.get_comm_latency() >= 0:
            t.set_schedulable("Yes")
        else:
            failed += 1
    return failed,
