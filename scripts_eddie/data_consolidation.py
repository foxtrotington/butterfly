import csv
import numpy as np
import pandas as pd

species = pd.read_csv("../data/in/species.csv", encoding = "ISO-8859-1")
gbif_obs = pd.read_csv("../data/in/gbif_observations.csv", encoding = "ISO-8859-1")
sdm_obs = pd.read_csv("../data/in/kensaku_master.csv", encoding = "ISO-8859-1")
inat_obs = pd.read_csv("../data/in/inat_butterfly_observations.csv", encoding = "ISO-8859-1")

def startup():
    gbif_dict = dictionarify(gbif_obs, "GBIF")
    sdm_dict = dictionarify(sdm_obs, "iNaturalist")
    inat_obs_dict = dictionarify(inat_obs, "iNaturalist")

    z = {**sdm_dict, **gbif_dict}
    z = {**inat_obs_dict, **z}
    flatDictionary = flattenDictionary(z)
    listToPutIntoDf = [["Id", "ScientificName", "Source", "SourceId", "Lat", "Lng", "Year", "Month"]]
    for row in flatDictionary:
            listToPutIntoDf.append([*row])
    df = pd.DataFrame(listToPutIntoDf)
    df.to_csv("../data/out/master_csv.csv", index=False)
    
def dictionarify(dataframe, sourceStr):
    returnDictionary = {}

    if sourceStr == "GBIF":
        for index, row in dataframe.iterrows():
            if not row["gbifid"] in returnDictionary:
                inat_obs_id = row["catalognumber"]
                source = sourceStr
                sourceId = row["gbifid"]
                lat = row["decimallatitude"]
                lng = row["decimallongitude"]
                year = row["year"]
                month = row["month"]
                scientificName = row["species"]

                returnDictionary[inat_obs_id] = {
                    "scientificName": scientificName,
                    "source": source,
                    "sourceId": sourceId,
                    "lat": lat,
                    "lng": lng,
                    "year": year,
                    "month": month,
                }
    
    elif sourceStr == "iNaturalist":
        for index, row in dataframe.iterrows():
            if "datetime" in row:
                inat_obs_id = row["id"]
                source = sourceStr
                sourceId = inat_obs_id
                lat = row["latitude"]
                lng = row["longitude"]
                datetime = pd.to_datetime(row["datetime"])
                year = datetime.year
                month = datetime.month
                scientificName = row["scientific_name"]
                
                returnDictionary[inat_obs_id] = {
                    "scientificName": scientificName,
                    "source": source,
                    "sourceId": sourceId,
                    "lat": lat,
                    "lng": lng,
                    "year": year,
                    "month": month,
                }

            else:
                inat_obs_id = row["id"]
                source = sourceStr
                sourceId = inat_obs_id
                lat = row["decimalLatitude"]
                lng = row["decimalLongitude"]
                datetime = pd.to_datetime(row["eventDate"])
                year = datetime.year
                month = datetime.month
                scientificName = row["scientificName"]
                
                returnDictionary[inat_obs_id] = {
                    "scientificName": scientificName,
                    "source": source,
                    "sourceId": sourceId,
                    "lat": lat,
                    "lng": lng,
                    "year": year,
                    "month": month,
                }
            
    return returnDictionary
    
def flattenDictionary(dictVar, level = 2):
    '''
    A utility function that will flatten a dictionary of dictionaries
    in: 
        dictVar: expects a dictionary object
        level: expects an integer value that describes how many nested dictionaries
              there are
    out: 
        returnList: a 1d list of the items in the nested dictionary
    '''

    returnList = []
    for key, value in dictVar.items():
        flattenedMonths = []
        flattenedMonths.append(key)
        for key2, value2 in value.items():
            flattenedMonths.append(value2)
        returnList.append(flattenedMonths)
    
    return returnList
    
def main():
    startup()

if __name__ == "__main__":
    main()