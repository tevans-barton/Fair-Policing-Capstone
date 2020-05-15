import re
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import seaborn as sns
from get_date_range_df import get_data_from_range

TOP_PATH = os.environ['PWD']
DATA_INPUT_PATH = TOP_PATH + '/data/cleaned/'

def regression(date_range, race, issue, reg_type = 'log'):
    assert (reg_type == 'linear' or reg_type == 'log'), "Regression type must be one of 'linear' or 'log'"
    issue = issue.replace(' ', '_')

    #Read in the data you need from the date range given using helper function above
    df = get_data_from_range(date_range)

    #Create a binary column to see if a stop was for that race or not
    df[race] = [1 if x == race else 0 for x in df['subject_race']]

    #Group dataframe by the day of the stop and calculate the stop rate for the given race on that day
    df = df[['date_stop', race]].groupby('date_stop').mean().reset_index()
    
    #Get/clean the search trends for the given issue
    search_df = pd.read_csv(TOP_PATH + '/data/raw/' + issue + '.csv')
    search_df.drop('Unnamed: 0', inplace = True, axis = 1, errors = 'ignore')
    search_df['value'] = [int(x) if str(x).isnumeric() else 0 for x in search_df['value']]
    search_df['log_value'] = [np.log(x + .001) for x in search_df['value']]

    #merge together stop data and search trend data
    df_final = df.merge(search_df, left_on = 'date_stop', right_on = 'date')

    #Do linear regression against the search trend value
    if reg_type == 'linear':
        df_final = df_final.sort_values('value').reset_index(drop = True)
        reg = LinearRegression().fit(df_final['value'].values.reshape(-1,1), df_final[race].values)
        ax = sns.regplot(df_final['value'], df_final[race], scatter = True, fit_reg = True)
        ax.set(xlabel = 'Search Trend Value', 
            ylabel=('Percentage of Stops that were ' + str(race)), 
                title = ('Stop Rate of ' + str(race) + ' vs. Search Trend Rate'))
    
    #Do linear regression against the log of the search trend value
    else:
        df_final = df_final.sort_values('log_value').reset_index(drop = True)
        reg = LinearRegression().fit(df_final['log_value'].values.reshape(-1,1), df_final[race].values)
        ax = sns.regplot(df_final['log_value'], df_final[race], scatter = True, fit_reg = True)
        ax.set(xlabel = 'Log of Search Trend Value', 
            ylabel=('Percentage of Stops that were ' + str(race)), 
                title = ('Stop Rate of ' + str(race) + ' vs. Log of Search Trend Rate'))
    return reg

    


        







