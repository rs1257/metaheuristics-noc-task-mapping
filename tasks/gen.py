from tasks.task import *
from shared.constants import *


def create_tasks(file):
    tasks = []
    for t in range(TASK_GEN_NUMBER):
        task = Task()
        task.set_id(t)
        task.set_period(random.randint(MIN_PERIOD, MAX_PERIOD))
        task.set_deadline(task.period_)
        task.set_comp_time(random.randint(MIN_COMP_TIME, MAX_COMP_TIME))
        task.set_message_size(2 ** random.randint(MIN_MESSAGE_SIZE, MAX_MESSAGE_SIZE))
        task.set_task_dest(random.randint(0, TASK_GEN_NUMBER - 1))
        tasks.append(task)

    if os.path.exists(file):
        os.remove(file)
    f = open(file, 'a')
    for t in tasks:
        t.save(f)
    f.close()


def load_tasks(file):
    tasks = []
    with open(file, 'r') as f:
        content = f.readlines()
        for d in content:
            data = d.split(",")
            task = Task()
            task.set_id(int(data[0]))
            task.set_period(int(data[1]))
            task.set_deadline(int(data[2]))
            task.set_comp_time(int(data[3]))
            task.set_message_size(int(data[4]))
            task.set_task_dest(int(data[5]))
            tasks.append(task)
        # for t in tasks:
        # print(t)
    return tasks


def load_tasks_ava_simple(file):
    tasks = []
    f = open(file, 'r')
    content = f.readlines()
    for d in content:
        data = d.replace(", ", ",").split(",")
        task = Task()
        task.set_id(int(data[0]) - 1)
        task.set_period(int(data[5]))
        task.set_deadline(int(data[5]))
        task.set_comp_time(float(data[4]))
        task.set_message_size(int(data[7]))
        task.set_task_dest(int(data[3]) - 1)
        tasks.append(task)
    # for t in tasks:
    #    print(t)
    return tasks


if __name__ == '__main__':
    for i in range(NO_BENCHMARKS):
        f = FOLDER_LOCATION + FILE_NAME + str(i) + EXTENSION
        create_tasks(f)

    # load_tasks(FILE)
