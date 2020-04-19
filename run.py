#!/usr/bin/env python

import sys
import json
import shutil
import pandas as pd
import os
sys.path.append('src')
sys.path.append('src/data')
from etl import get_data

DATA_PARAMS = '/config/config.json'
TOP_PATH = os.environ['PWD']

def load_params(fp):
    with open(fp) as fh:
        param = json.load(fh)
    return param


def main(targets):
    
    if 'data' in targets:
        cfg = load_params(TOP_PATH + DATA_PARAMS)
        get_data(**cfg)

if __name__ == '__main__':
    targets = sys.argv[1:]
    main(targets)


    