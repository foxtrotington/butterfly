# get the grant to read the folloing file
# chmod u+x ../data/gbif/taxon-ids.txt
chmod u+x ./taxon-ids.txt
# chmod u+x ./taxon_ids_short.txt
chmod u+x ../data


#############################################
# read Pull_Sort.py start 
#############################################
# Once you get all observation data from iNaturalist， you do not need this process． you can comment it out.
echo -n "Do you want to run Pull_Sort.py to get raw observation data from iNaturalist? (y = yes, n = no):"
read ans

if [ $ans = "y" ]
then
	# call Pull_Sort.py. It download all observation data on taxon-id.txt, separate the data into each year and month.
	# the csv files are stored on data/inaturalist
	echo 'Pull_Sort.py start'
	echo $(date '+%y/%m/%d %H:%M:%S')
	python Pull_Sort.py
	echo 'Pull_Sort.py end'
	echo $(date '+%y/%m/%d %H:%M:%S')
elif [ $ans = "n" ]
then
	echo "you anwered no. continue the shell with the local raw observation data"
else
	echo "you inputthe wrong answer. exit the shell"
	exit
fi
#############################################
# read Pull_Sort.py end 
#############################################


# get the list of taxon ids removing a header
# this does not work
# taxon_ids= cat ../data/gbif/taxon-ids.txt | cut -f 1 | tail -n +2 $taxon_ids
# this works if there is the file on the designated path
# taxon_ids=$(cat ./taxon_ids.txt | cut -f 1 | tail -n +2 $taxon_ids)
# taxon_ids=$(cat ./taxon-ids-short.txt | cut -f 1 | tail -n +2 $taxon_ids)

# get all taxon id from the folders made by Pull_Sort.py
get all taxon id existing on ./data/inaturalist/
taxon_ids=$(ls -1 ./data/inaturalist/)
echo '$taxon_ids: ' $taxon_ids


#############################################
# run run_sdm.R start 
#############################################
echo 'get_obs_run_sdm_per_month loop start'
echo $(date '+%y/%m/%d %H:%M:%S')
# for loop for each taxon id
for taxon_id in $taxon_ids
do

	# get the file and folder list in a designated filder
	# get the years having the observations of each taxon id: if the folers named the year exist, we can say there is at least one csv file inside.  
	yearList=$(ls -1 ./data/inaturalist/$taxon_id)
	# echo 'year is '$yearList

	# loop by year
	for year in $yearList
	do
		# if $year gets the csv file having all observation data of the taxon id, make its own folder and run SDM for the taxon id
		case $year in
			*\.csv)
				echo "Found .csv suffix. file name is " $year ". taxon id is " $taxon_id
				# get rid of the extension from the file name = taxon id
				taxonIdNoExtension=$(basename $year | sed 's/\.[^\.]*$//')

				# make the output folder if does not exist
				mkdir -p ../data/sdm_results/$taxon_id/$taxonIdNoExtension/

				# run SDM with the csv file
				echo "run-sdm.R start:" $(date '+%y/%m/%d %H:%M:%S')
				Rscript --vanilla run_sdm.R ./data/inaturalist/$taxon_id/$taxonIdNoExtension.csv $taxon_id ../data/sdm_results/$taxon_id/$taxonIdNoExtension/
				echo "run-sdm.R end:" $(date '+%y/%m/%d %H:%M:%S')
				;;

			# else (if $year is a foler whose name is yest, go inside the folder) 
			*)
				# get the file and folder name list in a designated filder	
				# get the months having the observations of each taxon id: if the folers named the month exist, we can say there is at least one csv file inside.
				monthList=$(ls -1 ./data/inaturalist/$taxon_id/$year)

				# loop by month
				for month in $monthList
				do

					# if $month gets the csv file having all observation data in the year, make its own folder and run SDM for one year result
					case $month in
						*\.csv)
							echo "Found .csv suffix. file name is " $month ". year is " $year ". taxon id is " $taxon_id
							# get taxon id and year from its file name
							taxon_id_per_year=$(basename $month | cut -d '-' -f 1)
							yearNoExtension=$(basename $month | cut -d '-' -f 2 | sed 's/\.[^\.]*$//')

							# make the output folder if does not exist
							mkdir -p ../data/sdm_results/$taxon_id/$yearNoExtension/$yearNoExtension

							# run SDM with the csv file
							echo "run-sdm.R start:" $(date '+%y/%m/%d %H:%M:%S')
							Rscript --vanilla run_sdm.R ./data/inaturalist/$taxon_id/$yearNoExtension/$taxon_id_per_year-$yearNoExtension.csv $taxon_id ../data/sdm_results/$taxon_id/$yearNoExtension/$yearNoExtension
							echo "run-sdm.R end:" $(date '+%y/%m/%d %H:%M:%S')
							;;
						# else (if $taxon_id is a foler whose name is taxon id) 
						*)
							# get the month from each file name d = delimiter (`-`)
							# month=$(basename $filename | cut -d '-' -f 3)

							echo '(normal case) run-sdm.R loop. taxon id is ' $taxon_id ' and year is ' $year ' and month is ' $month

							# make the output folder if does not exist
							mkdir -p ../data/sdm_results/$taxon_id/$year/$month

							# run SDM file
							# Rscript --vanilla run-sdm.R <path/to/data/file> <output-file-prefix> <path/to/output/directory/>
							# old command
							# Rscript --vanilla run_sdm.R ./data/inaturalist/$taxon_id-iNaturalist.csv $taxon_id ../output/$taxon_id
							echo "run-sdm.R start:" $(date '+%y/%m/%d %H:%M:%S')
							Rscript --vanilla run_sdm.R ./data/inaturalist/$taxon_id/$year/$month/$taxon_id-$year-$month.csv $taxon_id ../data/sdm_results/$taxon_id/$year/$month
							echo "run-sdm.R end:" $(date '+%y/%m/%d %H:%M:%S')
							;;
					esac
				done
			;;
		esac
	done

done

#############################################
# run run_sdm.R end 
#############################################

echo 'get_obs_run_sdm_per_month loop end' $(date '+%y/%m/%d %H:%M:%S')

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
