import requests #required for http requests
import json #used to translate returned data
import csv #used to write out csvs
import subprocess as sp #used for clearning console during runs
import os #used for directory creation


#listOfIdsNames takes a textfile name and uses it to create a dictionary
#this dictionary is returned to be used by data puller
def listOfIdsNames(filename):
    file = open(filename).readlines()
    dictionary = {}
    count = 0
    for data in file:
        data = data.strip().split()
        if(count != 0):
            dictionary[data[0]] = data[1]+" "+data[2] #key is taxon ID and value is scientific name
        else:       
            count = 1;
    return dictionary

#getAccessToken is required for uncapped requests of data from inaturalist
def getAccessToken(app_id,app_secret,username,password):
    
    site = "https://www.inaturalist.org"
    app_id = app_id #granted by inaturalist after logging in
    app_secret = app_secret #granted by inaturalist after logging in
    username = username #your username
    password = password #your password

    #payload is all required data changed into a dictionary to allow access with requests
    payload = {
        'client_id': app_id,
        'client_secret': app_secret,
        'grant_type': "password",
        'username': username,
        'password': password
    }

    response = requests.post(("%s/oauth/token" % site), payload) #the 24 hour token is generated 
    token = response.json()["access_token"] #access token is stored
    headers = {"Authorization": "Bearer %s" % token} #token is used for headers to finally allow access

    return headers


def dataPuller(species,headers1):
    print("Running...")

    run = 1
    for butterfly in species: #iterate through the dictionary pulling the taxon id observations
        
        percent = round((run/len(species))*100,1) #used to track progress of total pull
        
        print(str(percent)+"%")
       
        #used to get the requested data, obs_data allows us to determine how many pages there are so we can iterate through them all
        obs_data = requests.get(("http://api.inaturalist.org/v1/observations?taxon_id=" + str(butterfly) +"&quality_grade=research&page=1"), headers=headers1)
        jData = json.loads(obs_data.text)
        total_Observations = int(jData["total_results"])
        pages=0
        if( total_Observations % 30 != 0): #needed if there is exactly 30 per page or if there is an odd count say 31 therefore 2 pages
            pages = (total_Observations//30)+1
        else:
            pages = total_Observations//30

        run2 = 1
        tempList = [] #tempList will store all requested data for one species before it is reset for the next
        for i in range(1,pages): #pulls each page up one at a time 
            
            percent2 = round((run2/pages)*100,1)
            print(str(percent)+"%")
            print("... "+str(run2)+" of "+str(pages)+" pages")

            obs_data = requests.get(("http://api.inaturalist.org/v1/observations?taxon_id=" + str(butterfly) +"&quality_grade=research&page="+str(i)), headers=headers1) #TODO ids

            data = json.loads(obs_data.text)
            #works through each record per page
            for records in data['results']:

                holder = []# stores taxonID, lat,long, and date of observation per entry before being cleared

                
                holder.append(str(butterfly))
                
                
                if(records["location"] is not None):
                    latlong = records["location"].split(",")

                    holder.append(latlong[0])
                    holder.append(latlong[1])
                else:
                    holder.append("")
                    holder.append("")
                holder.append(records["observed_on"])
                
                tempList.append(holder) #temp list takes holders data as a list of lists

            run2+=1

            sp.call('cls',shell=True)
        run+=1
        print('Pulling Complete')
#With the pull complete for a species it is then written out to total, yearly, and month observation csv files
#---------DATA STRUCT----------DATA STRUCT---------------------
        data[butterfly] = {} #this will be a double nested dictionary containg year info, and month info.
        print(" Creating data structure")
        total = len(tempList)
        upper = 1
        for date_info in tempList: #a for loop to prep the tempList into organized data by year and month
            print(upper/total)
            upper +=1
            print(date_info)

            dates = date_info[3].split("-") #dates are in a yyyy-mm-dd format and thus are split to better sort the data

            if dates[0] not in data[butterfly]: #if the year isn't present, create a key with the year value and an empty dictionary for months
                data[butterfly][dates[0]] = {}
            if dates[1] not in data[butterfly][dates[0]]: #if the month in that year with data isn't present, create a key of that month with a list value
                data[butterfly][dates[0]][dates[1]]=[]

            observationData = [] #list to store observation recoreds of taxonid lat and long data
            observationData.append(butterfly)
            observationData.append(date_info[1])
            observationData.append(date_info[2])
            data[butterfly][dates[0]][dates[1]].append(observationData)
        sp.call('cls',shell=True)#clear the console
        print("Complete")

        masterWrite = [] #a list is required to write out a csv, will hold all needed data

        directory = 'data/inaturalist/'+str(butterfly)

        if not os.path.exists(directory):#checks for taxon id, year and month folders, creates them as needed
            os.makedirs(directory)

        print("Placing data into data structure")
        total = len(data[butterfly])
        upper = 1
        for years in data[butterfly]: #for every year store the data of the butter fly by each month
            print(upper/total)
            upper+=1
            directory = 'data/inaturalist/'+str(butterfly)
            directory+='/'+str(years)

            if not os.path.exists(directory):
                os.makedirs(directory)

            for months in data[butterfly][years]:

                directory = 'data/inaturalist/'+str(butterfly)+'/'+str(years)
                directory += "/"+str(months)

                if not os.path.exists(directory):
                    os.makedirs(directory)

                outtie = open('data/inaturalist/'+str(butterfly)+'/'+str(years)+'/'+str(months)+'/'+str(butterfly)+"-"+str(years)+"-"+str(months)+".csv",'w',newline='',encoding='utf-8')
                headers = ["taxonID", "latitude", "longitude"]
                writer = csv.writer(outtie)
                writer.writerow(headers)

                for geo in data[butterfly][years][months]:
                    masterWrite.append(geo)
                    writer.writerow(geo) #writes the csv for specified year and month
                outtie.close()
            sp.call('cls',shell=True)

            outtie = open('data/inaturalist/'+str(butterfly)+"/" + str(years)+'/'+str(butterfly)+"-"+str(years)+".csv",'w',newline='',encoding='utf-8')
            headers = ["taxonID", "latitude", "longitude"]
            writer = csv.writer(outtie)
            writer.writerow(headers)
            print("Final write outs")
            for all_data in masterWrite:
                writer.writerow(all_data) #writes data for entire year
            outtie.close()
            masterWrite = [] #resets masterWrite for next year

#---------DATA STRUCT----------DATA STRUCT---------------------
        with open('data/inaturalist/'+str(butterfly)+'/'+str(butterfly)+".csv", "w",encoding='utf-8') as file:
            writer = csv.writer(file)
            headers = ["taxonID", "latitude", "longitude","date"]
            writer.writerow(headers)
            writer.writerows(tempList) #writes a master file for the species of all data
        tempList = [] #resets templist for next species

       


def main():

    app_id = '69345738565c2bd88f2dafa49857e426ad01918d5e5a72fcdde40d258f22b49c'
    app_secret = '62899ac1d355f1743b84db1e21e94f2bc40de4915cb7a2cb2afaeab41dfb0de8'
    username = 'ornelaseduardo'
    password = 'qb7A1PAl4eRp6rPh'
    file = "taxon-Ids.txt"
    print("Running")
    file = "taxon-ids.txt"
    butterflys = listOfIdsNames(file)
    key = getAccessToken(app_id,app_secret,username,password)
    dataPuller(butterflys,key)
    print("Complete")

main()
