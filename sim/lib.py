'''
helper functions for the simulation
'''
import colorama

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
        tmp = (1 - df) * df * population_density
        return total_population - tmp
    return total_population - (df * population_density)

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

def print_current_state(countries):
    for n, c in countries.items():
        print(n)
        print('--------------------------')
        print(c)
        print('--------------------------')

def color_sign(x):
    c = colorama.Fore.WHITE
    if x == 1:
        c = colorama.Fore.GREEN
    if x == 2:
        c = colorama.Fore.RED
    if x == 3:
        c = colorama.Fore.RESET
    if x == 4:
        c = colorama.Fore.YELLOW
    if x == 5:
        c = colorama.Fore.WHITE
    if x == 6:
        c = colorama.Fore.MAGENTA
    if x == 7:
        c = colorama.Fore.CYAN
    return f'{c}{x}'
