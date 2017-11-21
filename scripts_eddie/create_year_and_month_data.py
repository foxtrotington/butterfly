import pandas as pd
import numpy as np
import datetime

speciesId = pd.read_csv("../data/species.csv")#.ix[:,"taxonID"]
headers = ["TaxonId", "ScientificName", "TotalObservations", "Year", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

def readCsv(pathToCsv):
    file = pd.read_csv(pathToCsv, encoding = "ISO-8859-1")

    # get date observed, taxonid, species name (might need to look up)
    filteredData = file.ix[:, ["Id", "ScientificName", "Year", "Month"]]

    # join data on ScientificName and Group By SciName, Year, Month and use size() to count observations in those groups
    df = pd.merge(filteredData, speciesId, left_on="ScientificName", right_on="scientificName").groupby(['ScientificName', 'Year', 'Month'], as_index=False).size()
    
    # reset to get the headers back
    df = df.reset_index()

    # change the name to add observation count
    df.columns = ["ScientificName", "Year", "Month", "ObservationCount"]

    # export to csv and index false to get rid of the index column
    df.to_csv("../data/observation_counts.csv", index=False)

''' 

Below is commented out because it's not needed to get readCsv to work anymore. Keeping it just in case though.

'''

# def groupSpeciesAndCreateFrame(df):
#     toReturn = pd.DataFrame(columns=headers)
#     listToPutIntoDf = []
#     months = pd.DataFrame(columns=headers[3:])
#     print(pd.merge(df, speciesId, left_on="ScientificName", right_on="scientificName").groupby(['ScientificName', 'Year', 'Month']).size())
#     #print(df.join(speciesId.set_index(['taxonID']), on=["Id"]).groupby(['Id', 'Year']))#.groupby(['Id', 'Year', 'Month']).size())
#     for id in speciesId:
#         groupedSpecies = df.ix[df["Id"] == id] 
#         # groupedSpecies.ix[:, "datetime"] = groupedSpecies.ix[:, "datetime"].apply(pd.to_datetime)

#         yearMonths = {}

#         for index, row in groupedSpecies.iterrows():
#             month = returnMonthAsString(row["Month"])
#             year = row["Year"]
#             if not year in yearMonths:
#                 yearMonths[year] = createEmptyMonthsDictionary()
#             yearMonths[year][month] += 1
        
#         flattenedDictionary = flattenDictionary(yearMonths)
#         for row in flattenedDictionary:
#             totalObs = sum(row[1:]) 
#             listToPutIntoDf.append([id, groupedSpecies["ScientificName"].values[0], totalObs, *row])
    
#     toReturn = pd.DataFrame(listToPutIntoDf, columns=headers)

#     return toReturn

# def createEmptyMonthsDictionary():
#     return {
#             "January": 0,
#             "February": 0,
#             "March": 0, 
#             "April": 0, 
#             "May": 0,
#             "June": 0,
#             "July": 0,
#             "August": 0,
#             "September": 0,
#             "October": 0,
#             "November": 0,
#             "December": 0
#         }

# def returnMonthAsString(month):
#     return [
#         "January",
#         "February",
#         "March", 
#         "April", 
#         "May",
#         "June",
#         "July",
#         "August",
#         "September",
#         "October",
#         "November",
#         "December"
#     ][month]

# def flattenDictionary(dictVar):
#     returnList = []
#     for key, value in dictVar.items():
#         flattenedMonths = []
#         flattenedMonths.append(key)
#         for key2, value2 in value.items():
#             flattenedMonths.append(value2)
#         returnList.append(flattenedMonths)
    
#     return returnList
            

def main():
    readCsv("../data/master_csv.csv")

if __name__ == "__main__":
    main()