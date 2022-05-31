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
    return ti * gr * ls * ms * lk

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
