#Tests error propogation through KKR
import unittest

from .context import hypercube
from hypercube import kkr_prop
from hypercube import ri

class TestCalcWiggled(unittest.TestCase):

    def setUp(self):
        #runs before each subtest
        self.ri1 = ri.ri("toon1994", 1, 200, 0.5, 0.5, 0.2, 0.2)
        self.ri2 = ri.ri("toon1994", 2, 200, 0.4, 0.6, 0.2, 0.2)
        self.ri3 = ri.ri("toon1994", 3, 200, 0.3, -0.2, 0.2, 0.2)

        self.ri = [self.ri1, self.ri2, self.ri3]
    
    def test_errors_are_list(self):
        result = kkr_prop.inv_fft(kkr_prop.fft_on_inv_wavel(self.ri)*kkr_prop.fft_on_k(self.ri))
        print("\nresult is ", result)
        self.IsInstance(result, [])

    def test
