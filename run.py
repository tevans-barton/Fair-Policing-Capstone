#!/usr/bin/env python

import sys
import json
import shutil
import pandas as pd
import os
sys.path.append('src')
sys.path.append('src/data')
from etl import get_data
import cleaning

DATA_PARAMS = '/config/config.json'
TOP_PATH = os.environ['PWD']

def load_params(fp):
    with open(fp) as fh:
        param = json.load(fh)
    return param


def main(targets):

    if 'clean' in targets:
        shutil.rmtree('data/raw',ignore_errors=True)
        shutil.rmtree('data/out',ignore_errors=True)
        shutil.rmtree('data/test',ignore_errors=True)

    if 'data' in targets:
        cfg = load_params(TOP_PATH + DATA_PARAMS)
        get_data(**cfg)

    if 'transform' in targets:
        if not os.path.exists(TOP_PATH + '/data/cleaned'):
            os.makedirs(TOP_PATH + '/data/cleaned')
        for filename in os.listdir(TOP_PATH + '/data/raw'):
            if 'STOPS' in filename:
                if '2018' in filename:
                    temp_df = cleaning.clean_2018_2019(TOP_PATH + '/data/raw/' + str(filename))
                else:
                    year = int(filename[6:10])
                    temp_df = cleaning.clean_2014_2017(TOP_PATH + '/data/raw/' + str(filename))
    return


        


if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)


    