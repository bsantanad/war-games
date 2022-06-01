'''
helper functions for the simulation
'''

def cwi(ti, gr, lr, ms, lk):
    '''
    calculate capability of war index
    :params:
        TI = country's total income
        GR = government rate
        LR = literacy rate
        MS = military spending
        LK = luck
    '''
    return ti * gr * lr * ms * lk

def dead_toll(cwi_winning_side, cwi_loosing_side):
    '''
    calculate the dead toll based on the cwi of a war
    '''
    return cwi_loosing_side / cwi_winning_side

def population_after_war(population_density, total_population, df, is_winner):
    '''
    get the population of a country after a war, you send the population
    density, the dead toll, and if the country you want to calc is the winner
    df: dead_toll
    '''
    if is_winner:
        tmp = (1 - dead_toll) * dead_toll * population_density
        return tmp - total_population

    return (dead_toll * population_density) - total_population

def fill_grid(grid, countries):
    '''
    given a grid and a dict of countries:
    {
        "africa": 20,
        "europe": 21,
        "asia": 11,
        "seme_asia": 14,
        "n_america": 20,
        "s_america": 13,
        "oceania": 1
    }

    it will fill the grid accordingly to the numbers of each country
    for example:
    [[1 1 1 1 1 1 1 1 1 1]
     [1 1 1 1 1 1 1 1 1 1]
     [2 2 2 2 2 2 2 2 2 2]
     [2 2 2 2 2 2 2 2 2 2]
     [2 3 3 3 3 3 3 3 3 3]
     [3 3 4 4 4 4 4 4 4 4]
     [4 4 4 4 4 4 5 5 5 5]
     [5 5 5 5 5 5 5 5 5 5]
     [5 5 5 5 5 5 6 6 6 6]
     [6 6 6 6 6 6 6 6 6 7]]

    :returns: np.matrix
    '''
    i = 0
    j = 0

    n = 1
    for country, value in countries.items():
        while(value > 0):
            grid[j][i] = n
            i += 1
            if i >= len(grid):
                i = 0
                j += 1
            value -= 1
        n += 1
    return grid

def get_neighbours(i, j, map_len):
    '''
    :returns: coord for
        left, right, up, down
    '''
    left = (i, j - 1)
    right = (i, j + 1)
    top = (i - 1, j)
    down = (i + 1, j)
    if j - 1 < 0:
        left = None
    if j + 1 > map_len - 1:
        right = None
    if i - 1 < 0:
        top = None
    if i + 1 > map_len - 1:
        down = None

    return left, right, top, down
