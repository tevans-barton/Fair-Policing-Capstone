import sys
sys.path.insert(0,'src')
sys.path.insert(0,'data')
sys.path.insert(0,'upload_data')
import geopandas as gpd
import pandas as pd
import geoplot as gplt
import geoplot.crs as gcrs
import matplotlib.pyplot as plt



def make_merged():
    census_fp = '../upload_data/sd_population.csv'
    census =  pd.read_csv(census_fp)
    areas = gpd.read_file('http://seshat.datasd.org/sde/pd/pd_beats_datasd.zip')
    areas = areas.drop(['objectid', 'name'],axis = 1)
    heat = areas.merge(census, on=['beat','serv'],how = 'outer')
    heat = heat.dropna()
    return heat

def population_heat(table, race):
    def roundup(x):
        return x if x % 100 == 0 else x + 100 - x % 100
    vmin, vmax = 0, roundup(table[race].max())
    fig, ax = plt.subplots(1, figsize=(10,10))
    ax.axis('off')
    ax.set_title('# of {r} per each Region'.format(r = race), fontdict={'fontsize':'25','fontweight' : '3'})
    sm = plt.cm.ScalarMappable(cmap='Blues', norm=plt.Normalize(vmin=vmin, vmax=vmax))
    fig.colorbar(sm)
    table.plot(column=race, cmap='Blues', linewidth=0.8, ax=ax, edgecolor='0.8')
