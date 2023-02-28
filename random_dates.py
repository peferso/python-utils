"""
Credits to akilat90: https://stackoverflow.com/questions/50559078/generating-random-dates-within-a-given-range-in-pandas
"""
import pandas as pd
import numpy as np


def random_dates(start, end, n=10):

    start_u = start.value//10**9
    end_u = end.value//10**9

    return pd.to_datetime(np.random.randint(start_u, end_u, n), unit='s')

# start = pd.to_datetime('2015-01-01')
# end = pd.to_datetime('2018-01-01')
# random_dates(start, end)
