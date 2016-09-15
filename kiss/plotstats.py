# -*- coding: utf-8 -*-

from os.path import join
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.style.use('ggplot')

def plot(file_name, chart_title):
    
    # Load DataFrame from file
    file_name = join('..\\stats',file_name)
    stats_df = pd.read_pickle(file_name)
    sdf = stats_df.copy()
    sdf = sdf.dropna()
    
    # Remove outliers
    sdf = sdf[np.abs(sdf['mean'] - sdf['mean'].mean()) <= (2 * sdf['mean'].std())]    
    
    # Convert to timedelta64
    sdf['mean'] = sdf['mean'].astype('timedelta64[ms]')
    sdf['std'] = sdf['std'].astype('timedelta64[ms]')
    sdf['min'] = sdf['min'].astype('timedelta64[ms]')
    sdf['max'] = sdf['max'].astype('timedelta64[ms]')
    sdf['25%'] = sdf['25%'].astype('timedelta64[ms]')
    sdf['75%'] = sdf['75%'].astype('timedelta64[ms]')
    
    # Plot
    p1 = sdf.plot(x=pd.to_datetime(sdf.date), y=['min', '25%', '75%', 'mean'], title=chart_title)
    p1.set_ylabel('ms')    
    
    p2 = sdf.plot(x=pd.to_datetime(sdf.date), y=['std'], title=chart_title)
    p2.set_ylabel('ms')   
    
    p3 = sdf.plot(x=pd.to_datetime(sdf.date), y=['max'], ylim=50, title=chart_title)
    p3.set_ylabel('ms')
    
    sdf.plot(x=pd.to_datetime(sdf.date), y=['count'], title=chart_title)
    
    return sdf
