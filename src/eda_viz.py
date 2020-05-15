import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
from get_date_range_df import get_data_from_range

TOP_PATH = os.environ['PWD']
DATA_OUTPATH = TOP_PATH + '/eda_visualizations'


def month_race_count_viz(date_range, issue, save_fig = False):
    month_dictionary = {
    1 : 'Jan',
    2 : 'Feb',
    3 : 'Mar',
    4 : 'Apr',
    5 : 'May',
    6 : 'Jun',
    7 : 'Jul',
    8 : 'Aug',
    9 : 'Sep',
    10 : 'Oct',
    11 : 'Nov',
    12 : 'Dec'
    }
    #Use get_data_from_range helper method to get a dataframe from given date range
    df_window = get_data_from_range(date_range)
    #Select out the columns that we are focused on in this project
    df_window = df_window[['stop_id', 'service_area', 'subject_race', 'date_stop']]
    df_window['Month'] = df_window['date_stop'].str.slice(5,7)
    df_window = df_window.astype({'Month' : int})
    viz_df = df_window.pivot_table(values = 'stop_id', index = 'Month', columns = 'subject_race', aggfunc = 'count')
    viz_df.index = viz_df.index.map(month_dictionary)
    ax = viz_df.plot.bar(stacked = True, figsize = [12, 6.75])
    ax.set(title = 'Counts of Race Stops in Window Around {iss} by Month'.format(iss = issue),
           ylabel = 'Individuals Stopped')
    fig = ax.figure
    if save_fig:
        if not os.path.exists(DATA_OUTPATH):
            os.makedirs(DATA_OUTPATH, exist_ok = True)
        fig.savefig(DATA_OUTPATH + '/{iss}_RACE_BY_MONTH_DISTR.png'.format(iss = issue))
    return


