import unittest
import numpy as np
from devoir2 import Devoir2
from solution_exacte import SolutionExacte

class TestDevoir2(unittest.TestCase):
    def test_Devoir2_coup1(self):
        rbi1 = np.array([0.00, 0.50, 1.10])
        vbi1 = np.array([4.00, 0.00, 0.80])
        wbi1 = np.array([0.00, -70.00, 0.00])

        coup, vbf, ti, x, y, z = Devoir2(1, rbi1, vbi1, wbi1)
        solution = SolutionExacte(1, rbi1, vbi1, wbi1)

        self.assertEqual(coup, solution[0])
        np.testing.assert_array_almost_equal(vbf, solution[1], decimal=2)
        self.assertAlmostEqual(ti[-1], solution[2], places=2)
        self.assertAlmostEqual(x[-1], solution[3], places=2)
        self.assertAlmostEqual(y[-1], solution[4], places=2)
        self.assertAlmostEqual(z[-1], solution[5], places=2)

    def test_Devoir2_coup2(self):
        rbi2 = np.array([0.00, 0.40, 1.14])
        vbi2 = np.array([10.00, 1.00, 0.20])
        wbi2 = np.array([0.00, 100.00, -50.00])

        coup, vbf, ti, x, y, z = Devoir2(1, rbi2, vbi2, wbi2)
        solution = SolutionExacte(1, rbi2, vbi2, wbi2)

        self.assertEqual(coup, solution[0])
        np.testing.assert_array_almost_equal(vbf, solution[1], decimal=2)
        self.assertAlmostEqual(ti[-1], solution[2], places=2)
        self.assertAlmostEqual(x[-1], solution[3], places=2)
        self.assertAlmostEqual(y[-1], solution[4], places=2)
        self.assertAlmostEqual(z[-1], solution[5], places=2)

    def test_Devoir2_coup3(self):
        rbi3 = np.array([2.74, 0.50, 1.14])
        vbi3 = np.array([-5.00, 0.00, 0.20])
        wbi3 = np.array([0.00, 100.00, 0.00])

        coup, vbf, ti, x, y, z = Devoir2(1, rbi3, vbi3, wbi3)
        solution = SolutionExacte(1, rbi3, vbi3, wbi3)

        self.assertEqual(coup, solution[0])
        np.testing.assert_array_almost_equal(vbf, solution[1], decimal=2)
        self.assertAlmostEqual(ti[-1], solution[2], places=2)
        self.assertAlmostEqual(x[-1], solution[3], places=2)
        self.assertAlmostEqual(y[-1], solution[4], places=2)
        self.assertAlmostEqual(z[-1], solution[5], places=2)

    def test_Devoir2_coup4(self):
        rbi4 = np.array([0.00, 0.30, 1.00])
        vbi4 = np.array([10.00, -2.00, 0.20])
        wbi4 = np.array([0.00, 10.00, -100.00])

        coup, vbf, ti, x, y, z = Devoir2(1, rbi4, vbi4, wbi4)
        solution = SolutionExacte(1, rbi4, vbi4, wbi4)

        self.assertEqual(coup, solution[0])
        np.testing.assert_array_almost_equal(vbf, solution[1], decimal=2)
        self.assertAlmostEqual(ti[-1], solution[2], places=2)
        self.assertAlmostEqual(x[-1], solution[3], places=2)
        self.assertAlmostEqual(y[-1], solution[4], places=2)
        self.assertAlmostEqual(z[-1], solution[5], places=2)

if __name__ == '__main__':
    unittest.main()
