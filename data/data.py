import csv
import json


dict_from_csv = {}

with open('src/population_total.csv', mode='r', encoding="utf8") as inp:
    reader = csv.reader(inp)
    for row in reader:
        print(row)
    #dict_from_csv = {rows[0]:rows[7] for rows in reader}

#print(dict_from_csv)



'''
with open('GLOB.SES.csv', 'r') as file_csv:
    fieldnames = ("field1","field2")
    reader = csv.DictReader(file_csv, fieldnames)
    
with open('myfile.json', 'w') as file_json:
    for row in reader:
            json.dump(row, file_json)    
'''