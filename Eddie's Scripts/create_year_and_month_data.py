import pandas as pd
import numpy as np
import datetime

speciesId = pd.read_csv("./species.csv").ix[:,"taxonID"]
headers = ["TaxonId", "ScientificName", "TotalObservations", "Year", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

def readCsv(pathToCsv):
    file = pd.read_csv(pathToCsv, encoding = "ISO-8859-1")

    # get date observed, taxonid, species name (might need to look up)
    filteredData = file.ix[:, ["taxon_id", "scientific_name", "datetime"]]
    # split into 2d dataframe that will be taxonId, speciesName, numObserved, month
    df = groupSpeciesAndCreateFrame(filteredData)
    # transform into csv
    df.to_csv("./observation_counts.csv", index=False)

def groupSpeciesAndCreateFrame(df):
    toReturn = pd.DataFrame(columns=headers)
    listToPutIntoDf = []
    months = pd.DataFrame(columns=headers[3:])

    for id in speciesId:
        groupedSpecies = df.ix[df["taxon_id"] == id]  
        groupedSpecies.ix[:, "datetime"] = groupedSpecies.ix[:, "datetime"].apply(pd.to_datetime)

        yearMonths = {}

        for obs in groupedSpecies.ix[:, "datetime"]:
            month = returnMonthAsString(obs.month - 1)
            year = obs.year
            if not year in yearMonths:
                yearMonths[year] = createEmptyMonthsDictionary()
            yearMonths[year][month] += 1
        
        flattenedDictionary = flattenDictionary(yearMonths)
        for row in flattenedDictionary:
            totalObs = sum(row[1:]) 
            listToPutIntoDf.append([id, groupedSpecies["scientific_name"].values[0], totalObs, *row])
    
    toReturn = pd.DataFrame(listToPutIntoDf, columns=headers)
    
    return toReturn

def createEmptyMonthsDictionary():
    return {
            "January": 0,
            "February": 0,
            "March": 0, 
            "April": 0, 
            "May": 0,
            "June": 0,
            "July": 0,
            "August": 0,
            "September": 0,
            "October": 0,
            "November": 0,
            "December": 0
        }

def returnMonthAsString(month):
    return [
        "January",
        "February",
        "March", 
        "April", 
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ][month]

def flattenDictionary(dictVar):
    returnList = []
    for key, value in dictVar.items():
        flattenedMonths = []
        flattenedMonths.append(key)
        for key2, value2 in value.items():
            flattenedMonths.append(value2)
        returnList.append(flattenedMonths)
    
    return returnList
            

def main():
    #readCsv("./ALLTHEFUCKING-FullData.csv")
    readCsv("./kensaku_master.csv")

if __name__ == "__main__":
    main()