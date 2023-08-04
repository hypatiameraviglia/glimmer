#Test absorp_error.py, which calculates the error on the imagianry index k from the error on the absorption coefficient, alpha, using a method presented in Leger et al. 1983

import unittest

from .context import hypercube
from hypercube import absorp_error
from hypercube import ri

class TestAbsorpError(unittest.TestCase):

    def setUp(self):
        #runs before each test in class
        self.ri = ri.ri("leger1983", [1, 2, 3], [200, 200, 200], "pe", [0.5, 0.4, 0.3], [0.2, 0.2, -0.2], [0, 0, 0], [0, 0, 0])
        dalpha = 0.10
        dalpha_array = [0.10, 0.25, 0.30]

#Tests for calc_error_from_dalpha
    def test_dks_are_list(self):
        result = absorp_error.calc_error_from_dalpha(self.ri, dalpha)
        self.assertEqual(type(result), type([]))

    def test_all_dks_filled(self):
        result = absorp_error.calc_error_from_dalpha(self.ri, dalpha)
        print("\ndks for Leger are ", result)
        self.assertEqual(len(result), len(self.ri.wavel))

    def test_dks_are_floats(self):
        result = absorp_error.calc_error_from_dalpha(self.ri, dalpha)
        for i in result:
            self.assertEqual(type(i), type(float(0.1)))

    def test_dks_greater_than_min(self):
        #Hand-calculated minimum dk -- at lowest test wavelength (1), dk
        #(by the equation in absorp_error.py) is 0.0079577
        result = absorp_error.calc_error_from_dalpha(self.ri, dalpha)
        min_dk = min(result)
        self.assertGreaterEqual(min_dk, 0.0079577)

    def test_dks_less_than_max(self):
        #Hand calculated maximum dk at greatest wavelength
        result = absorp_error.calc_error_from_dalpha(self.ri, dalpha)
        max_dk = max(result)
        self.assertLessEqual(max_dk, 0.023873241463)

#Tests for calc_error_from_array
    def test_array_dks_are_array(self):
        result = absorp_error.perovich(self.ri, dalpha_array)
        self.assertEqual(type(result), type([]))

    def test_all_array_dks_filled(self):
        result = absorp_error.perovich(self.ri, dalpha_array)
        print("\ndks from test are ", result)
        self.assertEqual(len(result), len(self.ri.wavel))

    def test_array_dks_are_floats(self):
        result = absorp_error.perovich(self.ri, dalpha_array)
        for i in result:
            self.assertEqual(type(i), type(float(0.1)))

