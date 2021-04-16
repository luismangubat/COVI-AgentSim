import unittest
from store0.model import load
import numpy as np


class Store0TestCase(unittest.TestCase):
    def test_load_model(self):
        m = load()
        print(m.summary)
        self.assertEqual(True, True)

    def test_predict(self):
        sample = np.array([0., 0., 0., 0., 0., 0., 2., 0., 5.]).reshape(1, -1, 1)
        assert sample.shape == (1, 9, 1)
        m = load()
        y = m(sample).numpy()
        self.assertEqual(y, np.array([0.]).reshape(1, 1))


if __name__ == '__main__':
    unittest.main()
