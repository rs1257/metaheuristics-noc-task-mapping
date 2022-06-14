class Task:
    id_ = -1
    period_ = -1
    deadline_ = -1
    comp_time_ = -1
    message_size_ = -1
    task_dest_ = -1
    priority_ = -1
    rta_ = -1
    latency_ = -1
    ki_ = -1
    comm_latency_ = -1
    schedulable_ = "No"
    name_ = ""

    def __init__(self):
        pass

    def set_id(self, identifier):
        self.id_ = identifier

    def get_id(self):
        return self.id_

    def set_period(self, period):
        self.period_ = period

    def get_period(self):
        return self.period_

    def set_deadline(self, deadline):
        self.deadline_ = deadline

    def get_deadline(self):
        return self.deadline_

    def set_comp_time(self, comp_time):
        self.comp_time_ = comp_time

    def get_comp_time(self):
        return self.comp_time_

    def set_message_size(self, message_size):
        self.message_size_ = message_size

    def get_message_size(self):
        return self.message_size_

    def set_task_dest(self, task_dest):
        self.task_dest_ = task_dest

    def get_task_dest(self):
        return self.task_dest_

    def set_priority(self, priority):
        self.priority_ = priority

    def get_priority(self):
        return self.priority_

    def set_schedulable(self, schedulable):
        self.schedulable_ = schedulable

    def get_schedulable(self):
        return self.schedulable_

    def set_rta(self, rta):
        self.rta_ = rta

    def get_rta(self):
        return self.rta_

    def set_latency(self, latency):
        self.latency_ = latency

    def get_latency(self):
        return self.latency_

    def set_ki(self, ki):
        self.ki_ = ki

    def get_ki(self):
        return self.ki_

    def set_comm_latency(self, comm_latency):
        self.comm_latency_ = comm_latency

    def get_comm_latency(self):
        return self.comm_latency_

    def set_name(self, name):
        self.name_ = name

    def get_name(self):
        return self.name_

    def display(self):
        return [self.id_, self.period_, self.deadline_, self.comp_time_, self.message_size_, self.task_dest_,
                self.priority_, self.schedulable_]

    def save(self, f):
        f.write("%i, %i, %i, %i, %i, %i\n" % (self.id_, self.period_, self.deadline_, self.comp_time_,
                                              self.message_size_, self.task_dest_))

    def __str__(self):
        return "%i, %i, %i, %i, %i, %i" % (self.id_, self.period_, self.deadline_, self.comp_time_,
                                           self.message_size_, self.task_dest_)
