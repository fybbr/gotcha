# -*- coding: utf-8 -*-
"""
Created on Fri Sep 09 14:13:20 2016

@author: Fabio Bissolotti
"""

'''
# Read persisted DF
df = pd.read_pickle(file_name)

stats_df.assign(dt = lambda x: pd.to_datetime(x.date))

# Ploting
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
%matplotlib inline
matplotlib.style.use('ggplot')
stats_df['mean'].astype('timedelta64[ms]').plot() ou hist()
stats_df.plot(x=pd.to_datetime(stats_df.date),y='count'
stats_df.plot(x=pd.to_datetime(stats_df.date), y='mean')

# Converte o tipo de uma col
sdf['mean'] = sdf['mean'].astype('timedelta64[ms]')

# Grouping
ClOrdID_grp.first()
ClOrdID_grp.last()
ClOrdID_grp.get_group('xxxx')
grouped['C'].agg([np.sum, np.mean, np.std])

.describe()
.size()

t = pd.to_timedelta('00:00:01.000000')
t2 = pd.to_timedelta('00:00:00.100000')
x[(x < t) & (x > t2)].describe()

for name, group in ClOrdID_grp:
    print(group)
    
df1.change.shift(1) - df1.change

'''