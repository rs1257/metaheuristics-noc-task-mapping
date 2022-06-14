def unschedulable_tasks_new(taskset):
    failed = 0
    for t in taskset:
        if t.get_rta() <= t.get_period() and t.get_rta() >= 0:
            t.set_schedulable("Yes")
        else:
            failed += 1
        if t.get_rta() + t.get_comm_latency() <= t.get_period() and t.get_rta() >= 0 and t.get_comm_latency() >= 0:
            t.set_schedulable("Yes")
        else:
            failed += 1
    return failed,

def unschedulable_tasks(taskset):
    failed = 0
    for t in taskset:
        if t.get_rta() + t.get_comm_latency() <= t.get_period() and t.get_rta() >= 0 and t.get_comm_latency() >= 0:
            t.set_schedulable("Yes")
        else:
            failed += 1
    return failed,

def unschedulable_supertasks(taskset):
    failed_tasks = []
    failed_flows = []
    for t in taskset:
        if t.get_rta() <= t.get_period() and t.get_period() >= 0:
            t.set_schedulable("Yes")
        else:
            failed_tasks.append(t.get_name()[:4])
        if t.get_rta() + t.get_comm_latency() <= t.get_period() and t.get_rta() >= 0 and t.get_comm_latency() >= 0:
            t.set_schedulable("Yes")
        else:
            failed_flows.append(t.get_name()[:4])
    tasks = len(failed_tasks)
    flows = len(failed_flows)
    super_tasks = len(set(failed_tasks))
    super_flows = len(set(failed_flows))
    # print(tasks, flows, super_tasks, super_flows)
    #if super_flows <= 1:
        #print(failed_flows)
        #print(failed_tasks)
    return super_flows,
