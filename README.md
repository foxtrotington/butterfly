Midterm Make-Up Project

Our project is an accumluation of scripts that pull data from iNaturalist and complile them into a CSV file. This CSV file is then pushed into the Species Distribution Model provided by the clients and output a heat map based on a specified species and month/year. To allow it to be interactive we have accumlated the neccessary code into a Jupyter Notebook file which takes user input to output the SDM image from the specified year/month for the specified species. We have included all necessary documentation to go along with our scripts and our Cyverse wiki is completely updated.

System Requirements:
Software: Python 3.6, R, Anaconda, Bash, (Maybe Access to HPC)
R Packages: rgdal, raster, sp, dismo, maptools

Getting Started: (Gathering Data)
1. Clone everything from Jeff Oliver's github via: git clone https://github.com/jcoliver/ebutterfly-sdm.git
2. Clone everything from our github via: git clone https://github.com/foxtrotington/butterfly.git
3. Aquire Data via running the Final_Request_Solution.py script in the PythonSDM folder of this github
4. Run the kensakulizer.py script

How to Use: (Running the SDM)
1.


License:
This program is released under the MIT license.

Contributors:
Danielle Perry, Kensaku Okada, Eddie Ornelas, Alexander Farmer, Adrianna Salazar




