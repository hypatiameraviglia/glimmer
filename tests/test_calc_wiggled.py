#Test Monte Carlo pertubation of RI values within error bars to estimate error introduced by spline

import unittest

from .context import hypercube
from hypercube import calc_wiggled
from hypercube import ri

class TestCalcWiggled(unittest.TestCase):

    def setUp(self):
        #runs before each test in class
        self.ri = ri.ri("leger1983", [1, 2, 3], [200, 150, 180], "pe", [0.5, 0.4, 0.3], [0.2, 0.2, -0.2], [0, 0, 0], [0, 0, 0])

    def test_wiggled_ris_are_list(self):
        result = calc_wiggled.wiggle_indices_n_times(self.ri)[1]
        #print("\nresult is ", result)
        self.assertEqual(type(result), type([]))

    def test_wiggled_ris_are_n_long(self):
        result = calc_wiggled.wiggle_indices_n_times(self.ri)[1]
        #print("\nresult is ", result)
        self.assertEqual(len(result), calc_wiggled.num_wiggled_indices)

    def test_n_avg_is_above_min(self):
        result = calc_wiggled.extrapolate_wiggled_ris(calc_wiggled.wiggle_indices_n_times(self.ri))[0]
        #print("\nresult is ", result)
        nmin = 0.3 # Lowest n point in sample data
        for avg in result:
            self.assertGreater(avg, nmin)

    def test_n_avg_is_below_max(self):
        result = calc_wiggled.extrapolate_wiggled_ris(calc_wiggled.wiggle_indices_n_times(self.ri))[0]
        nmax = 0.5
        for avg in result:
            self.assertLess(avg, nmax)

    def test_k_avg_is_above_min(self):
        result = calc_wiggled.extrapolate_wiggled_ris(calc_wiggled.wiggle_indices_n_times(self.ri))[2]
        kmin = -0.2
        for avg in result:
            self.assertGreater(avg, kmin)

    def test_k_avg_is_below_max(self):
        result = calc_wiggled.extrapolate_wiggled_ris(calc_wiggled.wiggle_indices_n_times(self.ri))[2]
        kmax = 0.2
        for avg in result:
            self.assertLess(avg, kmax)

    def test_n_stdev_above_min(self):
        result = calc_wiggled.extrapolate_wiggled_ris(calc_wiggled.wiggle_indices_n_times(self.ri))[1]
        stdevmin = 0
        for stdev in result:
            self.assertGreater(stdev, stdevmin)

    def test_k_stdev_above_min(self):
        result = calc_wiggled.extrapolate_wiggled_ris(calc_wiggled.wiggle_indices_n_times(self.ri))[3]
        stdevmin = 0
        for stdev in result:
            self.assertGreater(stdev, stdevmin)

