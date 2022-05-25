import csv
import json
import re

regions_data = dict()

with open('src/world_region.csv', mode='r', encoding="utf8") as inp:
    reader = csv.reader(inp)
    next(reader, None)
    for row in reader:
        country = row[1]
        region = row[2]
        if not region in regions_data:
            regions_data[region] = set()
        else:
            regions_data[region].add(country)
        

print(regions_data)
print(len(regions_data))


'''
with open('GLOB.SES.csv', 'r') as file_csv:
    fieldnames = ("field1","field2")
    reader = csv.DictReader(file_csv, fieldnames)
    
with open('myfile.json', 'w') as file_json:
    for row in reader:
            json.dump(row, file_json)    
'''