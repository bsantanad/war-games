import numpy as np
import simpy

RANDOM_SEED = 42
INCOME_THRESHOLD = 0 # FIXME this should be diff than 0
POP_THRESHOLD = 0 # FIXME this should be diff than 0
MAP_SIZE = 5 # grid size

class country_c():
    '''
    country class,
    '''
    def __init__(env, territory, population, population_growth,
                 income_per_capita, literacy_rate, military_spending):
        self.env = env
        self.territory = territory # list of positions in the grid
        self.population = population
        self.population_growth = population_growth
        self.income_per_capita = income_per_capita
        self.literacy_rate = literacy_rate
        self.gov_rate = 1 #FIXME random number between 1 and 0

    def total_income(self):
        return self.population * self.income_per_capita

def setup():
    t = {
        'africa': 19,
        'europe': 5,
        'n_america': 8,
        's_america': 7,
        'oceania': 6,
        'se_asia': 4,
        'middle_east': 2
    }
    avg = 0
    for territoy in t.values():
        avg += territoy

    grid = np.zeros([MAP_SIZE, MAP_SIZE], dtype = int)

setup()
