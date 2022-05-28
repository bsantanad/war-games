import csv
import json
import re

#from importlib_metadata import distribution
tens = dict(k=10e3, m=10e6, b=10e9)
regions_data = dict()
class Region:
    def __init__(self, name):
        self.name = name
        self.territory = Variable('territory')
        self.population = Variable('population')
        self.growth_rate = Variable('growth_rate')
        self.income = Variable('income')
        self.literacy_rate = Variable('literacy_rate')
        self.military_spdng = Variable('military_spdng')
class Variable:
    def __init__(self, name):
        self.name = name
        self.data = []
        self.distribution = ''
        self.mean = 0
        self.stdv = 0

def conversion(x):
    factor, exp = x[0:-1], x[-1].lower()
    ans = int(float(factor) * tens[exp])
    return ans

regions = dict()

regions['europe'] = Region('Europe')
regions['africa'] = Region('Africa')
regions['asia'] = Region('Asia')
regions['n_america'] = Region('N America')
regions['s_america'] = Region('S America')
regions['oceania'] = Region('Oceania')
regions['seme_asia'] = Region('S E Asia M E')




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
        

with open('src/population_total.csv', mode='r', encoding="utf8") as pop:
    reader = csv.reader(pop)
    next(reader, None)
    for row in reader:
        #print(row)
        country = row[0]
        for continent, countries in regions_data.items():
            if country in countries:
                if continent == 'europe':
                    new_row = row[1:]
                    converted = [conversion(x) for x in new_row]
                    
                    if not regions[continent].population.data:
                        regions[continent].population.data = converted
                    else: 
                    
                        for index, elem in enumerate(regions[continent].population.data):
                            regions[continent].population.data[index] += converted[index]
                    print(f"agrega {new_row[20]} : {regions[continent].population.data[20]}")



'''print(regions_data)
print(len(regions_data))'''

#seme_asia.population.data = 


'''
with open('GLOB.SES.csv', 'r') as file_csv:
    fieldnames = ("field1","field2")
    reader = csv.DictReader(file_csv, fieldnames)
    
with open('myfile.json', 'w') as file_json:
    for row in reader:
            json.dump(row, file_json)    
'''