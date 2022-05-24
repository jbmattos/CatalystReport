'''
LOADING CATALYST FUND ASSESSMENTS DATA 

This file is dedicated to load the available Catalyst Assessments data sets 
into properly adjusted data structure to data analysis.
'''

import numpy as np
import pandas as pd
import warnings

from data.loaders_assessments import *

# MESSAGES      
ERR_FNC_NOT_FOUND = "Error while loading {} results: {} processing.\nPlease, provide a proper < data.loaders_assessments.{}() > function for loading the expected results."
ERR_REF_NOT_FOUND = "Undefined Fund reference. Available fundings: {}.\n>> To add a new fund, please input the data file path on < data.datasets.FUNDS_FILES > and provide a proper loading function specified on < data.datasets.MAP_LOAD_FNC >."

class CatalystAssessments():

    FUNDS_FILES = available_data()

    def __init__(self, fund:str) -> None:
        if fund not in CatalystAssessments.FUNDS_FILES.keys():
            raise TypeError(ERR_REF_NOT_FOUND.format(list(CatalystAssessments.FUNDS_FILES.keys())))
        else: 
            self.fund = fund
            self.path = CatalystAssessments.FUNDS_FILES[fund]
            self.data = None
            ## default properties
            self.__is_default_filteredout = None
            self.__default_min_char_count = 150     # Text features with less than minimun character-count are automatically filtered out
            # buildin methods
            self.__load_data()
            # self.__pipeline()
            
        
    
    @property
    def assessments(self) -> pd.DataFrame:
        return self.data['assessments']

    def get_filtered_out(self, type: str='all') -> pd.DataFrame:
        '''
        Return the complete assessments that were filtered out.
        Types: default, ml_filter(?), ...
        !!!!!!!!!!!
        Change this function to select from pd the set of indexes present on all <self.__idx_default_filtered_out> keys
        '''
        ass = self.__default_filteredout_idx['default']
        return self.__df[ass]

    def get_full_assessments(self) -> pd.DataFrame:
        return self.__df

    ## REVIEW ABOVE
    ##############################################################

    def __load_data(self) -> None:
        '''
        Load the following object properties 
            data = { assessments : pd.DataFrame,
                     CAs : pd.DataFrame,
                     vcas : pd.DataFrame,
                     ...
                    }
            __is_default_filteredout
        '''
        __supp_ext = ['.xlsx']


        if self.path[-5:] == '.xlsx':
            xlsx_obj = self.__read_xlsx_file()
        else:
            raise TypeError('File extension not supported. Supported < CatalystData.__read_file() > extensions: {}'.format(__supp_ext))
        
        data = {}
        data['assessments'] = self.__get_assessments(xlsx_obj)
        # data['CAs'] = self.__get_comunity_advisors(xlsx_obj)
        # data['vCAs'] = self.__get_veteran_comunity_advisors(xlsx_obj)



        # Rows (assessments) to filter out
        ## The length of the assessment is insufficient to provide value, 
        ## for example less than 150 characters across the three criteria fields of the assessment. 
        ## These will be filtered. 

        # self.__is_default_filteredout = data['assessments'][CatalystAssessments.DEFAULT_TXT_FEAT].agg(''.join, axis=1).apply(lambda x: len(x)) < self.__default_min_char_count
        self.data = data
        return
    
    def __read_xlsx_file(self) -> dict:
        return pd.ExcelFile(self.path)
    
    def __get_veteran_comunity_advisors(self, xlsx_obj:pd.ExcelFile) -> pd.DataFrame:
        '''
        This function returns a pd.DataFrame containing the relevant information 
        about all veteran comunity advisors participating in the Fund process
        '''
        func = 'get_vcas_{}'.format(self.fund)
        try: 
            params = globals()[func]()
        except: 
            raise TypeError(ERR_FNC_NOT_FOUND.format(self.fund, 'self.__get_veteran_comunity_advisors()', func))
        
        data = xlsx_obj.parse(sheet_name=params['sheet'])
        return data
    
    def __get_comunity_advisors(self, xlsx_obj:pd.ExcelFile) -> pd.DataFrame:
        '''
        This function returns a pd.DataFrame containing the relevant information 
        about all comunity advisors participating in the Fund process
        '''
        func = 'get_cas_{}'.format(self.fund)
        try: 
            params = globals()[func]()
        except: 
            raise TypeError(ERR_FNC_NOT_FOUND.format(self.fund, 'self.__get_comunity_advisors()', func))
        
        data = xlsx_obj.parse(sheet_name=params['sheet'])
        return data

    def __get_assessments(self, xlsx_obj:pd.ExcelFile) -> pd.DataFrame:
        '''
        This function returns a pd.DataFrame containing the relevant information 
        about all Assessments in a Fund process
        '''
        func = 'get_assessments_{}'.format(self.fund)
        try: 
            return globals()[func](xlsx_obj=xlsx_obj)
        except: 
            raise TypeError(ERR_FNC_NOT_FOUND.format(self.fund, 'self.__get_assessments()', func))

    def __pipeline(self) -> None:
        '''
        This function loads the Catalyst results from data source
        and returns a CatalystData object with relevant data preprocessed

        The calls from this function manipulate CatalystData objects while performing data preprocessing
        '''
        return 


    #-------------------
    # FORMAT FUNCTIONS
    #-------------------


if __name__ == "__main__":
    pass