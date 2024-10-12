import unittest
import numpy as np
from devoir2 import Devoir2
from solution_exacte import SolutionExacte

class TestDevoir2(unittest.TestCase):
    def test_Devoir2_coup1_option0(self):
        option = 0
        rbi1 = np.array([0.00, 0.50, 1.10])
        vbi1 = np.array([4.00, 0.00, 0.80])
        wbi1 = np.array([0.00, -70.00, 0.00])

        coup, vbf, ti, x, y, z = Devoir2(option, rbi1, vbi1, wbi1)
        solution = SolutionExacte(0, rbi1, vbi1, wbi1)

        self.assertEqual(coup, solution[0])
        np.testing.assert_array_almost_equal(vbf, solution[1], decimal=3)
        self.assertAlmostEqual(ti[-1], solution[2], places=3)
        self.assertAlmostEqual(x[-1], solution[3], places=3)
        self.assertAlmostEqual(y[-1], solution[4], places=3)
        self.assertAlmostEqual(z[-1], solution[5], places=3)

if __name__ == '__main__':
    unittest.main()
