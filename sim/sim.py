import json

import numpy as np
import simpy

import lib

RANDOM_SEED = 42
INCOME_THRESHOLD = 0 # FIXME this should be diff than 0
POP_THRESHOLD = 0 # FIXME this should be diff than 0
MAP_SIZE = 10 # grid size nxn

grid = np.zeros([MAP_SIZE, MAP_SIZE], dtype = int)

class country_c():
    '''
    country class,
    '''
    def __init__(self, territory, n_cells, population, population_growth,
                 income_per_capita, literacy_rate, military_spending):
        self.territory = territory # actual territory
        self.n_cells= n_cells # number of spaces in the grid
        self.population = population
        self.population_growth = population_growth
        self.income_per_capita = income_per_capita
        self.literacy_rate = literacy_rate
        self.military_spending = military_spending
        self.gov_rate = 1 #FIXME random number between 1 and 0

        self.is_at_war = False # bool that tells us if the country is at war
                               # if it is it can not start another one
        self.number = None

    def total_income(self):
        return self.population * self.income_per_capita



def setup():

    # FIXME get this data from the data team
    t = {
        'africa': 22874822.413793102,
        'europe': 24013826.137931034,
        'asia': 12038027.879310345,
        'seme_asia': 16254452.465517242,
        'n_america': 22248771.896551725,
        's_america': 14953913.793103449,
        'oceania': 795158.9655172414,
    }

    # TODO read all data of the data team, and load it to countries structure
    # also each country will be represented in the grid as a number, so be
    # sure to set the `number` attr

    # e.g. of how to create a country
    africa = country_c(
        0, # territory
        0, # n_cells
        0, # population
        0, # population_growth
        0, # income_per_capita
        0, # literacy_rate
        0, # military_spending
    )

    # get percentage of territorry we will assing to each country
    # and save it in p
    total = 0
    for territoy in t.values():
        total += territoy
    p = {
        'africa': round(t['africa'] * 100 / total),
        'europe': round(t['europe'] * 100 / total),
        'asia': round(t['asia'] * 100 / total),
        'seme_asia': round(t['seme_asia'] * 100 / total),
        'n_america': round(t['n_america'] * 100 / total),
        's_america': round(t['s_america'] * 100 / total),
        'oceania': round(t['oceania'] * 100 / total),
    }

    global grid
    grid = lib.fill_grid(grid, p)

setup()

def war(env):
    while True:
        print(f'day: {env.now}')
        print(grid)
        for j, row in enumerate(grid):
            for i, col in enumerate(row):
                yield env.process(check_for_war(env, (i, j)))

def check_for_war(env, coords):
    yield env.timeout(1)

env = simpy.Environment()
env.process(war(env))
env.run(until = 1)
