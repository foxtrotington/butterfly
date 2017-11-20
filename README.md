# Midterm Make-Up Project

Our project is an accumluation of scripts that pull data from iNaturalist and complile them into a CSV file. This CSV file is then pushed into the Species Distribution Model provided by the clients and output a heat map based on a specified species and month/year. To allow it to be interactive we have accumlated the neccessary code into a Jupyter Notebook file which takes user input to output the SDM image from the specified year/month for the specified species. We have included all necessary documentation to go along with our scripts.


System Requirements: Software: Python 3.6, R, Anaconda, Bash 
R Packages: rgdal, raster, sp, dismo, maptools

# Table of Content
[link text] (#getting-started) Getting Started
[link text] (https://github.com/foxtrotington/butterfly#how-to-use-running-the-sdm) How to Use
[link text] (https://github.com/foxtrotington/butterfly#output) Output
[link text] (https://github.com/foxtrotington/butterfly#data-consolidation) Data Consolidation
[link text] (https://github.com/foxtrotington/butterfly#runtimes) Runtimes

# <a name="getting-started"></a>Getting Started: (Gathering Data)

1. Clone everything from our github by running the command
   -> git clone https://github.com/foxtrotington/butterfly.git
2. Aquire data via
    Navigating to the PythonSDM folder -> cd butterfly/PythonSDM
    Then running the Pull_Sort script -> python Pull_Sort.py

# How to Use: (Running the SDM)
1. Navigate to PythonSDM folder
    -> cd butterfly/PythonSDM
2. Run "get_observation_data_run_sdm.sh" 
    -> python get_observation_data_run_sdm.sh

You will see the SDM result divided by taxon id, year, and month in "output" folder on the root directory. If you see there is no folder for a certain month, then there was no observation data for that month for that certain taxon id.

If you just want the observation data from iNaturalist:
    Run "data-puller.py" -> python data_puller.py
You will get all observation raw data as csv files with the taxon id recorded in "taxon-id.txt".

# Output:
![alt text](https://github.com/foxtrotington/butterfly/blob/master/52773-prediction_360.png) ![alt text](https://github.com/foxtrotington/butterfly/blob/master/52773-prediction_360%20(1).png)

# Data Consolidation
By running `data-consolidation.py` in the scripts_eddie folder, you can combine multiple observation CSVs together. All you need to do is give it paths to the CSV files and the headers you want from those CSVs. What should be generated if all the correct information is supplied is a master_csv file under `data/out/master_csv.csv`

# Runtimes:
	Estimated run time of gathering observation data and sorting via Pull_Sort.py: 36 minutes
	Estimated run time for running of the SDM: approximately 4 hours


License: This program is released under the MIT license.

Contributors: Danielle Perry, Kensaku Okada, Eddie Ornelas, Alexander Farmer, Adrianna Salazar



