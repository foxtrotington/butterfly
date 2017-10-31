import requests
import json
import csv
import subprocess as sp
import sys


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


def getAccessToken(species):
    print("Running...")
    site = "https://www.inaturalist.org"
    app_id = '69345738565c2bd88f2dafa49857e426ad01918d5e5a72fcdde40d258f22b49c'
    app_secret = '62899ac1d355f1743b84db1e21e94f2bc40de4915cb7a2cb2afaeab41dfb0de8'
    username = 'ornelaseduardo'
    password = 'qb7A1PAl4eRp6rPh'

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
    run = 1
    for butterfly in species:
        
        percent = round((run/len(species))*100,1)
        #sp.call('cls',shell=True)
        print(str(percent)+"%")
        #print(str(butterfly))

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
            record = 1
            for records in data['results']:

                holder = []

                holder.append(records["id"])
                holder.append(str(butterfly))
                holder.append(str(species[butterfly]))
                
                if(records["location"] is not None):
                    latlong = records["location"].split(",")

                    holder.append(latlong[0])
                    holder.append(latlong[1])
                holder.append(records["observed_on"])
                holder.append(records["time_observed_at"])
                tempList.append(holder)

            run2+=1

            sp.call('cls',shell=True)
        run+=1

        with open(str(butterfly)+".csv", "w",encoding='utf-8') as file:
            writer = csv.writer(file)

            writer.writerows(tempList)
        tempList = []

def main():
    print("Running")
    butterflys = listOfIdsNames()
    dick = {"52773":"Poanes zabulon"}
    getAccessToken(butterflys)
    print("Complete")

main()