import unittest
from tasks.task import Task
from schedulability.end_to_end_response_time import *
from schedulability.computation_response_time import *
from schedulability.communication_latency import *

t1 = Task()
t1.set_period(7)
t1.set_deadline(t1.get_period())
t1.set_comp_time(3)

t2 = Task()
t2.set_period(12)
t2.set_deadline(t2.get_period())
t2.set_comp_time(3)

t3 = Task()
t3.set_period(20)
t3.set_deadline(t3.get_period())
t3.set_comp_time(5)

t4 = Task()
t4.set_period(80)
t4.set_deadline(t4.get_period())
t4.set_comp_time(40)

t5 = Task()
t5.set_period(40)
t5.set_deadline(t5.get_period())
t5.set_comp_time(10)

t6 = Task()
t6.set_period(20)
t6.set_deadline(t6.get_period())
t6.set_comp_time(5)

t7 = Task()
t7.set_period(19)
t7.set_deadline(21)
t7.set_comp_time(40)


class TestOrderingMethods(unittest.TestCase):

    def test_dmpo_1(self):
        tasks = [t1, t2, t3]
        computational_response_time(tasks)

        self.assertEqual(1, t1.get_priority())
        self.assertEqual(2, t2.get_priority())
        self.assertEqual(3, t3.get_priority())

    def test_dmpo_2(self):
        tasks = [t4, t5, t6]
        computational_response_time(tasks)

        self.assertEqual(3, t4.get_priority())
        self.assertEqual(2, t5.get_priority())
        self.assertEqual(1, t6.get_priority())

    def test_rmpo_1(self):
        tasks = [t1, t2, t3]
        computational_response_time(tasks, type="rmpo")

        self.assertEqual(1, t1.get_priority())
        self.assertEqual(2, t2.get_priority())
        self.assertEqual(3, t3.get_priority())

    def test_rmpo_2(self):
        tasks = [t4, t5, t6]
        computational_response_time(tasks, type="rmpo")

        self.assertEqual(3, t4.get_priority())
        self.assertEqual(2, t5.get_priority())
        self.assertEqual(1, t6.get_priority())

    def test_rmpo_diff(self):
        tasks = [t5, t6, t7]
        computational_response_time(tasks, type="rmpo")

        self.assertEqual(3, t5.get_priority())
        self.assertEqual(2, t6.get_priority())
        self.assertEqual(1, t7.get_priority())

    def test_dmpo_diff(self):
        tasks = [t5, t6, t7]
        computational_response_time(tasks)

        self.assertEqual(3, t5.get_priority())
        self.assertEqual(1, t6.get_priority())
        self.assertEqual(2, t7.get_priority())

    def test_new_oderering(self):
        t1, t2, t3 = Task(), Task(), Task()
        t1.set_priority(3), t2.set_priority(1), t3.set_priority(2)
        t1.set_name("1"), t2.set_name("2"), t3.set_name("3")
        tasks = [t1, t2, t3]
        result = sort_tasks_priority(tasks)

        self.assertEqual("2", result[0].get_name())
        self.assertEqual("3", result[1].get_name())
        self.assertEqual("1", result[2].get_name())

