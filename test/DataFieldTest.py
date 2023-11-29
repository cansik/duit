import unittest

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

    def test_to_string(self):
        self.a = DataField("a")
        self.assertEqual("DataField[str] (a)", str(self.a))


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
