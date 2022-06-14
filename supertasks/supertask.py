from supertasks.super_task import *

class SuperTask:
    id_ = -1
    name_ = ""
    subtasks_ = []
    core_ = -1

    def __init__(self):
        pass

    def set_id(self, id):
        self.id_ = id

    def get_id(self):
        return self.id_

    def set_name(self, name):
        self.name_ = name

    def get_name(self):
        return self.name_

    def set_subtasks(self, subtasks):
        self.subtasks_ = subtasks

    def get_subtasks(self):
        return self.subtasks_

    def count_subtasks(self):
        return len(self.subtasks_)

    def set_core(self, core):
        self.core_ = core
        for t in self.subtasks_:
            t.set_core(core)

    def get_core(self):
        return self.core_

    def __str__(self):
        return "Supertask: " + self.name_ + " Subtasks: " + ', '.join([t.get_name() for t in self.subtasks_])


def convert_tasks_to_supertasks(f):
    with open(f, 'r') as b:
        content = b.readlines()
        names = []
        tasks = []
        for d in content:
            data = d.replace(", ", ",").replace("\n", "").split(",")
            if not data[2][:4] in names:
                names.append(data[2][:4])
            tasks.append(data)

        supertasks = []
        for n in names:
            s = SuperTask()
            s.set_name(n)
            subtasks = []
            for t in tasks:
                if t[2].startswith(n):
                    # add other properties of tasks too
                    nt = Task()
                    nt.set_id(int(t[0]) - 1)
                    nt.set_name(t[2])
                    nt.set_task_dest(int(t[3]) - 1)
                    nt.set_comp_time(float(t[4]))
                    nt.set_period(float(t[5]))
                    nt.set_priority(int(t[6]))
                    nt.set_message_size(int(t[7]))
                    subtasks.append(nt)
            s.set_subtasks(subtasks)
            supertasks.append(s)
        return supertasks


if __name__ == '__main__':
    tasks = convert_tasks_to_supertasks("../benchmarks/ava.txt")
    print(len(tasks))


