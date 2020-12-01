# -*- coding: utf-8 -*-
"""
Created on Wed Sep 07 10:30:03 2016

@author: Fábio Bissolotti
"""

import pandas as pd
from os import walk
from os.path import join
import matplotlib.ticker as ticker
 
LOGDIR = '..\\logs'
CLOCK_DELAY = pd.to_timedelta('00:00:00.000000') # Clocl delay in ms

if CLOCK_DELAY > pd.to_timedelta('00:00:00.000000'):
    print('Clock delay is set to ', str(CLOCK_DELAY))
    input('Hit ENTER to continue...')

# Filter for messages and tags
tags = ['1', '11', '35', '52', '55', '150']
#tags = ['11', '35', '37', '52', '39', '40', '55', '100', '150', '207', '5149']
status = ['0', '4', '5', '6', 'E' ]

_files = []
for (dirpath, dirnames, filenames) in walk(LOGDIR):
    _files.extend(filenames)
    break

legend = []
for _file in _files:
    LOGFILE = join(dirpath, _file)   
    print('\n\n*** Processing logfile', LOGFILE, '...')
    legend.append(_file)
    
    rows = []
    with open(LOGFILE) as f:
        for line in f:
            try:
                timestamp, body = line.split(' : ')
            except:
                print('Could not parse this line:', line)
            
            row_dict = {}
            row_dict['ts'] = timestamp
            
            # split each line
            for element in body.split('\x01'):
                try:
                    # split each tag
                    tag, val = element.split('=')
                    if tag == '150' and not val in status:
                        continue
                    # Discard entries using the morning test account
                    if tag == '1' and val == '4004':
                        continue
                    if tag in tags:
                        row_dict[tag] = val
                except:
                    pass
            
            # Discard messages missing account
            if row_dict['35'] == 'D' and '1' not in row_dict:
                continue
            
            # Message type and order status filter
            if row_dict['35'] == 'D':
            #if row_dict['35'] == 'F':
            #if row_dict['35'] == 'G':
                rows.append(row_dict)
                
            elif row_dict['35'] == '8' and '150' in row_dict and row_dict['150'] == '0': # New
            #elif row_dict['35'] == '8' and '150' in row_dict and row_dict['150'] == '4': # Canceled
            #elif row_dict['35'] == '8' and '150' in row_dict and row_dict['150'] == '5': # Replaced
            #elif row_dict['35'] == '8' and '150' in row_dict and row_dict['150'] == '6': # Pending Cancel
            #elif row_dict['35'] == '8' and '150' in row_dict and row_dict['150'] == 'E': # Pending Replace
                rows.append(row_dict)
    
    if rows == []:
        print('No application data found in this file.')
        continue            
            
    df = pd.DataFrame(rows)
    df['52'] = df['52'].apply(lambda x: pd.Series(pd.to_datetime(x)))
    df['ts'] = df['ts'].apply(lambda x: pd.Series(pd.to_datetime(x)))
    
    # Group by tag 11
    ClOrdID_grp = df.groupby(by=['11'])
    
    # Time diferences then filter by t1 and t2
    t1 = pd.to_timedelta('00:00:30.000000')
    t2 = pd.to_timedelta('00:00:00.000000')
    x = ClOrdID_grp['ts'].apply(lambda x: x - x.shift(1) - CLOCK_DELAY)
    x = x[(x < t1) & (x > t2)]

    x = x.astype('timedelta64[ms]')
    x.index = list(range(1, len(x)+1))
    xx = x.plot(title='Cash & Carry', xticks=x.index)
    xx.xaxis.set_major_locator(ticker.MultipleLocator(200))
    xx.set_xlabel('order sequence')
    xx.set_ylabel('ms')
    xx.legend(legend)
