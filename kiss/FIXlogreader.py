# -*- coding: utf-8 -*-
"""
Created on Wed Sep 07 10:30:03 2016

@author: Fábio Bissolotti
"""

import pandas as pd
from os import walk
from os.path import join
 
LOGDIR = '..\\Logs'
#LOGFILE = 'FIX.4.4-E2MUS-SGNUS.messages.current.log'

# Filter for messages and tags
tags = ['11', '35', '52', '150']
#tags = ['11', '35', '37', '52', '39', '40', '55', '100', '150', '207', '5149']
status = ['0', '6', 'E' ]

_files = []
for (dirpath, dirnames, filenames) in walk(LOGDIR):
    _files.extend(filenames)
    break

stats = []
for _file in _files:
    LOGFILE = join(dirpath, _file)   
    print '\nProcessando log', LOGFILE, '...'
    rows = []
    with open(LOGFILE) as f:
        for line in f:
            timestamp, body = line.split(' : ')
            
            row_dict = {}
            
            # split each line
            for element in body.split('\x01'):
                try:
                    # split each tag
                    tag, val = element.split('=')
                    if tag == '150' and not val in status:
                        continue
                    if tag in tags:
                        row_dict[tag] = val
                except:
                    pass
            # Message type and order status filter    
            if row_dict['35'] == 'D':
            #if row_dict['35'] == 'F':
            #if row_dict['35'] == 'G':
                rows.append(row_dict)
            elif row_dict['35'] == '8' and row_dict.has_key('150') and row_dict['150'] == '0':
            #elif row_dict['35'] == '8' and row_dict.has_key('150') and row_dict['150'] == '6':
            #elif row_dict['35'] == '8' and row_dict.has_key('150') and row_dict['150'] == 'E':
                rows.append(row_dict)
    
    if rows == []:
        print 'No application data found in this file.'
        continue            
            
    df = pd.DataFrame(rows)
    df['52'] = df['52'].apply(lambda x: pd.Series(pd.to_datetime(x)))
    
    ClOrdID_grp = df.groupby('11')
    
    # Time diferences
    t1 = pd.to_timedelta('00:00:01.000000')
    t2 = pd.to_timedelta('00:00:00.100000')
    x = ClOrdID_grp['52'].apply(lambda x: x - x.shift(1))
    x = x[(x < t1) & (x > t2)]
    xdesc = x.describe()
    xdesc['date'] = df['52'][0]

    stats.append(xdesc)

# Persiste the statistics dataframe
stats_df = pd.DataFrame(stats)
out_filename = join(dirpath,'FIXstats.pkl')
stats_df.to_pickle(out_filename)

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