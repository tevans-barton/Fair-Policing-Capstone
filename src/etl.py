import pandas as pd
import os
import json

OLD_FORMAT_URL_FIRST_HALF = 'http://seshat.datasd.org/pd/vehicle_stops_'
OLD_FORMAT_URL_SECOND_HALF = '_datasd_v1.csv'
NEW_FORMAT_URL_FIRST_HALF = 'http://seshat.datasd.org/pd/ripa_'

def get_table(year, ripa_suffixes = None, ripa_columns = None):
    if year < 2018:
        url = OLD_FORMAT_URL_FIRST_HALF + str(year) + OLD_FORMAT_URL_SECOND_HALF
        df = pd.read_csv(url)
        df = df.drop(['sd_resident', 'date_time'], axis = 1)
    else:
        df = pd.read_csv(NEW_FORMAT_URL_FIRST_HALF + ripa_suffixes[0])[ripa_columns[0]]
        for i in range(1, len(ripa_suffixes)):
            temp_df = pd.read_csv(NEW_FORMAT_URL_FIRST_HALF + ripa_suffixes[i])[ripa_columns[i]]
            df = pd.merge(df, temp_df, on = 'stop_id')
            df = df.drop_duplicates(['stop_id'])
    return df


def get_data(years, ripa_suffixes, ripa_columns, outpath):
    if not os.path.exists(outpath):
        os.makedirs(outpath, exist_ok = True)
    for y in years:
        if y == 2018:
            get_table(y, ripa_suffixes, ripa_columns).to_csv(outpath + '/2018-2019.csv', index = False)
        else:
            get_table(y).to_csv(outpath + '/' + str(y) + '.csv', index = False)
    return