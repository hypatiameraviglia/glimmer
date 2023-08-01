#Tests error propogation through KKR
import unittest

from .context import hypercube
from hypercube import kkr_prop
from hypercube import ri

class TestCalcWiggled(unittest.TestCase):

    def setUp(self):
        #runs before each subtest
        self.ri = ri.ri("leger1983", [1, 2, 3], [200, 200, 200], "pe", [0.5, 0.4, 0.3], [0.2, 0.2, -0.2], [0, 0, 0], [0, 0, 0])
 
    def test_errors_are_list(self):
        result = kkr_prop.inv_fft(kkr_prop.fft_on_inv_wavel(self.ri)*kkr_prop.fft_on_k(self.ri))
        print("\nresult is ", result)
        self.IsInstance(result, [])
