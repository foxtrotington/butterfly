import sqlite3
import pandas as pd
import csv

cnn = sqlite3.connect("../test/test.db")
c = cnn.cursor()
test = [None] * 37
test[0] = 20

with open("./inat_butterfly_observations.csv", encoding = "ISO-8859-1") as file: 
    reader = csv.reader(file)
    dataAsList = list(reader)
    del dataAsList[0]
    print(len(dataAsList[0]))
    c.execute("insert into test values (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", test)

