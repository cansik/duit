import pickle
import unittest

import numpy as np

from duit.model.DataField import DataField
from duit.model.DataList import DataList


class DataFieldTest(unittest.TestCase):
    def test_un_equal(self):
        self.a = DataField("a")
        self.b = DataField("b")
        self.assertFalse(self.a == self.b)

    def test_equal(self):
        self.a = DataField("a")
        self.b = DataField("a")
        self.assertTrue(self.a == self.b)

    def test_equal_numpy(self):
        data1 = np.zeros((15, 20, 3), dtype=np.uint8)
        data2 = np.zeros((15, 20, 3), dtype=np.uint8)

        self.a = DataField(data1)
        self.b = DataField(data2)

        self.assertTrue(self.a == self.b)

    def test_un_equal_numpy(self):
        data1 = np.zeros((15, 20, 3), dtype=np.uint8)
        data2 = np.ones((15, 10, 3), dtype=np.uint8)

        self.a = DataField(data1)
        self.b = DataField(data2)

        self.assertFalse(self.a == self.b)

    def test_to_string(self):
        self.a = DataField("a")
        self.assertEqual("DataField[str] (a)", str(self.a))

    def test_event_register(self):
        self.counter = 0
        self.a = DataField("a")

        @self.a.on_changed.register
        def on_change(value: str):
            self.counter += 1

        self.a.value = "b"
        self.a.value = "c"

        self.assertEqual(self.counter, 2)

    def test_pickle_datafield(self):
        self.a = DataField("a")
        data = pickle.dumps(self.a)
        self.ca = pickle.loads(data)

        self.assertEqual(self.a, self.ca)


class DataListTest(unittest.TestCase):
    def test_list(self):
        field = DataList([1, 2, 3])

        self.events_fired = 0

        def on_fire(value):
            self.events_fired += 1

        field.on_changed += on_fire

        field.append(5)
        field.append(7)

        self.assertEqual([1, 2, 3, 5, 7], field.value)
        self.assertEqual(2, self.events_fired)


if __name__ == '__main__':
    unittest.main()
