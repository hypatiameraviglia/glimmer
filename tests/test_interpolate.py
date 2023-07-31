#Tests interpolate.py, which takes in a collated ri object containing all the 
# data from each study and interpolates n, k, dn, and dk within temperature/
# wavelength space

from .context import hypercube
from hypercube import interpolate
from hypercube import ri

class TestInterpolate(unittest.TestCase):

    def setUp(self):
        #Runs before each test within the class
        self.ri1 = ri.ri("toon1994", 1, 200, 0.5, 0.5, 0.2, 0.2)
        self.ri2 = ri.ri("warren1984", 2, 120, 0.4, 0.6, 0.2, 0.2)
        self.ri3 = ri.ri("toon1994", 3, 200, 0.3, -0.2, 0.2, 0.2)

        self.ri = [self.ri1, self.ri2, self.ri3]
    
    def temp_axis_is_array(self):
        temp_axis = interpolate.interpolate(self.ri)[1]
        self.assertEqual(type(temp_axis), type([]))

    def temp_axis_only_floats(self):
        temp_axis = interpolate.interpolate(self.ri)[1]
        for i in temp_axis:
            self.assertEqual(type(i), type(float(0.1)))

    def temp_axis_max(self):
        temp_axis = interpolate.interpolate(self.ri)[1]
        self.assertEqual(max(temp_axis), 200)

    def temp_axis_min(self):
        temp_axis = interpolate.interpolate(self.ri)[1]
        self.assertEqual(min(temp_axis), 120)

    def wavel_axis_is_array(self):
        wavel_axis = interpolate.interpolate(self.ri)[2]
        self.assertEqual(type(wavel_axis), type([]))

    def wavel_axis_only_floats(self):
        wavel_axis = interpolate.interpolate(self.ri)[2]
        for i in wavel_axis:
            self.assertEqual(type(i), type(float(0.1)))

    def wavel_axis_max(self):
        wavel_axis = interpolate.interpolate(self.ri)[2]
        self.assertEqual(min(wavel_axis), 1)

    def wavel_axis_max(self):
        wavel_axis = interpolate.interpolate(self.ri)[2]
        self.assertEqual(max(wavel_axis), 3)

    def n_axis_is_array(self):
        n_axis = interpolate.interpolate(self.ri)[3]
        self.assertEqual(type(n_axis), type([]))

    def n_axis_only_floats(self):
        n_axis = interpolate.interpolate(self.ri)[3]
        for i in n_axis:
            self.assertEqual(type(i), type(float(0.1)))

    def k_axis_is_array(self):
        k_axis = interpolate.interpolate(self.ri)[4]
        self.assertEqual(type(k_axis), type([]))

    def k_axis_only_floats(self):
        k_axis = interpolate.interpolate(self.ri)[4]
        for i in k_axis:
            self.assertEqual(type(i), type(float(0.1)))

    def dn_axis_is_array(self):
        dn_axis = interpolate.interpolate(self.ri)[5]
        self.assertEqual(type(dn_axis), type([]))

    def dn_axis_only_floats(self):
        dn_axis = interpolate.interpolate(self.ri)[5]
        for i in dn_axis:
            self.assertEqual(type(i), type(float(0.1)))

    def dk_axis_is_array(self):
        dk_axis = interpolate.interpolate(self.ri)[6]
        self.assertEqual(type(dk_axis), type([]))

    def dk_axis_only_floats(self):
        dk_axis = interpolate.interpolate(self.ri)[6]
        for i in dk_axis:
            self.assertEqual(type(i), type(float(0.1)))
