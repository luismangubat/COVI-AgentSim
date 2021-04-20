import unittest
from store0.model import load
import numpy as np
import simpy
from covid19sim.locations import store0


class Store0ModelTestCase(unittest.TestCase):
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


class Store0TestCase(unittest.TestCase):
    def test_queue(self):
        env = simpy.Environment()
        env.process(store0.Store0(env).pulse())
        env.run(2*10e4)
        self.assertEqual(True, True)

    def test_predict(self):
        s = store0.Store0()
        sample = np.array([0., 0., 0., 0., 0., 0., 2., 0., 5.]).reshape(1, -1, 1)
        assert sample.shape == (1, 9, 1)
        y = s.model(sample).numpy()
        self.assertEqual(y, np.array([0.]).reshape(1, 1))

    def test_init(self):
        s = store0.Store0()
        assert s.history_queue.shape == (9, 1)
        self.assertEqual(True, True)

    def test_predict(self):
        s = store0.Store0()
        y = s.predict()
        assert y.shape == (1, 1)
        self.assertEqual(True, True)

    def test_save(self):
        s = store0.Store0()
        h = np.array([0.,]).reshape(1, 1)
        s.save(h)
        assert s.history_queue.shape == (9, 1)
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
