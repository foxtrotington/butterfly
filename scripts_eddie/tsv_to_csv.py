import csv

# read tab-delimited file
with open('0000250-171113114016250.csv','r') as fin:
    cr = csv.reader(fin, delimiter='\t')
    filecontents = [line for line in cr]
# write comma-delimited file (comma is the default delimiter)
with open('gbif_observations.csv','w') as fou:
    cw = csv.writer(fou, quotechar='', quoting=csv.QUOTE_NONE, escapechar='\\')
    cw.writerows(filecontents)