'''
LOADING CATALYST FUND ASSESSMENTS DATA 

This file is dedicated to load the available Catalyst Assessments data sets 
into properly adjusted data structure to data analysis.
'''

import numpy as np
import pandas as pd

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
            self.__data = None
            # buildin methods
            self.__load_data()
            
    @property
    def assessments(self) -> pd.DataFrame:
        return self.__data['assessments'].copy()
    @property
    def cas(self) -> pd.DataFrame:
        return self.__data['CAs'].copy()
    @property
    def vcas(self) -> pd.DataFrame:
        return self.__data['vCAs'].copy()
    
    def get_ca_count_by_status(self) -> pd.DataFrame:
        df = self.assessments.groupby('CA')['QA_STATUS'].value_counts().unstack(fill_value=0)
        if df.shape[1] == 0: 
            print('!! No CatalystAssessments.assessments.QA_STATUS information.')
            return
        else: return df

    def get_ca_count_by_reason(self) -> pd.DataFrame:
        df = self.assessments.groupby('CA')['REASON'].value_counts().unstack(fill_value=0)
        if df.shape[1] == 0: 
            print('!! No CatalystAssessments.assessments.REASON information.')
            return
        else: return df

    def get_ca_count_by_class(self) -> pd.DataFrame:
        df = self.assessments.groupby('CA')['QA_CLASS'].value_counts().unstack(fill_value=0)
        if df.shape[1] == 0: 
            print('!! No CatalystAssessments.assessments.QA_CLASS information.')
            return
        else: return df
    
    def get_vca_count_by_class(self) -> pd.DataFrame:
        '''
        similar to get_ca_count_by_class
        return a dataframe containing the vCAs by their Reviews classification counts
        '''
        # create a key on __data to save this information, since it will have to be built from other documents in __load_data
        pass

    def __load_data(self) -> None:
        '''
        Load the following object properties 
            data = { assessments : pd.DataFrame,
                     CAs : pd.DataFrame,
                     vcas : pd.DataFrame,
                     ...
                    }
        '''
        __supp_ext = ['.xlsx']
        if self.path[-5:] == '.xlsx':
            self.__load_data_from_xlsx_files()
        else:
            raise TypeError('File extension not supported. Supported < CatalystData.__read_file() > extensions: {}'.format(__supp_ext))
    
    def __load_data_from_xlsx_files(self) -> None:
        xlsx_obj = pd.ExcelFile(self.path)

        data = {}
        # the following methods are mappings to fund-specific loader's functions
        data['assessments'] = self.__get_assessments(xlsx_obj)
        data['CAs'] = self.__get_comunity_advisors(df_assess=data['assessments'], xlsx_obj=xlsx_obj)
        data['vCAs'] = self.__get_veteran_comunity_advisors(xlsx_obj)


        self.__data = data.copy()
        return
    
    def __get_veteran_comunity_advisors(self, xlsx_obj:pd.ExcelFile) -> pd.DataFrame:
        '''
        This function returns a pd.DataFrame containing the relevant information 
        about all veteran comunity advisors participating in the Fund process
        '''
        func = 'get_vcas_{}'.format(self.fund)
        try: 
            return globals()[func](xlsx_obj=xlsx_obj)
        except: 
            raise TypeError(ERR_FNC_NOT_FOUND.format(self.fund, 'self.__get_veteran_comunity_advisors()', func))
    
    def __get_comunity_advisors(self, df_assess:pd.DataFrame, xlsx_obj:pd.ExcelFile) -> pd.DataFrame:
        '''
        This function returns a pd.DataFrame containing the relevant information 
        about all comunity advisors participating in the Fund process
        '''
        func = 'get_cas_{}'.format(self.fund)
        try: 
            return globals()[func](df_assess=df_assess, xlsx_obj=xlsx_obj)
        except: 
            raise TypeError(ERR_FNC_NOT_FOUND.format(self.fund, 'self.__get_comunity_advisors()', func))

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

    #-------------------
    # FORMAT FUNCTIONS
    #-------------------


if __name__ == "__main__":
    pass