import unittest

import numpy as np

from duit.model.DataField import DataField
from duit.settings.Settings import Settings


class DemoConfig:
    def __init__(self):
        data = np.full(shape=(5, 3), fill_value=100, dtype=np.uint8)
        self.name = DataField("a")
        self.data = DataField(data)


class SerializerTest(unittest.TestCase):
    def test_default(self):
        config = DemoConfig()
        settings = Settings()

        data = settings.serialize(config)

        new_config = DemoConfig()
        new_config.data.value[:] = 0

        self.assertEqual(new_config.data.value[0][0], 0)

        settings.deserialize(data, new_config)
        self.assertTrue(np.array_equal(config.data.value, new_config.data.value))


if __name__ == '__main__':
    unittest.main()
