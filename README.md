# Midterm Make-Up Project

Our project is an accumluation of scripts that pull data from iNaturalist and complile them into a CSV file. This CSV file is then pushed into the Species Distribution Model provided by the clients and output a heat map based on a specified species and month/year. To allow it to be interactive we have accumlated the neccessary code into a Jupyter Notebook file which takes user input to output the SDM image from the specified year/month for the specified species. We have included all necessary documentation to go along with our scripts.


System Requirements: Software: Python 3.6, R, Anaconda, Bash 
R Packages: rgdal, raster, sp, dismo, maptools

# Table of Content
- [Getting Started](https://github.com/foxtrotington/butterfly#getting-started-gathering-data)
- [How to Use](https://github.com/foxtrotington/butterfly#how-to-use-running-the-sdm)
- [Output](https://github.com/foxtrotington/butterfly#output)
- [Data Consolidation](https://github.com/foxtrotington/butterfly#data-consolidation) 
- [Runtimes](https://github.com/foxtrotington/butterfly#runtimes)

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
By running `data-consolidation.py` in the scripts_eddie folder, we were able to combine multiple observation CSVs together. By using observation id as the pivot point for joining all three CSVs, we were able to output a CSV with ~400,000 observation points from GBIF, Jeffs get_observation and downloading the iNaturalist data dump. This table is optimal for `run_sdm` consumption and will be here for the benefit of other teams. The file can be found under  `data/master_csv.csv`

# Runtimes:
	Estimated run time of gathering observation data and sorting via Pull_Sort.py: 36 minutes
	Estimated run time for running of the SDM: approximately 4 hours


# Troubleshooting:
Directories: We encountered an issue where the directories were not being created properly and we found that it was because we were not reseting the current directory.                            
Data Accessing: Data was missing lat/long values which we chose to fix by adding empty cells                       
Writing Data: We had issues writing the entire yearly data out and the fix was to write all month data for that year.

License: This program is released under the MIT license.

Contributors: Danielle Perry, Kensaku Okada, Eddie Ornelas, Alexander Farmer, Adrianna Salazar



