import pandas as pd
import datetime
import numpy as np
from random_dates import random_dates
import pytz


# %%
# Available timezone codes
#
pytz.all_timezones

# %%
# Create some dummy data
#
start = pd.to_datetime('2015-01-01')
end = pd.to_datetime('2018-01-01')
df = pd.DataFrame(
    {
        'date': random_dates(start, end)
    }
)
df['date_str'] = df['date'].dt.strftime('%Y-%m-%d %H:%M:%S')

# %%
# Set a timezone
#
df['date_UTC'] = df['date'].dt.tz_localize('UTC')

# %%
# Change from one timezone to another
#
df['date_CST'] = df['date_UTC'].dt.tz_convert('US/Central')
df['date_ElSalvador'] = df['date_UTC'].dt.tz_convert('America/El_Salvador')

# %%
# From a str column
#
df['date_CST_2'] = pd.to_datetime(
    df['date_str'], utc=True
).dt.tz_convert('America/El_Salvador')


# %%
# Get the difference in hours betwee two timezones given a input date time.
#
def get_hours_dif(
    timezone_A: str,
    timezone_B: str,
    date_time: pd.api.types.DatetimeTZDtype
) -> float:
    datetime_A = pd.Series(date_time).dt.tz_localize(timezone_A)
    datetime_B = datetime_A.dt.tz_convert(timezone_B)
    _datetime_A = pd.to_datetime(datetime_A.dt.strftime('%Y-%m-%d %H:%M:%S'))
    _datetime_B = pd.to_datetime(datetime_B.dt.strftime('%Y-%m-%d %H:%M:%S'))
    time_dif = (_datetime_B - _datetime_A).astype('timedelta64[h]')
    return time_dif.values[0]
