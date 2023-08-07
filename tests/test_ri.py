# Test the set up of the ri class which serves as the basis for Glimmer
# tests hypercube/ri.py

import unittest

from .context import hypercube
from hypercube import ri

class TestRIClass(unittest.TestCase):

    def setUp(self):
        #runs before each test in class
        self.ri = ri.ri("leger1983", [1, 2, 3], [200, 200, 200], "pe", [0.5, 0.4, 0.3], [0.2, 0.2, -0.2], [0.1, 0.1, 0.1], [0.1, 0.1, 0.1])

    def test_dataset_is_string(self):
        self.assertEqual(type(self.ri.dataset), type(""))

    def test_dataset_correct(self):
        self.assertEqual(self.ri.dataset, "leger1983")

    def test_wavel_is_array(self):
        self.assertEqual(type(self.ri.wavel), type([]))

    def test_wavels_are_floats(self):
        for wavel in self.ri.wavel:
            self.assertEqual(type(wavel), type(float(0.1)))
    
    def test_wavels_correct(self):
        self.assertEqual(self.ri.wavel, [1, 2, 3])

    def test_temp_is_float(self):
        for temp in self.ri.temp:
            self.assertEqual(type(temp), type(float(0.1)))
    
    def test_temp_correct(self):
        self.assertEqual(self.ri.temp, [200, 200, 200])

    def test_errortype_string(self):
        self.assertEqual(type(self.ri.errortype), type("hello"))

    def test_errortype_correct(self):
        self.assertEqual(self.ri.errortype, "pe")

    def test_k_is_array(self):
        self.assertEqual(type(self.ri.k), type([]))

    def test_ks_are_floats(self):
        for k in self.ri.k:
            self.assertEqual(type(k), type(float(0.1)))

    def test_k_correct(self):
        self.assertEqual(self.ri.k, [0.2, 0.2, -0.2])

    def test_n_is_array(self):
        self.assertEqual(type(self.ri.n), type([]))

    def test_ns_are_floats(self):
        for n in self.ri.n:
            self.assertEqual(type(n), type(float(0.1)))

    def test_n_correct(self):
        self.assertEqual(self.ri.n, [0.5, 0.4, 0.3])
        
    def test_k_array_same_length_as_wavel(self):
        self.assertEqual(len(self.ri.k), len(self.ri.wavel))

    def test_nmax_is_array(self):
        self.assertEqual(type(self.ri.nmax), type([]))

    def test_nmax_are_floats(self):
        for nmax in self.ri.nmax:
            self.assertEqual(type(nmax), type(float(0.1)))
    
    def test_nmax_correct(self):
        self.assertEqual(self.ri.nmax, [0.6, 0.5, 0.4])

    def test_nmin_is_array(self):
        self.assertEqual(type(self.ri.nmin), type([]))

    def test_nmin_are_floats(self):
        for nmin in self.ri.nmin:
            self.assertEqual(type(nmin), type(float(0.1)))

    def test_nmin_correct(self):
        self.assertEqual(self.ri.nmin, [0.4, 0.3, 0.2])

    def test_kmax_is_array(self):
        self.assertEqual(type(self.ri.kmax), type([]))

    def test_kmax_are_floats(self):
        for kmax in self.ri.kmax:
            self.assertEqual(type(kmax), type(float(0.1)))

    def test_kmax_correct(self):
        self.assertEqual(self.ri.kmax, [0.3, 0.3, -0.1])

    def test_kmin_is_array(self):
        self.assertEqual(type(self.ri.kmin), type([]))

    def test_kmin_are_floats(self):
        for kmin in self.ri.kmin:
            self.assertEqual(type(kmin), type(float(0.1)))

    def test_kmin_correct(self):
        self.assertEqual(self.ri.kmin, [0.1, 0.1, -0.3])
