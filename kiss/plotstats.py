# -*- coding: utf-8 -*-

from os.path import join
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')

# Load DataFrame from file
filename = join('..\\Logs','FIXstats.pkl')
stats_df = pd.read_pickle(filename)

# Plot
stats_df['mean'] = stats_df['mean'].astype('timedelta64[ms]')
stats_df['std'] = stats_df['std'].astype('timedelta64[ms]')
stats_df['min'] = stats_df['min'].astype('timedelta64[ms]')
stats_df['max'] = stats_df['max'].astype('timedelta64[ms]')
stats_df['25%'] = stats_df['25%'].astype('timedelta64[ms]')
stats_df['75%'] = stats_df['75%'].astype('timedelta64[ms]')
stats_df.plot(x=pd.to_datetime(stats_df.date), y=['min', '25%', '75%', 'mean'])
stats_df.plot(x=pd.to_datetime(stats_df.date), y=['std'])
stats_df.plot(x=pd.to_datetime(stats_df.date), y=['max'])
stats_df.plot(x=pd.to_datetime(stats_df.date), y=['count'])
