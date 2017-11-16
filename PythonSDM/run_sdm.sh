chmod u+x ../data/gbif/taxon-ids.txt

# get the list of taxon ids removing a header
# taxon_ids= cat ../data/gbif/taxon-ids.txt | cut -f 1 | tail -n +2 $taxon_ids
# taxon_ids=$(cat ./taxon-ids.txt | cut -f 1 | tail -n +2 $taxon_ids)
taxon_ids=$(cat ./taxon-ids-short.txt | cut -f 1 | tail -n +2 $taxon_ids)
echo '$taxon_ids'
echo $taxon_ids

# initialize the counter
count=0

# declare and initialize the variables
year=""
month=""

# insert the data
# TODO the year and month data should be passed by Data-Puller.py
$year=2011
$month=10

echo 'calling run-sdm.R loop start'
echo $(date '+%y/%m/%d %H:%M:%S')
for taxon_id in $taxon_ids
do
	echo "taxon id: $taxon_id"

	# if the year and month variables have data
	# source https://open-groove.net/shell/if-and-or/
	if [ ! -z "$year"] && [ !-z "$month" ]; then
		echo 'month and year were specified.'
		# make a directory to store the output for each taxon id
		mkdir ../output/$taxon_id/$year/%month
		# get the csv files, each of which has the observation data for the specific month of an year 
		Rscript --vanilla run_sdm.R ./data/inaturalist/$taxon_id-iNaturalist.csv $taxon_id ../output/$taxon_id

	# if the year variable has data
	elif [ ! -z "$year" ]; then
		# TODO: same as the last one  
		# make a directory to store the output for each taxon id
		mkdir ../output/$taxon_id/$year
		# get the csv files, each of which has the observation data for the specific year 
		Rscript --vanilla run_sdm.R ./data/inaturalist/$taxon_id-iNaturalist.csv $taxon_id ../output/$taxon_id

	else
		# TODO: when no period is specified, need to take all csv files of the observation
		# make a directory to store the output for each taxon id
		mkdir ../output/$taxon_id
		# Rscript --vanilla run-sdm.R <path/to/data/file> <output-file-prefix> <path/to/output/directory/>
		# get the csv files, each of which has all observation data for the whole season.
		Rscript --vanilla run_sdm.R ./data/inaturalist/$taxon_id-iNaturalist.csv $taxon_id ../output/$taxon_id



	count=$(( count + 1 ))
	echo  "for loop count finished: $count"
	echo $(date '+%y/%m/%d %H:%M:%S')
done

echo 'calling run-sdm.R loop  end'


