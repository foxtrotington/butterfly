# get the list of folde names without "./"
folders=$(find -type d | sed "s|^\./||")
# echo $folders

for folder in $folders
do
	# echo $folder
	# zip each directory (folder)
	zip -r $folder.tar.gz $folder
done
