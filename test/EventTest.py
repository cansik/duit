import unittest

from simbi.event.Event import Event


class EventTest(unittest.TestCase):

    def test_basic_event(self):

        def fire_first(value: int):
            print(f"First: {value}")

        def fire_second(value: int):
            print(f"Second: {value}")

        event = Event[int]()
        event.append(fire_first)
        event += fire_second

        event(15)


if __name__ == '__main__':
    unittest.main()
