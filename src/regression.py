import re
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import seaborn as sns

TOP_PATH = os.environ['PWD']
DATA_INPUT_PATH = TOP_PATH + '/data/cleaned/'

def regression(date_range, race, issue):
    #Check that date_range is in the format that this code is designed to run it
    assert(len(date_range) == 2 and isinstance(date_range, tuple)), "Incorrect parameter format, should be a tuple of two dates"
    assert(re.match(r"^[0-9]{2}-[0-9]{2}-[0-9]{4}$", date_range[0])), "Incorrect date pattern ('MM-DD-YYYY')"
    assert(re.match(r"^[0-9]{2}-[0-9]{2}-[0-9]{4}$", date_range[1])), "Incorrect date pattern ('MM-DD-YYYY')"
    issue = issue.replace(' ', '_')
    #Mark the earlier date as the start date
    if pd.to_datetime(date_range[0]) <= pd.to_datetime(date_range[1]):
        start_date = date_range[0]
        end_date = date_range[1]
    else:
        start_date = date_range[1]
        end_date = date_range[0]

    #Use string slicing to find the month, day, and year of each date
    start_month = int(start_date[0:2])
    start_day = int(start_date[3:5])
    start_year = int(start_date[-4:])

    end_month = int(end_date[0:2])
    end_day = int(end_date[3:5])
    end_year = int(end_date[-4:])

    #Read in the data that we need for the ranges
    #Will have issues with certain ranges, but will work for our purposes
    if start_year == 2019:
        df = pd.read_csv(DATA_INPUT_PATH + '2018-2019_cleaned.csv')
    elif start_year == 2018:
        df_1 = pd.read_csv(DATA_INPUT_PATH + '2017_cleaned.csv')
        df_2 = pd.read_csv(DATA_INPUT_PATH + '2018-2019_cleaned.csv')
        df = pd.concat([df_1, df_2])
    elif start_year == end_year:
        df = pd.read_csv(DATA_INPUT_PATH + str(start_year) + '_cleaned.csv')
    else:
        df_1 = pd.read_csv(DATA_INPUT_PATH + str(start_year) + '_cleaned.csv')
        df_2 = pd.read_csv(DATA_INPUT_PATH + str(end_year) + '_cleaned.csv')
        df = pd.concat([df_1, df_2])
    
    df = df[[pd.to_datetime(start_date) <= pd.to_datetime(x) and pd.to_datetime(end_date) >= pd.to_datetime(x) for x in df['date_stop']]]
    df[race] = [1 if x == race else 0 for x in df['subject_race']]
    df = df[['date_stop', race]].groupby('date_stop').mean().reset_index()
    
    search_df = pd.read_csv(TOP_PATH + '/data/raw/' + issue + '.csv')
    search_df.drop('Unnamed: 0', inplace = True, axis = 1, errors = 'ignore')
    search_df['value'] = [int(x) if x.isnumeric() else 0 for x in search_df['value']]
    df_final = df.merge(search_df, left_on = 'date_stop', right_on = 'date')
    df_final = df_final.sort_values('value').reset_index(drop = True)
    reg = LinearRegression().fit(df_final['value'].values.reshape(-1,1), df_final[race].values)
    sns.regplot(df_final['value'], df_final[race], scatter = True, fit_reg = True)
    return reg

    


        







