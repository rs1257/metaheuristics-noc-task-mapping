import unittest
from supertasks.supertask import *


class TestSuperTaskMethods(unittest.TestCase):

    def test_convert_tasks_to_super(self):
        supertasks = convert_tasks_to_supertasks("testfiles/supertasks.txt")
        # check correct number of supertasks
        self.assertEqual(6, len(supertasks))

        # check correct names for supertasks
        self.assertEqual("ABCD", supertasks[0].get_name())
        self.assertEqual("RTQW", supertasks[1].get_name())
        self.assertEqual("RYEN", supertasks[2].get_name())
        self.assertEqual("POTY", supertasks[3].get_name())
        self.assertEqual("JPOY", supertasks[4].get_name())
        self.assertEqual("KDEH", supertasks[5].get_name())

        # check correct number of subtasks
        self.assertEqual(4, supertasks[0].count_subtasks())
        self.assertEqual(1, supertasks[1].count_subtasks())
        self.assertEqual(1, supertasks[2].count_subtasks())
        self.assertEqual(2, supertasks[3].count_subtasks())
        self.assertEqual(1, supertasks[4].count_subtasks())
        self.assertEqual(1, supertasks[5].count_subtasks())

        # check all subtasks have the correct name
        self.assertEqual("ABCD-A", supertasks[0].get_subtasks()[0].get_name())
        self.assertEqual("ABCD-D", supertasks[0].get_subtasks()[1].get_name())
        self.assertEqual("ABCD-B", supertasks[0].get_subtasks()[2].get_name())
        self.assertEqual("RTQW", supertasks[1].get_subtasks()[0].get_name())
        self.assertEqual("RYEN", supertasks[2].get_subtasks()[0].get_name())
        self.assertEqual("POTY-D", supertasks[3].get_subtasks()[0].get_name())
        self.assertEqual("POTY-F", supertasks[3].get_subtasks()[1].get_name())
        self.assertEqual("JPOY", supertasks[4].get_subtasks()[0].get_name())
        self.assertEqual("KDEH", supertasks[5].get_subtasks()[0].get_name())
