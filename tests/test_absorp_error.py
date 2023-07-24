#Test absorp_error.py, which calculates the error on the imagianry index k from the error on the absorption coefficient, alpha, using a method presented in Leger et al. 1983

import unittest

from .context import glimmer
from glimmer import absorp_error
from glimmer import ri

class TestAbsorpError(unittest.TestCase):

    def setUp(self):
        #runs before each test in class
        self.ri1 = ri.ri("leger1983", 1, 200, 0.5, 0.2, 0, 0)
        self.ri2 = ri.ri("leger1983", 2, 200, 0.4, 0.2, 0, 0)
        self.ri3 = ri.ri("leger1983", 3, 200, 0.3, -0.2, 0, 0)
        
        self.ri = [self.ri1, self.ri2, self.ri3]

    def test_dks_are_list(self):
        result = absorp_error.leger(self.ri)
        self.assertEqual(type(result), type([]))

    def test_all_dks_filled(self):
        result = absorp_error.leger(self.ri)
        print("\ndks for Leger are ", result)
        self.assertEqual(len(result), len(ri.wavelength))

    def test_dks_are_floats(self):
        result = absorp_error.leger(self.ri)
        for i in result:
            self.assertEqual(type(i), type(float(0.1)))

    def test_dks_greater_than_min(self):
        #Hand-calculated minimum dk -- at lowest test wavelength (1), dk
        #(by the equation in absorp_error.py) is 0.0079577
        result = absorp_error.leger(self.ri)
        min_dk = min(result)
        self.assertGreaterEqual(min_dk, 0.0079577)

    def test_dks_less_than_max(self):
        #Hand calculated maximum dk at greatest wavelength
        result = absorp_error.leger(self.ri)
        max_dk = max(result)
        self.assertLessEqual(min_dk, 0.023873241463)

