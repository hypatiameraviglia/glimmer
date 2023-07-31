#Tests read_in_lit.py, which sort info from .txt files in literature directory 
#into objects of the class ri, defined in ri.py

import unittest

from .context import hypercube
from hypercube import read_in_lit
from hypercube import ri

import os

class TestReadInLit(unittest.TestCase):

    def setUp(self):
        directory = "~/scattering/tests"

# Tests of read_data

    def test_dataset_is_string(self):
        dataset = read_in_lit.read_data(directory).dataset
        self.assertEqual(type(dataset), type(""))

    def test_ks_in_array(self):
        k = read_in_lit.read_data(directory).k
        self.assertEqual(type(k), type([]))

    def test_ks_are_floats(self):
        k = read_in_lit.read_data(directory).k
        for i in k:
            self.assertEqual(type(i), type(float(0.1)))

    def test_wavels_in_array(self):
        wavel = read_in_lit.read_data(directory).wavel
        self.assertEqual(type(wavel), type([]))

    def test_wavels_are_floats(self):
        wavel = read_in_lit.read_data(directory).wavel
        for i in wavel:
            self.assertEqual(type(i), type(float(0.1)))

    def test_ks_same_len_as_wavels(self):
        k = read_in_lit.read_data(directory).k
        wavel = read_in_lit.read_data(directory).wavel
        self.assertEqual(len(k), len(wavel))

#Tests of get_error

    def test_dk_in_array(self):
        dk = read_in_lit.get_error(read_in_lit.read_data(directory)).dk
        self.assertEqual(type(dk), type([]))

    def test_dk_same_len_as_wavels(self):
        dk = read_in_lit.get_error(read_in_lit.read_data(directory)).dk
        wavel = read_in_lit.read_data(directory).wavel
        self.assertEqual(len(dk), len(wavel))

    def test_dks_are_floats(self):
        dk = read_in_lit.get_error(read_in_lit.read_data(directory)).dk
        for i in dk:
            self.assertEqual(type(i), type(float(0.1)))

    def test_error_value(self):
        k = read_in_lit.read_data(directory).k
        dk = read_in_lit.get_error().dk
        for i in dk:
            self.assertEqual(i/k, 0.20)
