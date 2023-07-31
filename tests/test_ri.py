# Test the set up of the ri class which serves as the basis for Glimmer
# tests hypercube/ri.py

import unittest

from .context import hypercube
from hypercube import ri

class TestRIClass(unittest.TestCase):

    def setUp(self):
        #runs before each test in class
        self.ri1 = ri.ri("toon1994", 1, 200, 0.5, 0.5, 0.2, 0.2)
        self.ri2 = ri.ri("toon1994", 2, 200, 0.4, 0.6, 0.2, 0.2)
        self.ri3 = ri.ri("toon1994", 3, 200, 0.3, -0.2, 0.2, 0.2)

        self.ri = [self.ri1, self.ri2, self.ri3]

    def test_dataset_is_string(self):
        self.assertEqual(type(self.ri[1].dataset), type(""))

    def test_wavel_is_array(self):
        self.assertEqual(type(self.ri.wavel), type([]))

    def test_wavels_are_floats(self):
        for wavel in self.ri.wavel:
            self.assertEqual(type(wavel), type(float(0.1)))
    
    # If these fail, add float conversion to ri.py init function
    
    def test_temp_is_float(self):
        for temp in self.ri.temp:
            self.assertEqual(type(temp), type(float(0.1)))

    def test_k_is_array(self):
        self.assertEqual(type(self.ri.k), type([]))

    def test_ks_are_floats(self):
        for k in self.ri.k:
            self.assertEqual(type(k), type(float(0.1)))

    def test_k_array_same_length_as_wavel(self):
        self.assertEqual(len(self.ri.k), len(self.ri.wavel))
