import unittest

from duit.model.DataList import DataList


class DataFieldTest(unittest.TestCase):
    def basic_data_model_test(self):
        self.assertEqual(True, False)  # add assertion here


class DataListTest(unittest.TestCase):
    def test_list(self):
        field = DataList([1, 2, 3])

        def on_fire(value):
            print(f"list has changed: {value}")

        field.on_changed += on_fire

        field.append(5)
        field.append(7)

        for i in field:
            print(i)


if __name__ == '__main__':
    unittest.main()
