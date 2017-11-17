# get the grand to read the folloing file
# chmod u+x ../data/gbif/taxon-ids.txt
chmod u+x ./taxon_ids.txt
# chmod u+x ./taxon_ids_short.txt


# call kensakulizer. It download all observation data on taxon-id.txt, separate the data into each year and month.
# the csv files are stored on data/inaturalist
python kensakulizer.py

# get the list of taxon ids removing a header
# this does not work
# taxon_ids= cat ../data/gbif/taxon-ids.txt | cut -f 1 | tail -n +2 $taxon_ids
# this works if there is the file on the designated path
# taxon_ids=$(cat ../data/gbif/taxon-ids.txt | cut -f 1 | tail -n +2 $taxon_ids)
# taxon_ids=$(cat ./taxon-ids.txt | cut -f 1 | tail -n +2 $taxon_ids)
taxon_ids=$(cat ./taxon-ids-short.txt | cut -f 1 | tail -n +2 $taxon_ids)
echo '$taxon_ids'
echo $taxon_ids

echo 'get_obs_run_sdm_per_month loop start'
echo $(date '+%y/%m/%d %H:%M:%S')

# for loop for each taxon id
for taxon_id in $taxon_ids
do

	# get the file and folder list in a designated filder
	# get the years having the observations of each taxon id: if the folers named the year exist, we can say there is at least one csv file inside.  
	yearList=$(ls -1 ./data/inaturalist/$taxon_id)

	# echo 'year is '
	# echo $yearList

	# make directories for the year(s)
	# mkdir 

	# loop by year
	for year in $yearList
	do

		# get the file and folder name list in a designated filder		
		# get the months having the observations of each taxon id: if the folers named the month exist, we can say there is at least one csv file inside.
		monthList=$(ls -1 ./data/inaturalist/$taxon_id/$year)


		# loop by month
		for month in $monthList
		do
		# get the month from each file name d = delimiter (`-`)
		# month=$(basename $filename | cut -d '-' -f 3)

		echo 'run-sdm.R loop start. taxon id is ' $taxon_id ' and year is ' $year ' and month is ' $month
		echo $(date '+%y/%m/%d %H:%M:%S')

		# make the output folder if does not exist
		mkdir -p ../data/sdm_results/$taxon_id/$year/$month

		# run SDM file
		# Rscript --vanilla run-sdm.R <path/to/data/file> <output-file-prefix> <path/to/output/directory/>
		# old command
		# Rscript --vanilla run_sdm.R ./data/inaturalist/$taxon_id-iNaturalist.csv $taxon_id ../output/$taxon_id
		Rscript --vanilla run_sdm.R ./data/inaturalist/$taxon_id/$year/$month/$taxon_id-$year-$month.csv $taxon_id ../output/$taxon_id/$year/$month
		echo 'run-sdm.R loop end.'
		echo $(date '+%y/%m/%d %H:%M:%S')

		done

	done

done


echo 'get_obs_run_sdm_per_month loop end'
echo $(date '+%y/%m/%d %H:%M:%S')


exit

##########################################################

# old code for record below

# get only the filename from the file path 
# $(basename $file | cut -d '-' -f 1)
# hoge="52773-2005-08"
# echo $hoge|cut -d "-" -f 3
# # Aにでーたを入れたいけどできない。do from here
# a=$(basename $hoge | cut -d '-' -f 3) 
# echo $a


# exit

# for taxon_id in $taxon_ids
# do
# 	echo "taxon id: $taxon_id"

# 	# make a directory to store the output for each taxon id
# 	mkdir ../output/$taxon_id

# 	# get the list of all file names having monthly raw data
# 	fileNameList= ls -1 ./data/inatualist/$taxon_id
# 	# fileNameList= ls -1 ./data/inaturalist/52773
# 	echo $fileNameList

# 	for filename in $fileNameList
# 	do
	
# 		# get the month from each file name d = delimiter (`-`)
# 		month=$(basename $filename | cut -d '-' -f 3)
# 		# TODO: this has not been vaerified
# 		# yearMonth=$(basename $filename | cut -d '-' -f 3)


# 		# Rscript --vanilla run-sdm.R <path/to/data/file> <output-file-prefix> <path/to/output/directory/>
# 		Rscript --vanilla run_sdm.R ./data/inaturalist/$taxon_id-iNaturalist.csv $taxon_id ../output/$taxon_id
# 	done

# 	count=$(( count + 1 ))
# 	echo  "for loop count finished: $count"
# 	echo $(date '+%y/%m/%d %H:%M:%S')

# done
