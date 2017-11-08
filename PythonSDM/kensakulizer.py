import csv
import subprocess as sp
import sys
import os


def listOfIdsNames():
    file = open("taxon-Ids.txt").readlines()
    dictionary = {}
    count = 0
    for data in file:
        data = data.strip().split()
        if(count != 0):
            dictionary[data[0]] = data[1]+" "+data[2]
        else:       
            count = 1;
    return dictionary




def cleaner(species):

	data = {}
	counter=1
	species = [52773]
	for id in species:
		print(str(counter/len(species)*100)+str('%'))
		counter+=1
		#print(id)
		if id != '216349':

			innie = str(id)+"-iNaturalist.csv"

		if id not in data:
			data[id] = {}




			with open(innie,newline='',encoding='utf-8') as f:
				reader = csv.reader(f)
			
			
				for row in reader:
				
					if len(row) >6 and row[19] != 'observed_on':
						dates = row[19].split("-")
						
						if dates[0] not in data[id]:
							data[id][dates[0]]={}
							
						if dates[1] not in data[id][dates[0]]:
							data[id][dates[0]][dates[1]]=[]
						observationData=[]
						observationData.append(id)
						observationData.append(row[4])
						observationData.append(row[5])
						data[id][dates[0]][dates[1]].append(observationData)
				

			masterWrite = []
			for ids in data:

				for years in data[ids]:
					

					for months in data[ids][years]:

						outtie = open(str(id)+"-"+str(years)+"-"+str(months)+".csv",'w',newline='',encoding='utf-8')
						headers = ["taxonID", "latitude", "longitude"]
						writer = csv.writer(outtie)
						writer.writerow(headers)

						for geo in data[ids][years][months]:

							writer.writerow(geo)



	f.close()
	outtie.close()



def main():
    print("Running")
    butterflys = listOfIdsNames()
    cleaner(butterflys)
    print("Complete")

main()
