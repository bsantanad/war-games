import random
import time
import json
import os

import numpy as np
import simpy

import lib

import colorama

'''
FIXME
does not consider internal conflicts
does not conisder peace times
does not consider government at all
does not consider growth population
does not consider literacy
does not consider peace times
'''

def color_sign(x):
    c = colorama.Fore.WHITE
    if x == 1:
        c = colorama.Fore.GREEN
    if x == 2:
        c = colorama.Fore.RED
    if x == 3:
        c = colorama.Fore.BLUE
    if x == 4:
        c = colorama.Fore.YELLOW
    if x == 5:
        c = colorama.Fore.WHITE
    if x == 6:
        c = colorama.Fore.MAGENTA
    if x == 7:
        c = colorama.Fore.CYAN
    return f'{c}{x}'

np.set_printoptions(formatter={'int': color_sign})

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

        self.is_at_war = [] # list of coords that are at war

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
    '''
    based on the percentage of initial territory build the map, this
    is a grid 10 by 10 with numbers that represent the countries
    '''
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


def war():
    env = None
    day = 0
    while True:
        if day == 10:
            break
        time.sleep(1)
        print(f'day: {day}')
        print(grid)

        # we will use the income and population density of the whole world in
        # order to build distributions, and get the mean and standard deviation
        incomes = []
        for country in countries.values():
            incomes.append(country.income_per_capita)
        income_std = np.std(incomes)

        populations = []
        for country in countries.values():
            populations.append(country.population)
        populations_mean = np.mean(populations)
        populations_std = np.std(populations)

        for j, row in enumerate(grid):
            for i, col in enumerate(row):
                check_for_war(
                    env, (j, i),
                    income_std,
                    populations_std,
                    populations_mean
                )
        day += 1

def check_for_war(env, coords, income_std, populations_std, populations_mean):
    '''
    this checks if we need to start a war, first it will find the neighbours
    and then get the countries info. based on that it will calculate if
    the war need to be started if so, call start_war if not do nothing

    the grid is also a global variable, so there you can use it inside the
    function without much trouble
    '''
    # get country we are currently at
    country_num = grid[coords[0]][coords[1]]
    for name, country in countries.items():
        if country.number == country_num:
            country_name = name
            break

    '''
    # FIXME check if this works
    for c in countries[country_name].is_at_war:
        if c == coords:
            #print(f'{coords} already at war')
            return
    '''

    # get neighbours in grid and then get the actual country that number
    # represents
    neigh_coords = lib.get_neighbours(coords[0], coords[1], MAP_SIZE)
    neigh_nums = [None, None, None, None]
    for i, neigh in enumerate(neigh_coords):
        if not neigh:
            continue
        neigh_nums[i] = grid[neigh[0]][neigh[1]]

    neighbours = [None, None, None, None]
    for i, n in enumerate(neigh_nums):
        for name, country in countries.items():
            if country.number == n:
                neighbours[i] = name
                break

    # check if the neighbours are the same country as us
    for i, neigh in enumerate(neighbours):
        if neigh == country_name:
            neighbours[i] = None

    # we are deep in our contury no relevant neighbours
    if neighbours.count(None) == len(neighbours):
        return
    #print(f'found neighbour of {country_name} at {env.now}')
    #print(neighbours)

    # check for war income trigger
    for i, neighbour in enumerate(neighbours):
        if not neighbour:
            continue
        '''
        for c in countries[neighbour].is_at_war:
            #print(c)
            #print(neigh_coords[i])
            if c == neigh_coords[i]:
                #print('already at war')
                return
        '''
        #print(f'checking for conflict between {country_name} and {neighbour}')
        # neighbour total income
        n_total_income = countries[neighbour].income_per_capita * \
                         countries[neighbour].population
        # country total income
        c_total_income = countries[country_name].income_per_capita * \
                         countries[country_name].population

        # if neighbour country total income is within one std deviation of
        # owns, then launch the war
        if c_total_income - n_total_income < income_std:
            countries[neighbour].is_at_war.append(neigh_coords[i])
            countries[neighbour].is_at_war.append(coords)
            #print('=======start war')
            #print(f'conflict between {country_name} and {neighbour}')
            winner = start_war(
                env,
                coords,
                neigh_coords[i],
                country_name,
                neighbour,
            )
            if winner == country_name:
                grid[neigh_coords[i][0]][neigh_coords[i][1]] = \
                     countries[country_name].number
            elif winner == neighbour:
                grid[coords[0]][coords[1]] = \
                     countries[neighbour].number
            return

    # check for population trigger
    # if population density reaches one std dev above the median of the region,
    # a conflict will be triggered in order to look for further territory.
    if countries[country_name].population + populations_std > populations_mean:
        lowest = -1
        n_lowest = None
        c_lowest = None
        for i, neighbour in enumerate(neighbours):
            if not neighbour:
                continue
            for c in countries[neighbour].is_at_war:
                if c == neigh_coords[i]:
                    #print('already at war')
                    return
            if countries[neighbour].income_per_capita < lowest:
                n_lowest = neighbour
                c_lowest = neigh_coords[i]
                lowest = countries[neighbour].income_per_capita
                continue

        if n_lowest:
            #print(f'conflict between {country_name} and {n_lowest}')
            #print('=======start war')
            start_war(env, coords, c_lowest, country_name, n_lowest)

def start_war(env, coords, n_coords, country_s, country_a):
    '''
    calculate the outcome of a war between two countries:
    country_s is the one that started the war
    country_a is the one that is against

    n_coords neighbour coords

    here we also need to substract causalties and all that
    it is done by accessing the global dict: `countries`
    if say, you want to access africa you would do
    countries['africa'].population -= casualties
    '''
    cwi_s = lib.cwi(
        countries[country_s].income_per_capita * \
            countries[country_s].population,
        countries[country_s].gov_rate,
        1, #FIXME
        countries[country_s].military_spending,
        1,
    )
    cwi_a = lib.cwi(
        countries[country_a].income_per_capita * \
            countries[country_s].population,
        countries[country_a].gov_rate,
        1, #FIXME
        countries[country_a].military_spending,
        random.uniform(0, 1), #luck
    )
    if cwi_s > cwi_a:
        #print(f'{country_s} won')
        df = lib.dead_toll(cwi_s, cwi_a)
        countries[country_s].population = lib.population_after_war(
            countries[country_s].population / countries[country_s].territory,
            countries[country_s].population,
            df,
            1,
        )
        countries[country_a].population = lib.population_after_war(
            countries[country_a].population / countries[country_a].territory,
            countries[country_a].population,
            df,
            0,
        )
        return country_s
    else:
        #print(f'{country_a} won')
        df = lib.dead_toll(cwi_a, cwi_s)
        countries[country_s].population = lib.population_after_war(
            countries[country_s].population / countries[country_s].territory,
            countries[country_s].population,
            df,
            0,
        )
        countries[country_a].population = lib.population_after_war(
            countries[country_a].population / countries[country_a].territory,
            countries[country_a].population,
            df,
            1,
        )
        return country_a

## flow starts here:)
load_data()
build_map(countries)
war()
