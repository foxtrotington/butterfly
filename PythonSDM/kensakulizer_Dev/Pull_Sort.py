import requests
import json
import csv
import subprocess as sp
import os



def listOfIdsNames(filename):
    file = open(filename).readlines()
    dictionary = {}
    count = 0
    for data in file:
        data = data.strip().split()
        if(count != 0):
            dictionary[data[0]] = data[1]+" "+data[2]
        else:       
            count = 1;
    return dictionary


def getAccessToken(app_id,app_secret,username,password):
    
    site = "https://www.inaturalist.org"
    app_id = app_id
    app_secret = app_secret
    username = username
    password = password

    payload = {
        'client_id': app_id,
        'client_secret': app_secret,
        'grant_type': "password",
        'username': username,
        'password': password
    }

    response = requests.post(("%s/oauth/token" % site), payload)
    token = response.json()["access_token"]
    headers = {"Authorization": "Bearer %s" % token}

    return headers


def dataPuller(species,headers):
    print("Running...")

    run = 1
    for butterfly in species:
        
        percent = round((run/len(species))*100,1)
        
        print(str(percent)+"%")
       

        obs_data = requests.get(("http://api.inaturalist.org/v1/observations?taxon_id=" + str(butterfly) +"&quality_grade=research&page=1"), headers=headers)
        jData = json.loads(obs_data.text)
        total_Observations = int(jData["total_results"])
        pages=0
        if( total_Observations % 30 != 0):
            pages = (total_Observations//30)+1
        else:
            pages = total_Observations//30

        run2 = 1
        tempList = []
        for i in range(1,pages):
            
            percent2 = round((run2/pages)*100,1)
            print(str(percent)+"%")
            print("... "+str(run2)+" of "+str(pages)+" pages")

            obs_data = requests.get(("http://api.inaturalist.org/v1/observations?taxon_id=" + str(butterfly) +"&quality_grade=research&page="+str(i)), headers=headers) #TODO ids

            data = json.loads(obs_data.text)
            
            for records in data['results']:

                holder = []

                #holder.append(records["id"])
                holder.append(str(butterfly))
                #holder.append(str(species[butterfly]))
                
                if(records["location"] is not None):
                    latlong = records["location"].split(",")

                    holder.append(latlong[0])
                    holder.append(latlong[1])
                else:
                    holder.append("")
                    holder.append("")
                holder.append(records["observed_on"])
                #holder.append(records["time_observed_at"])
                tempList.append(holder)

            run2+=1

            sp.call('cls',shell=True)
        run+=1
        print('Pulling Complete')
#---------DATA STRUCT----------DATA STRUCT---------------------
        data[butterfly] = {}
        print("/t Creating data structure")
        total = len(tempList)
        upper = 1
        for date_info in tempList:
            print(upper/total)
            upper +=1
            print(date_info)

            dates = date_info[3].split("-")

            if dates[0] not in data[butterfly]:
                data[butterfly][dates[0]] = {}
            if dates[1] not in data[butterfly][dates[0]]:
                data[butterfly][dates[0]][dates[1]]=[]

            observationData = []
            observationData.append(butterfly)
            observationData.append(date_info[1])
            observationData.append(date_info[2])
            data[butterfly][dates[0]][dates[1]].append(observationData)
            sp.call('cls',shell=True)
        print("Complete")

        masterWrite = []

        directory = 'data/inaturalist/'+str(butterfly)

        if not os.path.exists(directory):
            os.makedirs(directory)

        print("/t Placing data into data structure")
        total = len(data[butterfly])
        upper = 1
        for years in data[butterfly]:
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
                    writer.writerow(geo)
                outtie.close()
                sp.call('cls',shell=True)

            outtie = open('data/inaturalist/'+str(butterfly)+"/" + str(years)+'/'+str(butterfly)+"-"+str(years)+".csv",'w',newline='',encoding='utf-8')
            headers = ["taxonID", "latitude", "longitude"]
            writer = csv.writer(outtie)
            writer.writerow(headers)
            print("Final write outs")
            for all_data in masterWrite:
                writer.writerow(all_data)
            outtie.close()
            masterWrite = []

#---------DATA STRUCT----------DATA STRUCT---------------------
        with open('data/inaturalist/'+str(butterfly)+'/'+str(butterfly)+".csv", "w",encoding='utf-8') as file:
            writer = csv.writer(file)

            writer.writerows(tempList)
        tempList = []

       


def main():

    app_id = '69345738565c2bd88f2dafa49857e426ad01918d5e5a72fcdde40d258f22b49c'
    app_secret = '62899ac1d355f1743b84db1e21e94f2bc40de4915cb7a2cb2afaeab41dfb0de8'
    username = 'ornelaseduardo'
    password = 'qb7A1PAl4eRp6rPh'
    file = "taxon-Ids.txt"
    print("Running")
    # butterflys = listOfIdsNames(file)
    butterflys = {48578:'Anteos maerula'}
    key = getAccessToken(app_id,app_secret,username,password)
    dataPuller(butterflys,key)
    print("Complete")

main()