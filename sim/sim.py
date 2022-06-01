import json
import os

import numpy as np
import simpy

import lib

RANDOM_SEED = 42
INCOME_THRESHOLD = 0 # FIXME this should be diff than 0
POP_THRESHOLD = 0 # FIXME this should be diff than 0
MAP_SIZE = 10 # grid size nxn

grid = np.zeros([MAP_SIZE, MAP_SIZE], dtype = int)

DATA_PATH = os.getenv('DATA_PATH', '../data/data.json')

countries = {
    'africa': {},
    'europe': {},
    'middle_east': {},
    'asia': {},
    'oceania_se_asia': {},
    'n_america': {},
    's_america': {},
}

class country_c():
    '''
    country class,
    '''
    def __init__(self, territory, n_cells, population, population_growth,
                 income_per_capita, literacy_rate, military_spending, number):
        self.territory = territory # actual territory
        self.n_cells= n_cells # number of spaces in the grid
        self.population = population
        self.population_growth = population_growth
        self.income_per_capita = income_per_capita
        self.literacy_rate = literacy_rate
        self.military_spending = military_spending
        self.number = number
        self.gov_rate = 1 #FIXME random number between 1 and 0

        self.is_at_war = False # bool that tells us if the country is at war
                               # if it is it can not start another one

    def __str__(self):
        return json.dumps({
            'territory': self.territory,
            'n_cells': self.n_cells,
            'population': self.population,
            'population_growth': self.population_growth,
            'income_per_capita': self.income_per_capita,
            'literacy_rate': self.literacy_rate,
            'military_spending': self.military_spending,
            'gov_rate': self.gov_rate,
            'is_at_war': self.is_at_war,
            'number': self.number,
        }, indent = 4)

    def total_income(self):
        return self.population * self.income_per_capita

def load_data():
    '''
    load data from json and add it to a dict where the key is the
    country name, and the value is a country_c object
    '''
    # read data from the ../data/data.json
    script_dir = os.path.dirname(__file__)
    path = script_dir + '/' +  DATA_PATH
    with open(path, 'r') as f:
        d = json.loads(f.read())

    i = 1
    for country in countries.keys():
        countries[country] = country_c(
            d.get(country, {}).get('territory', {}).get('mean', {}),
            0, # n_cells
            d.get(country, {}).get('population', {}).get('mean', {}),
            d.get(country, {}).get('growth_rate', {}).get('mean', {}),
            d.get(country, {}).get('income', {}).get('mean', {}),
            0, # literacy_rate
            d.get(country, {}).get('military_spdng', {}).get('mean', {}),
            i,
        )
        i += 1

def build_map(countries):

    # get percentage of territorry we will assing to each country
    # and save it in p
    total = 0
    for d in countries.values():
        total += d.territory

    cells = {
        'africa': round(countries['africa'].territory * 100 / total),
        'europe': round(countries['europe'].territory * 100 / total),
        'middle_east': round(countries['middle_east'].territory * 100 / total),
        'asia': round(countries['asia'].territory * 100 / total),
        'oceania_se_asia': \
            round(countries['oceania_se_asia'].territory * 100 / total),
        'n_america': round(countries['n_america'].territory * 100 / total) - 1,
        's_america': round(countries['s_america'].territory * 100 / total),
    }

    for country, n in cells.items():
        countries[country].n_cells = n

    global grid
    grid = lib.fill_grid(grid, cells)


def war(env):
    while True:
        print(f'day: {env.now}')
        print(grid)
        for j, row in enumerate(grid):
            for i, col in enumerate(row):
                yield env.process(check_for_war(env, (i, j)))

def check_for_war(env, coords):
    yield env.timeout(1)

## look here :)
load_data()
build_map(countries)

print(countries['africa'])

env = simpy.Environment()
env.process(war(env))
env.run(until = 1)

