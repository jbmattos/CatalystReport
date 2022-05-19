'''
LOADING CATALYST FUND RESULTS DATA

This file is dedicated to load the available CatalystReport data sets 
into properly adjusted data structure to data analysis.

- The public functions output a processed CatalystData object.
- The pipeline (protected) functions are mappers to fund-specific functions responsible for properly fomatting the data from different funds. 
- The fund-specific functions implement fund-personalised processing and perform default setup functions
- The __default functions modify and return processed CatalystData objects

To add new Fund's Results, the following fund-specific functions should be provided:
- __get_validation_fN
- __input_budget_fN
- __process_fN
for N standing for the integer reference to the fund.
Templates for the above fund-specific functions are provided throughout this file. 

This files contains a collection of public and private functions
    v.0 - which offer some functionality in loading the vCA's assessments databases.
'''
import numpy as np
import pandas as pd
import warnings

from data.loaders_votingresults import *


# MESSAGES      
ERR_FNC_NOT_FOUND = "Error while loading {} results: {} processing.\nPlease, provide a proper < data.datasets.{}() > function for providing the expected results."
ERR_REF_NOT_FOUND = "Undefined Fund reference. Available fundings: {}.\n>> To add a new fund, please input the data file path on < data.datasets.FUNDS_FILES > and provide a proper loading function specified on < data.datasets.MAP_LOAD_FNC >."
WAR_BUDGET_NOT_FOUND = '< {}-{} > Budget not found. Please, make sure the challenge name from Catalyst.data matches the challenge names in Catalyst.validation.'

# GLOBAL VAR
VALIDATION_COLS = ['challenge', 'budget']
DEFAULT_COLS = ['challenge', 'Budget', 'Proposal', 'SCORE', 'YES', 'NO', 'Unique Yes', 'Unique No', 'Result','STATUS','REQUESTED $', 'REQUESTED %']
INT_COLS = ['YES', 'NO', 'Unique Yes', 'Unique No', 'Result', 'REQUESTED $']
FUNDS_FILES = available_data()


class CatalystVotingResults():
    def __init__(self, fund:str) -> None:
        if fund not in FUNDS_FILES.keys():
            raise TypeError(ERR_REF_NOT_FOUND.format(list(FUNDS_FILES.keys())))
        else: 
            self.fund = fund
            self.path = FUNDS_FILES[fund]
            self.data = None
            self.results = None
            self.validation = None
            self.withdrawals = None
            self._DEFAULT_COLS = DEFAULT_COLS
            self.__load_data()
            self.__pipeline()
        
    def __load_data(self) -> None:
        '''
        All __read_ functions called here should return a tuple (data, valid, withd) for
            data = { sheet/challenge names : pd.DataFrame }
            valid = pd.DataFrame
            withd = pd.DataFrame
        '''
        __supp_ext = ['.xlsx']        

        if self.path[-5:] == '.xlsx':
            data, valid, withd = self.__read_xlsx_file()
        else:
            raise TypeError('File extension not supported. Supported < CatalystData.__read_file() > extensions: {}'.format(__supp_ext))
        
        self.data = data
        self.validation = valid
        self.withdrawals = withd
        return

    def __read_xlsx_file(self) -> dict:
        '''
        Return 
            self.data = None
            self.validation = None
            self.withdrawals = None
        '''
        xlsx_obj = pd.ExcelFile(self.path)
        data = {}
        for sheet in xlsx_obj.sheet_names:
            data[sheet] = xlsx_obj.parse(sheet_name=sheet)
        
        if 'validation' in data.keys():
            df_valid = data.pop('validation')
        elif 'Validation' in data.keys():
            df_valid = data.pop('Validation')
        else:
            df_valid = None
        
        if 'withdrawals' in data.keys():
            df_withd = data.pop('withdrawals')
        elif 'Withdrawals' in data.keys():
            df_withd = data.pop('Withdrawals')
        elif 'withdrawal' in data.keys():
            df_withd = data.pop('withdrawal')
        elif 'Withdrawal' in data.keys():
            df_withd = data.pop('Withdrawal')
        else:
            df_withd = None

        if 'template' in data.keys():
            del data['template']
        elif 'Template' in data.keys():
            del data['Template']
        
        return (data, df_valid, df_withd)

    def __pipeline(self) -> None:
        '''
        This function loads the Catalyst results from data source
        and returns a CatalystData object with relevant data preprocessed

        The calls from this function manipulate CatalystData objects while performing data preprocessing
        '''
        
        self.__validation_setup()
        self.__budget_setup()
        self.__challenge_data_processing()
        return 

    #################################
    # PIPELINE FUNCTIONS
    #
    # explanation
    #################################

    def __validation_setup(self) -> None:
        '''
        This function generates a formatted Validation DataFrame
        
        modifies: CatalystData.validation
        '''
        if isinstance(self.validation, pd.DataFrame):
            func = 'validation_setup_{}'.format(self.fund)
            try: 
                df = globals()[func](self.validation)
            except: 
                raise TypeError(ERR_FNC_NOT_FOUND.format(self.fund, '__validation_setup(data: CatalystData) -> CatalystData', func))

            df.columns = VALIDATION_COLS
            df.dropna(subset=['challenge'],inplace=True)
            df.reset_index(drop=True, inplace=True)
            df['budget'] = df['budget'].astype(int)
            self.validation = df
        return

    def __budget_setup(self) -> None:
        '''
        This function inputs Budget value and Challenge Name 
        to every dataframe of each challenge on the fund

        modifies: CatalystData.data[fund] : DataFrame
        '''
        func = 'get_budget_{}'.format(self.fund)
        try: 
            params = globals()[func]()
        except: 
            raise TypeError(ERR_FNC_NOT_FOUND.format(self.fund, '__input_budget(data: CatalystData) -> CatalystData', func))
        replace_validation = params['replace_validation']
        input_bud = params['input_bud']

        dfs = self.data
        for challenge in dfs.keys():
            if challenge in input_bud:
                bud = input_bud[challenge]
            else:
                if challenge in replace_validation: ch = replace_validation[challenge]
                else: ch = challenge
                try:
                    bud = self.validation.loc[self.validation.challenge==ch]['budget'].item()
                except:
                    warnings.warn(WAR_BUDGET_NOT_FOUND.format(self.fund, challenge))
                    bud = np.nan
            dfs[challenge]['challenge'] = challenge
            dfs[challenge]['Budget'] = bud
        return 

    def __challenge_data_processing(self) -> None:
        '''
        This function preprocess the DataFrames of each challenge in the fund

        modifies: CatalystData.data[fund] : DataFrame
                  CatalystData.results
        '''
        func = 'get_process_{}'.format(self.fund)
        try: 
            params = globals()[func]()
        except: 
            raise TypeError(ERR_FNC_NOT_FOUND.format(data.fund, '__challenge_data_processing(data: CatalystData) -> CatalystData', func))
        rename_default_cols = params['rename_default_cols']

        to_concat = []
        for challenge, df in self.data.items():
            # rename columns 
            df.rename(columns=rename_default_cols, inplace=True)
            
            # adjust type int
            df = self.__format_int(df)
            
            # format default features
            df['REQUESTED %'] = 100*df['REQUESTED $']/df['Budget']
            df = self.__format_status(df)

            self.data[challenge] = df.copy()
            default_cols = list(set(df.columns).intersection(DEFAULT_COLS))
            to_concat.append(df[default_cols].copy())
        
        # concatenate all challenges' default data 
        self.results = pd.concat(to_concat, axis='index')
        self.results.reset_index(drop=True, inplace=True)

        # rearrange columns
        cols = [c for c in DEFAULT_COLS if c in self.results.columns]
        self.results = self.results[cols] 
        return

    #################################
    # PIPELINE FUNCTIONS
    #
    # explanation
    #################################

    def __format_int(self, df: pd.DataFrame) -> pd.DataFrame:
        to_int = list(set(df.columns).intersection(INT_COLS))
        df[to_int] = df[to_int].astype(int)
        return df

    def __format_status(self, df: pd.DataFrame) -> pd.DataFrame:
        def napp_status_mat(df):
            return (df['Meets approval threshold']=='NO')
        def napp_status_yn(df):
            return (df['YES'] < 1.15*df['NO'])

        if 'Meets approval threshold' in df.columns:
            df.loc[napp_status_mat(df),'STATUS'] = 'NOT APPROVED'
        elif ('YES' in df.columns) and ('NO' in df.columns):
            df.loc[napp_status_yn(df),'STATUS'] = 'NOT APPROVED'
        else:
            warnings.warn('Status NOT_APPROVED: Not enought data for defining such status. Kept original STATUS.')
        return df

    def __format_currency_cols(self, df: pd.DataFrame, cols_to_format=[]) -> pd.DataFrame:
        for feat in cols_to_format:
            df[feat] = df.loc[:,feat].str.replace('₳', '')
            df[feat] = df.loc[:,feat].str.replace(',', '').astype(int)
        return df

    def __format_requested_col(self, df: pd.DataFrame) -> pd.DataFrame:
        df['REQUESTED $'] = df.loc[:,'REQUESTED $'].str.replace('$', '')
        df['REQUESTED $'] = df.loc[:,'REQUESTED $'].str.replace(',', '').astype(float).astype(int)
        return df