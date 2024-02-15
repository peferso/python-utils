# %%
import pandas as pd


def get_row(data, column, N=None):
    """
    From input dataframe column, creates a
    generator that yields each time each
    row value up to row N.
    """
    if N is None:
        N = data.shape[0]
    if N > data.shape[0]:
        raise ValueError('N is greater than the number of rows')
    for i in range(N):
        yield data[column].iloc[i]

some_data = pd.DataFrame(
        {
            'col': [1, 2, 3, 4, 5, 6]
        }
    )

# %%
values = get_row(some_data, 'col', 3)

# %%
next(values)
# %%
next(values)
# %%
next(values)

# %%
[i for i in get_row(some_data, 'col')]