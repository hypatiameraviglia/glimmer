#Test Monte Carlo pertubation of RI values within error bars to estimate error introduced by spline

import unittest

from .context import hypercube
from hypercube import calc_wiggled
from hypercube import ri

class TestCalcWiggled(unittest.TestCase):

    def setUp(self):
        #runs before each test in class
        self.ri = ri.ri("leger1983", [1, 2, 3], [200, 200, 200], "pe", [0.5, 0.4, 0.3], [0.2, 0.2, -0.2], [0, 0, 0], [0, 0, 0])

    def test_wiggled_ris_are_list(self):
        result = calc_wiggled.wiggle_indices_n_times(self.ri)
        print("\nresult is ", result)
        self.assertEqual(type(result), type([]))

    def test_wiggled_ris_are_n_long(self):
        result = calc_wiggled.wiggle_indices_n_times(self.ri)
        print("\nresult is ", result)
        self.assertEqual(len(result), calc_wiggled.num_wiggled_indices)

    #TODO: How can we test the average and stdev without taking the integration of the spline? What did Conor say about this?

