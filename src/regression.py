import re
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import seaborn as sns

TOP_PATH = os.environ['PWD']
DATA_INPUT_PATH = TOP_PATH + '/data/cleaned/'

#helper function to get all of the data required for a given date range
def get_data_from_range(date_range):
    START_OF_2018_DATA = pd.to_datetime('07-01-2018')
    #Check that date_range is in the format that this code is designed to run it
    assert(len(date_range) == 2 and isinstance(date_range, tuple)), "Incorrect parameter format, should be a tuple of two dates"
    assert(re.match(r"^[0-9]{2}-[0-9]{2}-[0-9]{4}$", date_range[0])), "Incorrect date pattern ('MM-DD-YYYY')"
    assert(re.match(r"^[0-9]{2}-[0-9]{2}-[0-9]{4}$", date_range[1])), "Incorrect date pattern ('MM-DD-YYYY')"

    #Mark the earlier date as the start date
    if pd.to_datetime(date_range[0]) <= pd.to_datetime(date_range[1]):
        start_date = date_range[0]
        end_date = date_range[1]
    else:
        start_date = date_range[1]
        end_date = date_range[0]

    #Use string slicing to find the year of each date
    start_year = int(start_date[-4:])
    end_year = int(end_date[-4:])

    #Because of the way the stop files are made (2018 data being split between the 2017 file and the joint 2018-2019 file),
    #it was required to do some slight altering of the years
    if pd.to_datetime(end_date) >=  START_OF_2018_DATA:
        end_year = 2018
    elif end_year == 2018:
        end_year = 2017
    
    #Make the dataframe to return and loop through the years to concat dataframes
    df = pd.DataFrame()
    for yr in range(start_year, end_year + 1):
        if yr == 2018:
            df = pd.concat([df, pd.read_csv(TOP_PATH + '/data/cleaned/2018-2019_cleaned.csv')])
        else:
            df = pd.concat([df, pd.read_csv(TOP_PATH + '/data/cleaned/' + str(yr) + '_cleaned.csv')])

    df = df[[pd.to_datetime(start_date) <= pd.to_datetime(x) and pd.to_datetime(end_date) >= pd.to_datetime(x) for x in df['date_stop']]]
    return df


        





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

    


        







