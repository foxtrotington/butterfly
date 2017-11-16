# give this script the read and write right to this file 
chmod u+x ../data/gbif/taxon-ids.txt

# get the list of taxon ids removing a header
# taxon_ids= cat ../data/gbif/taxon-ids.txt | cut -f 1 | tail -n +2 $taxon_ids
taxon_ids=$(cat ../data/gbif/taxon-ids.txt | cut -f 1 | tail -n +2 $taxon_ids)
echo $taxon_ids

count=0
echo 'calling get-observation-data.R loop start'
echo $(date '+%y/%m/%d %H:%M:%S')
for taxon_id in $taxon_ids
do
	echo "taxon id: $taxon_id"
	Rscript --vanilla get-observation-data.R $taxon_id
	count=$(( count + 1 ))
	echo  "for loop count finished: $count"
	echo $(date '+%y/%m/%d %H:%M:%S')

done
echo 'calling get-observation-data.R loop end'

# initialize the counter
count=0

echo 'calling run-sdm.R loop start'
echo $(date '+%y/%m/%d %H:%M:%S')
for taxon_id in $taxon_ids
do
	echo "taxon id: $taxon_id"
	# Rscript --vanilla run-sdm.R <path/to/data/file> <output-file-prefix> <path/to/output/directory/>
	Rscript --vanilla run_sdm.R ./data/inaturalist/$taxon_id-iNaturalist.csv $taxon_id ../output/
	count=$(( count + 1 ))
	echo  "for loop count finished: $count"
	echo $(date '+%y/%m/%d %H:%M:%S')
done

echo 'calling run-sdm.R loop  end'
