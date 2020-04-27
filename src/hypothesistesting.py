import os
import sys
import json
import pandas as pd
import numpy as np
import glob
from scipy.stats import ttest_ind
from scipy import stats

TOP_PATH = os.environ['PWD']
os.chdir(TOP_PATH + '/data/raw')

races = {'A':'Middle Eastern or South Asian',
'B':'Black/African American',
'C':'Asian',
'D':'Asian',
'F':'Asian',
'G':'Pacific Islander',
'H':'Hispanic/Latino/a',
'I':'Middle Eastern or South Asian',
'J':'Asian',
'K':'Asian',
'L':'Asian',
'O':'Other',
'P':'Pacific Islander',
'S':'Pacific Islander',
'U':'Pacific Islander',
'V':'Asian',
'W':'White',
'Z':'Middle Eastern or South Asian'}

fourteen = pd.read_csv('STOPS_2014.csv')
fourteen['subject_race'] = fourteen['subject_race'].map(races)
fifteen =  pd.read_csv('STOPS_2015.csv')
fifteen['subject_race'] = fifteen['subject_race'].map(races)
sixteen =  pd.read_csv('STOPS_2016.csv')
sixteen['subject_race'] = sixteen['subject_race'].map(races)
seventeen =  pd.read_csv('STOPS_2017.csv')
seventeen['subject_race'] = seventeen['subject_race'].map(races)

ftos = pd.concat([fourteen, fifteen, sixteen, seventeen]).reset_index(drop = True)
ftos = ftos[['stop_id' , 'subject_race', 'date_stop']]

eighteen = pd.read_csv('STOPS_2018-2019.csv')
eighteen['subject_race'] = eighteen.race
eighteen = eighteen[['stop_id', 'subject_race', 'date_stop']]
allyears = pd.concat([ftos, eighteen]).reset_index(drop = True)

def time_period(df, start, end):
    period = df[(df['date_stop'] >= start) & (df['date_stop'] <=end)] 
    return period

def get_ttest(alldata, race, eventcsv, startdate, enddate):
    allstops = time_period(alldata, startdate, enddate)
    racialstops = allstops[allstops['subject_race'] == race]
    val = racialstops.groupby('date_stop')['stop_id'].count().values
    ind = racialstops.groupby('date_stop')['stop_id'].count().index
    total = allstops.groupby('date_stop')['stop_id'].count().values
    newdf1 = pd.DataFrame()
    newdf1['date_stop'] = ind
    newdf1['Stop_Counts'] = val
    newdf1['date_stop'] = pd.to_datetime(newdf1.date_stop, format= '%Y-%m-%d')
    allstops['date_stop'] = pd.to_datetime(allstops.date_stop, format= '%Y-%m-%d')
    allstops = pd.DataFrame(allstops.groupby('date_stop')['stop_id'].count())
    
    combo = newdf1.merge(allstops,how='outer', on='date_stop')
    combo.stop_id = total
    combo.Stop_Counts[np.isnan(combo.Stop_Counts)] = 0
    combo['date'] = combo['date_stop']
    combo = combo[['date', 'Stop_Counts', 'stop_id']]
    
    ev = pd.read_csv(eventcsv)
    ev = ev[['date', 'value']]
    ev.date =  pd.to_datetime(ev.date, format= '%Y-%m-%d')
    
    merged = combo.merge(ev, on='date')
    merged.value = pd.to_numeric(merged.value, errors='coerce')
    merged.value[np.isnan(merged.value)] = 0
    
    merged1 = merged.copy()
    
    merged.Stop_Counts = (merged.Stop_Counts/merged.stop_id)
    return ttest_ind(merged.stop_id, merged.value, equal_var=False), merged1

