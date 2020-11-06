# -*- coding: utf-8 -*-
"""
Created on Wed Sep 07 10:30:03 2016

@author: Fábio Bissolotti
"""

import pandas as pd
from os import walk
from os.path import join
 
LOGDIR = '..\\logs-xp'
#LOGFILE = 'FIX.4.4-E2MUS-SGNUS.messages.current.log'

# Filter for messages and tags
tags = ['11', '35', '52', '100', '150']
#tags = ['11', '35', '37', '52', '39', '40', '55', '100', '150', '207', '5149']
status = ['0', '6', 'E' ]

_files = []
for (dirpath, dirnames, filenames) in walk(LOGDIR):
    _files.extend(filenames)
    break

stats = []
for _file in _files:
    LOGFILE = join(dirpath, _file)   
    print('\n\n*** Processing logfile', LOGFILE, '...')
    rows = []
    with open(LOGFILE) as f:
        for line in f:
            try:
                timestamp, body = line.split(' : ')
            except:
                print('Could not parse this line:', line)
            
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
                rows.append(row_dict)
            elif row_dict['35'] == '8' and '150' in row_dict and row_dict['150'] == '0':
                rows.append(row_dict)
    
    if rows == []:
        print('No application data found in this file.')
        continue            
            
    df = pd.DataFrame(rows)
    df['52'] = df['52'].apply(lambda x: pd.Series(pd.to_datetime(x)))
    
    ClOrdID_grp = df.groupby('11')
    
    # Fill missing ExecID tags (100) 
    route_df = ClOrdID_grp['100'].fillna(method='ffill')
    route_df = route_df.to_frame()
    route_df.columns = ['route']
    
    # Time diferences
    t1 = pd.to_timedelta('00:00:01.000000')
    t2 = pd.to_timedelta('00:00:00.000000')
    delta = ClOrdID_grp['52'].apply(lambda x: x - x.shift(1))
    delta = delta[(delta < t1) & (delta > t2)]
    delta_df = delta.to_frame()
    delta_df.columns = ['delta']
    
    # Join Routes and Deltas
    plt_df = delta_df.join(route_df)
    plt_df['delta'] = plt_df['delta'].astype('timedelta64[ms]')

    for name, group in plt_df.groupby('route'):
        print('*** Ploting', name)
        group.plot(title=str(name))

print('*** Done!')
