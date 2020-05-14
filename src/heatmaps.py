import sys
sys.path.insert(0,'../src')
sys.path.insert(0,'../data')
sys.path.insert(0,'../upload_data')
sys.path.insert(0,'../config')
sys.path.insert(0,'..')
import geopandas as gpd
import pandas as pd
import geoplot as gplt
import geoplot.crs as gcrs
import matplotlib.pyplot as plt
import etl
import json
import cleaning
import datetime


def make_areas():
    areas = gpd.read_file('http://seshat.datasd.org/sde/pd/pd_beats_datasd.zip')
    areas = areas.drop(['objectid', 'name', 'beat', 'div'],axis = 1)
    return areas

def make_denominator(census, race):
    table = pd.pivot_table(census,index = 'serv', values = [race, 'Total'], aggfunc = sum)
    table = table.div(table.iloc[:,-1],axis = 0).drop('Total', axis = 1)
    table = table.rename(columns={race:'denominator'})
    return table

def make_numerator(df,race,start_date,end_date):
    numer = df[(df['date_stop'] >= start_date) & (df['date_stop'] <= end_date)]
    numer = pd.pivot_table(numer, index = 'service_area', columns = 'subject_race', values = 'stop_id', aggfunc = 'count',fill_value=0)
    numer['Total'] = numer.apply(sum, axis = 1)
    numer = numer.div(numer.iloc[:,-1],axis = 0)
    try:
        numer.index = numer.index.astype('int64')
    except:
        numer = numer.drop('Unknown')
        numer.index = numer.index.astype('int64')
    numer = pd.DataFrame(numer[race])
    return numer.rename(columns={race:'numerator'})

def make_proportions(df,race,start_date,end_date):
    census_fp = '../upload_data/sd_population.csv'
    census =  pd.read_csv(census_fp)
    numers = make_numerator(df,race,start_date,end_date)
    denoms = make_denominator(census, race)
    merger = numers.merge(denoms, left_index=True,right_index=True)
    return pd.DataFrame(merger.numerator/merger.denominator, columns=['prop'])

def make_heat(df,race,event,start_date,end_date):
    areas = make_areas()
    props = make_proportions(df,race,start_date,end_date)
    heat = areas.merge(props, left_on='serv',right_index=True, how='outer')
    heat = heat.dissolve(by='serv',aggfunc='first').fillna(0).drop(0)
    fig, ax = plt.subplots(1, figsize=(10,10))
    ax.axis('off')
    ax.set_title(f'Proportion of {race} Drivers Stopped By Service Area\n Event: {event}'.format(race,event), fontdict={'fontsize':'25','fontweight' : '3'})
    sm = plt.cm.ScalarMappable(cmap='Blues', norm=plt.Normalize(vmin=0, vmax=heat.prop.max()))
    fig.colorbar(sm)
    heat.plot(column='prop', cmap='Blues', linewidth=0.8, ax=ax, edgecolor='0.8')