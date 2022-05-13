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
VALIDATION_COLS = ['challange', 'budget']

##################################################
# MANUAL INPUT:  
#     For new fundings, add the references bellow
##################################################

# ADD PATH TO NEW FUND'S FILES
FUNDS_FILES = {      
    "f3": PATH+"data_files/Fund3 Voting results.xlsx",
    "f4": PATH+"data_files/Fund4 Voting results.xlsx",
    "f5": PATH+"data_files/Fund5 Voting results.xlsx",
    "f6": PATH+"data_files/Fund6 Voting results.xlsx",
    "f7": PATH+"data_files/Fund7 Voting results.xlsx",
    "f8": PATH+"data_files/Fund8 Voting results.xlsx"
}
# ADD MAPPING TO LOAD FUNCTION
MAP_LOAD_FNC = {      
    "f3": "load_f3",
    "f4": "load_f4",
    "f5": "load_f5",
    "f6": "load_f6",
    "f7": "load_f7",
    "f8": "load_f8"
}


##################
# ERROR MESSAGES #
##################
ERR_FNC_NOT_FOUND = "{} load function not found: please, provide a < data.datasets.load_{}(file_path) > function for loading the fund data -- make sure the function is properly specified on < data.datasets.MAP_LOAD_FNC >."
ERR_REF_NOT_FOUND = "Undefined Fund reference. Available fundings: {}.\n>> To add a new fund, please input the data file path on < data.datasets.FUNDS_FILES > and provide a proper loading function specified on < data.datasets.MAP_LOAD_FNC >."
ERR_VALID_NOT_FOUND = "{} validation table requires setup: no setup function provided. Please, provide a {} function with proper validation table formatting."

    
class CatalystData():
    def __init__(self, fund:str, file_path:str) -> None:
        self.fund = fund
        self.path = file_path
        self.data = None
        self.validation = None
        self.__read_file(file_path)
        
    def __read_file(self, file_path: str):
        '''
        All functions called here should return a dictionary {challange_name/sheet : pd.DataFrame}
        '''
        __supp_ext = ['.xlsx']
        if file_path[-5:] == '.xlsx':
            return self.__read_xlsx_file(file_path)
        else:
            raise TypeError('File extension not supported. Supported < CatalystData.__read_file() > extensions: {}'.format(__supp_ext))
        return

    def __read_xlsx_file(self, file_path: str) -> dict:
        '''
        return:  { sheet_name : pd.DataFrame(sheet) }
        '''
        xlsx_obj = pd.ExcelFile(file_path)
        dfs_dict = {}
        for sheet in xlsx_obj.sheet_names:
            dfs_dict[sheet] = xlsx_obj.parse(sheet_name=sheet)
        
        if 'validation' in dfs_dict.keys():
            df_valid = dfs_dict.pop('validation')
        elif 'Validation' in dfs_dict.keys():
            df_valid = dfs_dict.pop('Validation')
        else:
            df_valid = None
        
        self.data = dfs_dict
        self.validation = df_valid
        return


#################################
# PUBLIC FUNCTIONS:
#
#    DATA LOAD FUNCTIONS
#
# return:
#         CatalystData object
#################################

def get_catalyst_data(fund:str) -> CatalystData:
    '''
    This function maps the data load of all available data sets.
    '''
    if fund in FUNDS_FILES.keys():
        try: 
            return globals()[MAP_LOAD_FNC[fund]](fund=fund, file_path=FUNDS_FILES[fund])
        except: 
            raise TypeError(ERR_FNC_NOT_FOUND.format(fund, fund))   
    else: 
        raise TypeError(ERR_REF_NOT_FOUND.format(list(FUNDS_FILES.keys())))
    return

def load_f3(fund:str, file_path: str) -> CatalystData:
    print(load_f3)
    
    data = CatalystData(fund, file_path)
    data = __validation_setup(data)
    
    return data

def load_f4(fund:str, file_path: str) -> CatalystData:
    print(load_f4)
    
    data = CatalystData(fund, file_path)
    data = __validation_setup(data)
    
    return data

def load_f5(fund:str, file_path: str) -> CatalystData:
    print(load_f5)
    
    data = CatalystData(fund, file_path)
    data = __validation_setup(data)
    
    return data

def load_f6(fund:str, file_path: str) -> CatalystData:
    print(load_f6)
    
    data = CatalystData(fund, file_path)
    data = __validation_setup(data)
    
    return data

def load_f7(fund:str, file_path: str) -> CatalystData:
    print(load_f7)
    
    data = CatalystData(fund, file_path)
    data = __validation_setup(data)
    
    return data

def load_f8(fund:str, file_path: str) -> CatalystData:
    print(load_f8)
    
    data = CatalystData(fund, file_path)
    data = __validation_setup(data)
    
    return data


#################################
# PRIVATE FUNCTIONS: 
#
#    DF-VALIDATION FUNCTIONS
#
#################################

def __validation_setup(data: CatalystData) -> CatalystData:
    # print(__validation_setup)
    if isinstance(data.validation, pd.DataFrame):
        func = '__get_validation_{}'.format(data.fund)
        try: 
            data.validation = globals()[func](data.validation)
        except: 
            raise TypeError(ERR_VALID_NOT_FOUND.format(data.fund, func))
    return data

def __get_validation_f3(df:pd.DataFrame) -> pd.DataFrame:
    # print(__get_validation_f3)
    df.dropna(inplace=True)
    df = df.iloc[:-1].copy()
    df.reset_index(drop=True, inplace=True)
    df.columns = VALIDATION_COLS
    func_format = lambda s: s.split('(')[1].split(')')[0]
    df.loc[:,'challange'] = df['challange'].map(func_format)
    df['budget'] = df['budget'].astype(int)
    return df

def __get_validation_f4(df:pd.DataFrame) -> pd.DataFrame:
    # print(__get_validation_f4)
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.columns = VALIDATION_COLS
    func_format = lambda s: s.split('(')[1].split(')')[0]
    df.loc[0:6,'challange'] = list(map(func_format, df.loc[0:6,'challange']))
    df['budget'] = df['budget'].astype(int)
    return df

def __get_validation_f5(df:pd.DataFrame) -> pd.DataFrame:
    # print(__get_validation_f5)
    df.dropna(inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.columns = VALIDATION_COLS

    func_format = lambda s: s.split('(')[1].split(')')[0]
    df.loc[0:8,'challange'] = list(map(func_format, df.loc[0:8,'challange']))
    df['budget'] = df['budget'].astype(int)
    return df

def __get_validation_f6(df:pd.DataFrame) -> pd.DataFrame:
    # print(__get_validation_f6)
    df.dropna(how='all',inplace=True)
    df.drop(columns='Fund size:',inplace=True)
    df.reset_index(drop=True, inplace=True)
    df = df.iloc[:-2].copy()
    df.columns = VALIDATION_COLS
    df['budget'] = df['budget'].astype(int)
    return df

def __get_validation_f7(df:pd.DataFrame) -> pd.DataFrame:
    # print(__get_validation_f7)
    df.drop(columns=['Fund size:','Unnamed: 3'],inplace=True)
    df.columns = VALIDATION_COLS
    df.dropna(subset=['challange'],inplace=True)
    df.reset_index(drop=True, inplace=True)
    df['budget'] = df['budget'].astype(int)
    return df

def __get_validation_f8(df:pd.DataFrame) -> pd.DataFrame:
    # print(__get_validation_f8)
    df.drop(columns=['Fund size:'],inplace=True)
    df.columns = VALIDATION_COLS
    df.dropna(subset=['challange'],inplace=True)
    df.reset_index(drop=True, inplace=True)
    df['budget'] = df['budget'].astype(int)
    return df