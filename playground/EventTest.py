import unittest

from duit.event.Event import Event


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

    def test_check_has_event(self):
        def fire_first(value: int):
            print(f"First: {value}")

        def fire_second(value: int):
            print(f"Second: {value}")

        event = Event[int]()
        event.append(fire_first)
        event += fire_second

        assert fire_second in event

    def test_remove_event(self):
        def fire_first(value: int):
            print(f"First: {value}")

        def fire_second(value: int):
            print(f"Second: {value}")

        event = Event[int]()
        event.append(fire_first)
        event += fire_second

        event -= fire_second

        assert fire_second not in event


if __name__ == '__main__':
    unittest.main()
