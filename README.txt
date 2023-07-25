# glimmer
Open-source code and database of refractive indices and Mie scattering curves for water ice across spans of Enceladus-like conditions.

--> Quick start guide
	Glimmer is an open-source, community-oriented Python package designed to fill in gaps in the published, experimental water ice refractive index data. Refractive indices are an essential data source for a variety of applications, but Glimmer is specifically designed to fill in gaps in the record at conditions relevant to the southern plumes of Enceladus. Glimmer interpolates and extrapolates real and imaginary refractive indices (and their errors) across wavelength-temperature space, from 0.1 - 30 microns and 130 - 200 K. 

To get started with Glimmer: 
1. Clone the repo onto your local machine
	$ git clone https://github.com/hypatiameraviglia/glimmer

2. From Glimmer's root repositiory, install dependencies
	$ pip install -r requirements.txt

3. Run greenbutton.py to run all scripts in order
	$ python greenbutton.py

Glimmer will not be automatically updated with new experimental refractive index data, so be sure to review current literature and add new data to the /lit subdirectory in the correct format before beginning.

Glimmer is intended to be useful and responsive to the planetary atmospheres com
munity. If you have a change, critique, or suggestion, please feel free to submit a pull request or contact the dev at hmeravig@asu.edu.

--> Pulling data
The latest interpolations from Glimmer are accessible under the /database subdirectory, organized into four layers: real refractive index (n), imaginary refractive index (k), the error (including both experimental and interpolational) on the real index (dn), and the error on the imaginary index (dk). Within each file, the data is organized in a 2D array by wavelength and temperature. A searchable, more user-friendly method of distributing the interpolations is in the works.

--> In-depth design
For an exploration of the code structure, science of scattering, and math mechanics, look for
        
        Meraviglia, H. R., Nixon, C. A., Aslam, S., Neveu, M., Gold, R. E., Irwin, P. G. J., Eigenbrode, J. L., "Chasing Rainbows: New Solutions to Gaps in Refractive Indices for Enceladus’ Plumes," Icarus, in progress.

