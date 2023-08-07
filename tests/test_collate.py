# Tests collate.py, which combines experimental data from multiple studies into
# one ri object

import unittest
import os

from .context import hypercube
from hypercube import collate
from hypercube import ri

class TestCollate(unittest.TestCase):

    def setUp(self):
        self.directory = "./tests"

# Tests of read_all_data
    def test_ri_list_is_array(self):
        ri_list = collate.read_all_data(ri, self.directory)
        self.assertEqual(type(ri_list), type([]))

    def test_ris_are_ris(self):
        ri_list = collate.read_all_data(ri, self.directory)
        for obj in ri_list:
            self.assertEqual(type(obj), type(ri))

    def test_ri_list_len_equal_to_num_files(self):
        num_files = 0

        for filename in os.listdir(self.directory):
            if filename.endswith('.txt'):
                num_files += 1
                # Should equal 2, hardcode if it continue to cause issues

        ri_list = collate.read_all_data(ri, self.directory)

        self.assertEqual(len(ri_list), num_files)

# Tests of avg_stacked_pts
    def test_avgd_ks_in_array(self):
        avgd_ri_list = collate.avg_stacked_pts(collate.read_all_data(ri, self.directory))
        self.assertEqual(type(avgd_ri_list.k), type([]))

    def test_avgd_ks_are_floats(self):
        avgd_ri_list = collate.avg_stacked_pts(collate.read_all_data(ri, self.directory))
        for ri in avgd_ri_list:
            for k in ri.k:
                self.assertEqual(type(k), type(float(0.1)))

    def test_adjd_dks_in_array(self):
        avgd_ri_list = collate.avg_stacked_pts(collate.read_all_data(ri, self.directory))
        self.assertEqual(tyep(avgd_ri_list.dk), type([]))

    def test_adjd_dks_are_floats(self):
        avgd_ri_list = collate.avg_stacked_pts(collate.read_all_data(ri, self.directory))
        for obj in avgd_ri_list:
            for dk in obj.dk:
                self.assertEqual(type(dk), type(float(0.1)))

    def test_avgd_ks_correct(self):
        avgd_ri_list = collate.avg_stacked_pts(collate.read_all_data(ri, self.directory))
        for i in range(len(avgd_ri_list)):
            if avgd_ri_list.wavel[i] == 2.5:
                # Hand-calculated from test_data files
                self.assertEqual(avgd_ri_list.k[i], 0.5)

    def test_adjd_dks_correct(self):
        avgd_ri_list = collate.avg_stacked_pts(collate.read_all_data(ri, self.directory))
        for i in range(len(avgd_ri_list)):
            if avgd_ri_list.wavel[i] == 2.5:
                #Hand-calculated from test_data files
                self.assertEqual(avgd_ri_list.dk[i], 0.1)

# Tests of collate
    def test_collated_wavels_in_array(self):
        collated_ri = collate.collate(ri, collate.avg_stacked_pts(collate.read_all_data(ri, self.directory)))
        self.assertEqual(type(collated_ri.wavel), type([]))

    def test_collated_wavels_are_floats(self):
        collated_ri = collate.collate(ri, collate.avg_stacked_pts(collate.read_all_data(ri, self.directory)))
        for wavel in collated_ri.wavel:
            self.assertEqual(type(wavel), type(float(0.1)))

    def test_collated_temps_in_array(self):
        collated_ri = collate.collate(ri, collate.avg_stacked_pts(collate.read_all_data(ri, self.directory)))
        self.assertEqual(type(collated_ri.temp), type([]))

    def test_collated_temps_are_floats(self):
        collated_ri = collate.collate(ri, collate.avg_stacked_pts(collate.read_all_data(ri, self.directory)))
        for temp in collated_ri.temp:
            self.assertEqual(type(temp), type(float(0.1)))

    def test_collated_ks_in_array(self):
        collated_ri = collate.collate(ri, collate.avg_stacked_pts(collate.read_all_data(ri, self.directory)))
        self.assertEqual(type(collated_ri.k), type([]))

    def test_collated_ks_are_floats(self):
        collated_ri = collate.collate(ri, collate.avg_stacked_pts(collate.read_all_data(ri, self.directory)))
        for k in collated_ri.k:
            self.assertEqual(type(k), type(float(0.1)))

    def test_collated_dks_in_array(self):
        collated_ri = collate.collate(ri, collate.avg_stacked_pts(collate.read_all_data(ri, self.directory)))
        self.assertEqual(type(collated_ri.dk), type([]))

    def test_collated_dks_are_floats(self):
        collated_ri = collate.collate(ri, collate.avg_stacked_pts(collate.read_all_data(ri, self.directory)))
        for dk in collated_ri.dk:
            self.assertEqual(type(dk), type(float(0.1)))

    def test_no_stacked_coordinates(self):
        collated_ri = collate.collate(ri, collate.avg_stacked_pts(collate.read_all_data(ri, self.directory)))
        testvalue = True
        for wavel_i in collated_ri.wavel:
            for wavel_j in collated_ri.wavel:
                for temp_i in collated_ri.temp:
                    for temp_j in collated_ri.temp:
                        if wavel_i == wavel_j and temp_i == temp_j:
                            testvalue = False
        self.assertTrue(testvalue, "Stacked points persisting after collation")

    def test_avgd_ks_correct(self):
        collated_ri = collate.collate(ri, collate.avg_stacked_pts(collate.read_all_data(ri, self.directory)))
        for i in range(len(collated_ri)):
            if collated_ri.wavel[i] == 2.5:
                self.assertEqual(collated_ri.k[i], 0.5)
                #Hand calculated avg of 0 and 1

    def test_adjd_dks_correct(self):
        collated_ri = collate.collate(ri, collate.avg_stacked_pts(collate.read_all_data(ri, self.directory)))
        for i in range(len(collated_ri)):
            if collated_ri.wavel == 2.5:
                self.assertEqual(collated_ri.dk[i], 0.1)
                #Hand calculated combined error between 20% and 30% of 1 and 0 respectively. See collate.avg_stacked_pts for equation

