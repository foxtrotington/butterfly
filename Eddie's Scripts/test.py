import pandas as pd
import numpy as np
import csv
import json
import requests

butterflyTaxonIds = pd.read_csv("./species.csv")

def getButterflyDataFrom(pathToCsv):
    observations = pd.read_csv(pathToCsv)

    taxonIdsInSpeciesAsList = butterflyTaxonIds.iloc[:, 0].tolist()

    butterflyData = observations[observations["taxonID"].isin(taxonIdsInSpeciesAsList)]
    butterflyData.to_csv("./inat_butterfly_observations.csv")

def getAccessToken():
    site = "https://www.inaturalist.org"
    app_id = '69345738565c2bd88f2dafa49857e426ad01918d5e5a72fcdde40d258f22b49c'
    app_secret = '62899ac1d355f1743b84db1e21e94f2bc40de4915cb7a2cb2afaeab41dfb0de8'
    username = 'ornelaseduardo'
    password = 'qb7A1PAl4eRp6rPh'
    ids = str(butterflyTaxonIds.iloc[:, 0].tolist()).replace("[", "").replace("]", "").replace(" ", "")

    # Send a POST request to /oauth/token with the username and password
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

    obs_data = requests.get(("http://api.inaturalist.org/v1/observations?taxon_id=" + ids +"&quality_grade=research&page=3"), headers=headers)
    
    with open('observations_from_inat_api.txt', 'w') as outfile:
        json.dump(json.loads(obs_data.text), outfile)

def main():
    getButterflyDataFrom("./observations.csv")
    #getAccessToken()


if __name__ == "__main__":
    main()
