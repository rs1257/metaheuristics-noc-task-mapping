import unittest
from schedulability.end_to_end_response_time import *
from tasks.task import Task
import math
from schedulability.computation_response_time import *
from schedulability.communication_latency import *

grid3 = populate_topology([3, 3])
grid4 = populate_topology([4, 4])
grid5 = populate_topology([5, 5])

t1 = Task()
t1.set_period(7)
t1.set_deadline(t1.get_period())
t1.set_comp_time(3)
t1.set_priority(1)

t2 = Task()
t2.set_period(12)
t2.set_deadline(t2.get_period())
t2.set_comp_time(3)
t2.set_priority(2)

t3 = Task()
t3.set_period(20)
t3.set_deadline(t3.get_period())
t3.set_comp_time(5)
t3.set_priority(3)

t4 = Task()
t4.set_period(80)
t4.set_deadline(t4.get_period())
t4.set_comp_time(40)
t4.set_priority(3)

t5 = Task()
t5.set_period(40)
t5.set_deadline(t5.get_period())
t5.set_comp_time(10)
t5.set_priority(2)

t6 = Task()
t6.set_period(20)
t6.set_deadline(t6.get_period())
t6.set_comp_time(5)
t6.set_priority(1)

t7 = Task()
t7.set_period(79)
t7.set_deadline(t7.get_period())
t7.set_comp_time(40)
t7.set_priority(3)

t8 = Task()
t8.set_period(5)
t8.set_deadline(t8.get_period())
t8.set_comp_time(1)
t8.set_priority(1)

t9 = Task()
t9.set_period(7)
t9.set_deadline(t9.get_period())
t9.set_comp_time(2)
t9.set_priority(2)

t10 = Task()
t10.set_period(9)
t10.set_deadline(t10.get_period())
t10.set_comp_time(1)
t10.set_priority(3)

t11 = Task()
t11.set_period(13)
t11.set_deadline(t11.get_period())
t11.set_comp_time(3)
t11.set_priority(4)

t12 = Task()
t12.set_period(36)
t12.set_deadline(t12.get_period())
t12.set_comp_time(4)
t12.set_priority(5)

t13 = Task()
t13.set_id(0)
t13.set_period(100)
t13.set_deadline(t13.get_period())
t13.set_comp_time(8)
t13.set_message_size(50)
t13.set_task_dest(2)

t14 = Task()
t14.set_id(1)
t14.set_period(75)
t14.set_deadline(t14.get_period())
t14.set_comp_time(5)
t14.set_message_size(64)
t14.set_task_dest(0)

t15 = Task()
t15.set_id(2)
t15.set_period(60)
t15.set_deadline(t15.get_period())
t15.set_comp_time(7)
t15.set_message_size(32)
t15.set_task_dest(1)


class TestEERMethods(unittest.TestCase):

    def test_rta_correct_result_1(self):
        tasks = [t1, t2, t3]
        computational_response_time(tasks)

        self.assertEqual(3, t1.get_rta())
        self.assertEqual(6, t2.get_rta())
        self.assertEqual(20, t3.get_rta())

    def test_rta_correct_result_2(self):
        tasks = [t4, t5, t6]
        computational_response_time(tasks)
        self.assertEqual(80, t4.get_rta())
        self.assertEqual(15, t5.get_rta())
        self.assertEqual(5, t6.get_rta())

    def test_rta_unschedulable(self):
        tasks = [t7, t5, t6]
        computational_response_time(tasks)
        self.assertEqual(80, t7.get_rta())
        self.assertEqual(15, t5.get_rta())
        self.assertEqual(5, t6.get_rta())

    def test_rta_harder(self):
        tasks = [t8, t9, t10, t11, t12]
        computational_response_time(tasks)
        self.assertEqual(1, t8.get_rta())
        self.assertEqual(3, t9.get_rta())
        self.assertEqual(4, t10.get_rta())
        self.assertEqual(12, t11.get_rta())
        self.assertEqual(34, t12.get_rta())

    def test_correct_hops(self):
        self.assertEqual(6, calculate_hops(grid3, 0, 8))
        self.assertEqual(4, calculate_hops(grid3, 0, 2))

        self.assertEqual(8, calculate_hops(grid4, 0, 15))
        self.assertEqual(5, calculate_hops(grid4, 0, 3))

        self.assertEqual(10, calculate_hops(grid5, 0, 24))
        self.assertEqual(8, calculate_hops(grid5, 0, 18))

    def test_calc_latency(self):
        self.assertEqual(31.0 / CLOCK_SPEED, round(calculate_latency(10, 12), 5))
        self.assertEqual(39.0 / CLOCK_SPEED, round(calculate_latency(3, 34), 5))
        self.assertEqual(221.0 / CLOCK_SPEED, round(calculate_latency(60, 102), 5))

    def test_common_link_1_grid3(self):
        v1 = calc_nodes_visited(4, 0, grid3)
        self.assertEqual({0, 1, 4}, v1)

        v2 = calc_nodes_visited(2, 4, grid3)
        self.assertEqual({2, 4, 5}, v2)

        self.assertEqual({4}, v1.intersection(v2))
        self.assertEqual(True, common_link(4, 0, 2, 4, grid3))

    def test_common_link_2_grid3(self):
        v1 = calc_nodes_visited(5, 0, grid3)
        self.assertEqual({0, 1, 2, 5}, v1)

        v2 = calc_nodes_visited(7, 0, grid3)
        self.assertEqual({0, 1, 4, 7}, v2)

        self.assertEqual({0, 1}, v1.intersection(v2))
        self.assertEqual(True, common_link(5, 0, 7, 0, grid3))

    def test_common_link_1_grid4(self):
        v1 = calc_nodes_visited(0, 15, grid4)
        self.assertEqual({0, 4, 8, 12, 13, 14, 15}, v1)

        v2 = calc_nodes_visited(9, 3, grid4)
        self.assertEqual({1, 2, 3, 5, 9}, v2)

        self.assertEqual(set(), v1.intersection(v2))
        self.assertEqual(False, common_link(0, 15, 9, 3, grid4))

    def test_common_link_1_grid5(self):
        v1 = calc_nodes_visited(5, 24, grid5)
        self.assertEqual({5, 10, 15, 20, 21, 22, 23, 24}, v1)

        v2 = calc_nodes_visited(18, 6, grid5)
        self.assertEqual({6, 7, 8, 13, 18}, v2)

        self.assertEqual(set(), v1.intersection(v2))
        self.assertEqual(False, common_link(5, 24, 18, 6, grid5))

    def test_same_core(self):
        v1 = calc_nodes_visited(24, 24, grid5)
        self.assertEqual({24}, v1)

        # no latency as it doesnt have to move core
        self.assertEqual(0, calculate_latency(calculate_hops(grid5, 24, 24), 24))

    def test_eer_latency(self):
        grid = grid3
        taskset = [t13, t14, t15]
        mapping = [0, 4, 2]
        h1 = calculate_hops(grid, mapping[t13.get_id()], mapping[t13.get_task_dest()])
        h2 = calculate_hops(grid, mapping[t14.get_id()], mapping[t14.get_task_dest()])
        h3 = calculate_hops(grid, mapping[t15.get_id()], mapping[t15.get_task_dest()])
        self.assertEqual(4, h1)
        self.assertEqual(4, h2)
        self.assertEqual(4, h3)

        t13.set_latency(calculate_latency(h1, math.ceil(t13.get_message_size() / 32)))
        t14.set_latency(calculate_latency(h2, math.ceil(t14.get_message_size() / 32)))
        t15.set_latency(calculate_latency(h3, math.ceil(t15.get_message_size() / 32)))

        self.assertAlmostEqual(9 / CLOCK_SPEED, float(t13.get_latency()), 4)
        self.assertAlmostEqual(9 / CLOCK_SPEED, float(t14.get_latency()), 4)
        self.assertAlmostEqual(8 / CLOCK_SPEED, float(t15.get_latency()), 4)

        computational_response_time(taskset)
        self.assertEqual(3, t13.get_priority())
        self.assertEqual(2, t14.get_priority())
        self.assertEqual(1, t15.get_priority())
        self.assertEqual(20, t13.get_rta())
        self.assertEqual(12, t14.get_rta())
        self.assertEqual(7, t15.get_rta())
        communication_latency(taskset, grid, mapping)
        self.assertAlmostEqual(8 / CLOCK_SPEED, float(t15.get_comm_latency()), 4)
        self.assertAlmostEqual(17 / CLOCK_SPEED, float(t14.get_comm_latency()), 4)
        self.assertAlmostEqual(26 / CLOCK_SPEED, float(t13.get_comm_latency()), 4)

        self.assertAlmostEqual(0.0 / CLOCK_SPEED, float(t15.get_ki()))
        self.assertAlmostEqual(8.0 / CLOCK_SPEED, float(t14.get_ki()))
        self.assertAlmostEqual(17.0 / CLOCK_SPEED, float(t13.get_ki()))

        unschedulable_tasks(taskset)
        self.assertEqual("Yes", t13.get_schedulable())
        self.assertEqual("Yes", t14.get_schedulable())
        self.assertEqual("Yes", t15.get_schedulable())
