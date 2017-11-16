Midterm Make-Up Project

Our project is an accumluation of scripts that pull data from iNaturalist and complile them into a CSV file. This CSV file is then pushed into the Species Distribution Model provided by the clients and output a heat map based on a specified species and month/year. To allow it to be interactive we have accumlated the neccessary code into a Jupyter Notebook file which takes user input to output the SDM image from the specified year/month for the specified species. We have included all necessary documentation to go along with our scripts and our Cyverse wiki is completely updated.

System Requirements: Software: Python 3.6, R, Anaconda, Bash, (Maybe Access to HPC) R Packages: rgdal, raster, sp, dismo, maptools

Getting Started: (Gathering Data)

1. Clone everything from our github via: git clone https://github.com/foxtrotington/butterfly.git
2. Aquire data via running the Final_Request_Solution.py script in the PythonSDM folder of this github
3. Run the kensakulizer.py script

How to Use: (Running the SDM)
1. Go to "PythonSDM" folder
2. Run "get_observation_data_run_sdm.sh"

You will see the SDM result divided by taxon id, year and month in "output" folder on the root directory. Is there is no observation in a month in a year for a taxon id, the folder does not exist.

If you just want the observation data from iNaturalist, run "data-puller.py" and you will get all observation raw data as csv files with the taxon id recorded in "taxon-id.txt".


Output:




License: This program is released under the MIT license.

Contributors: Danielle Perry, Kensaku Okada, Eddie Ornelas, Alexander Farmer, Adrianna Salazar


