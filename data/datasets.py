'''
LOADING DATABASES 

This file is dedicated to load the available CatalystReport data sets 
into properly adjusted pandas.DataFrame.

This files contains a collection of public and private functions
    v.0 - which offer some functionality in loading the vCA's assessments databases.
'''
import numpy as np
import pandas as pd
import os

PATH = os.path.dirname(__file__)+'/'

# DATA FILES
# if data files increase, implement better file-acessing functionality

DATA_FILES = {      
    "vca_aggregated-f7": PATH+"assessments_data/vca_f7-vca_aggregated.csv"
}


########################
# PUBLIC FUNCTIONS
########################

def read_data(file_name: str, fund:int) -> pd.DataFrame:
    f = file_name+'-f{}'.format(fund)
    if f in DATA_FILES.keys():
        return __read_file(file_path=DATA_FILES[f])
    else: raise TypeError("Undefined data file reference. Available data sets: {}".format(list(DATA_FILES.keys()))) 

########################
# PRIVATE FUNCTIONS
########################

# ---------------------------------------------
# CALL FROM PUBLIC

def __read_file(file_path: str) -> pd.DataFrame:
    '''
    This function maps the data load of all available data sets.
    '''
    if "vca_aggregated" in file_path:
        return __read_file_vca_aggregated(file_path)

# ---------------------------------------------
# CALL FROM PRIVATE

# >> FUNCTIONS: DATA READ/PROCESS
# Input: file_path str
# Output: pd.DataFrame

def __read_file_vca_aggregated(file_path: str) -> pd.DataFrame:

    df = pd.read_csv(file_path)

    # format: boolean features
    bool_feat = ['Proposer Mark','Result Excellent','Result Good','Result Filtered Out']
    df[bool_feat] = __x_to_bool(df[bool_feat])
    
    return df

# ---------------------------------------------
# COMPUTED FUNCTIONS

def __x_to_bool(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Transforms binary features assigned by [xX] into boolen type
        'xX' : True
        np.nan : False

    Warning: 
        1. Assure proper input/output formats (types)
    '''
    return df.replace({'[xX]':True, np.nan: False}, regex=True)
