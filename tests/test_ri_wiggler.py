#Tests ri_wiggler.py, which makes a copy of a set of indices and randomizes each point within the bounds of the error
import unittest

from .context import hypercube
from hypercube import ri_wiggler

class TestCalcWiggled(unittest.TestCase):

    def setUp(self):
        self.ri1 = ri.ri("toon1994", 1, 200, 0.5, 0.5, 0.2, 0.2)
        self.ri2 = ri.ri("toon1994", 2, 200, 0.4, 0.6, 0.2, 0.2)
        self.ri3 = ri.ri("toon1994", 3, 200, 0.3, -0.2, 0.2, 0.2)

        self.ri = [self.ri1, self.ri2, self.ri3]

    def copy_and_indices_at_different_location(self):
        original = ri_wiggler.read_ri(self.ri)
        copy = ri_wiggler.copy_ri(self.ri)
        self.assertNotEqual(id(original), id(copy))

    def copy_is_list(self):
        result = ri_wiggler.copy_ri(self.ri)
        self.IsInstance(result, [])

    def n_points_within_bounds(self):
        copy = ri_wiggler.copy_ri(self.ri)
        for index in copy:
            n_max = n + dn
            n_min = n - dn
            self.assertGreaterEqual(copy[index], n_min)
            self.assertLessEqual(copy[index], n_max)

    def k_points_within_bounds(self):
        copy = ri_wiggler.copy_ri(self.ri)
        for index in copy:
            k_max = k + dk
            k_min = k - dk
            self.assertGreaterEqual(copy[index], k_min)
            self.assertLessEqual(copy[index], k_max)

