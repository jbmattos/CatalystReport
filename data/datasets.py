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
import os
import warnings

PATH = os.path.dirname(__file__)+'/'
VALIDATION_COLS = ['challenge', 'budget']
DEFAULT_COLS = ['challenge', 'Budget', 'Proposal', 'SCORE', 'YES', 'NO', 'Unique Yes', 'Unique No', 'Result','STATUS','REQUESTED $', 'REQUESTED %']
INT_COLS = ['YES', 'NO', 'Unique Yes', 'Unique No', 'Result', 'REQUESTED $']

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
def available_data() -> dict:
    return FUNDS_FILES

##################
# MESSAGES       #
##################
ERR_FNC_NOT_FOUND = "Error while loading {} results: {} processing.\nPlease, provide a proper < data.datasets.{}() > function for providing the expected results."
ERR_REF_NOT_FOUND = "Undefined Fund reference. Available fundings: {}.\n>> To add a new fund, please input the data file path on < data.datasets.FUNDS_FILES > and provide a proper loading function specified on < data.datasets.MAP_LOAD_FNC >."
WAR_BUDGET_NOT_FOUND = '< {}-{} > Budget not found. Please, make sure the challenge name from Catalyst.data matches the challenge names in Catalyst.validation.'


#######################
# CATALYST DATA CLASS #
#######################
class CatalystData():
    def __init__(self, fund:str, file_path:str) -> None:
        self.fund = fund
        self.path = file_path
        self.data = None
        self.results = None
        self.validation = None
        self.withdrawals = None
        self._defaults_cols = DEFAULT_COLS
        self.__read_file(file_path)
        
    def __read_file(self, file_path: str):
        '''
        All functions called here should return a dictionary {challenge_name/sheet : pd.DataFrame}
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
        
        if 'withdrawals' in dfs_dict.keys():
            df_withd = dfs_dict.pop('withdrawals')
        elif 'Withdrawals' in dfs_dict.keys():
            df_withd = dfs_dict.pop('Withdrawals')
        elif 'withdrawal' in dfs_dict.keys():
            df_withd = dfs_dict.pop('withdrawal')
        elif 'Withdrawal' in dfs_dict.keys():
            df_withd = dfs_dict.pop('Withdrawal')
        else:
            df_withd = None

        if 'template' in dfs_dict.keys():
            del dfs_dict['template']
        elif 'Template' in dfs_dict.keys():
            del dfs_dict['Template']
        
        self.data = dfs_dict
        self.validation = df_valid
        self.withdrawals = df_withd
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
    This function calls load_fund considering data from default datapaths
    '''
    if fund in FUNDS_FILES.keys():
        return load_fund(fund=fund, file_path=FUNDS_FILES[fund])
    else: 
        raise TypeError(ERR_REF_NOT_FOUND.format(list(FUNDS_FILES.keys())))

def load_fund(fund:str, file_path: str) -> CatalystData:
    '''
    This function loads the Catalyst results from data source
    and returns a CatalystData object with relevant data preprocessed

    The calls from this function manipulate CatalystData objects while performing data preprocessing
    '''
    
    data = CatalystData(fund, file_path)
    data = _validation_setup(data)
    data = _input_budget(data)
    data = _challenge_data_processing(data)
    
    return data

#################################
# PIPELINE FUNCTIONS
#
# explanation
#################################

def _validation_setup(data: CatalystData) -> CatalystData:
    '''
    This function generates a formatted Validation DataFrame
    
    modifies: CatalystData.validation
    '''
    if isinstance(data.validation, pd.DataFrame):
        func = '__get_validation_{}'.format(data.fund)
        try: 
            return globals()[func](data)
        except: 
            raise TypeError(ERR_FNC_NOT_FOUND.format(data.fund, '__validation_setup(data: CatalystData) -> CatalystData', func))

def _input_budget(data: CatalystData) -> CatalystData:
    '''
    This function inputs Budget value and Challenge Name 
    to every dataframe of each challenge on the fund

    modifies: CatalystData.data[fund] : DataFrame
    '''
    func = '__input_budget_{}'.format(data.fund)
    try: 
        return globals()[func](data)
    except: 
        raise TypeError(ERR_FNC_NOT_FOUND.format(data.fund, '__input_budget(data: CatalystData) -> CatalystData', func))

def _challenge_data_processing(data: CatalystData) -> CatalystData:
    '''
    This function preprocess the DataFrames of each challenge in the fund

    modifies: CatalystData.data[fund] : DataFrame
              CatalystData.results
    '''
    func = '__process_{}'.format(data.fund)
    try: 
        return globals()[func](data)
    except: 
        raise TypeError(ERR_FNC_NOT_FOUND.format(data.fund, '__challenge_data_processing(data: CatalystData) -> CatalystData', func))


#################################
# FUND-SPECIFIC FUNCTIONS
################################

# ----------------------------------------
# DF-VALIDATION FUNCTIONS
#
# explanation
#
# TEMPLATE:
#
# def __get_validation_fN(df:pd.DataFrame) -> pd.DataFrame:
#     df = data.validation
#
#     # Drop unecessary rows (NaN values will be handle by default)
#     # (add optional code here)

#     # Drop additional columns. Only two columns should remain:
#         # The first containing the Challenge's names
#         # The second containing the Challenge's budget
#     # (add optional code here)
#
#     # Format Challenge's names
#     # (add optional code here)
#
#     return __default_setup(df)
# ----------------------------------------

def __get_validation_f3(data: CatalystData) -> CatalystData:
    df = data.validation.copy()

    # Drop unecessary rows (NaN values will be handle by default)
    df = df.iloc[:-1].copy()

    # Format Challenge's names
    func_format = lambda s: s.split('(')[1].split(')')[0] if isinstance(s, str) else s
    df.iloc[:,0] = df.iloc[:,0].map(func_format)
    
    return __default_setup_validation(data, df)

def __get_validation_f4(data: CatalystData) -> CatalystData:
    df = data.validation.copy()
    
    # Format Challenge's names
    func_format = lambda s: s.split('(')[1].split(')')[0] if isinstance(s, str) else s
    df.iloc[9:16,0] = df.iloc[9:16,0].map(func_format)

    return __default_setup_validation(data, df)

def __get_validation_f5(data: CatalystData) -> CatalystData:
    df = data.validation.copy()
    
    # Format Challenge's names
    func_format = lambda s: s.split('(')[1].split(')')[0] if isinstance(s, str) else s
    df.iloc[9:18,0] = df.iloc[9:18,0].map(func_format)
    
    return __default_setup_validation(data, df)

def __get_validation_f6(data: CatalystData) -> CatalystData:
    df = data.validation.copy()
    
    # Drop unecessary rows (NaN values will be handle by default)
    df = df.iloc[:-2].copy()

    # Drop additional columns. Only two columns should remain:
        # The first containing the Challenge's names
        # The second containing the Challenge's budget
    df.drop(columns='Fund size:', inplace=True)

    return __default_setup_validation(data, df)

def __get_validation_f7(data: CatalystData) -> CatalystData:
    df = data.validation.copy()
    
    # Drop additional columns. Only two columns should remain:
        # The first containing the Challenge's names
        # The second containing the Challenge's budget
    df.drop(columns=['Fund size:','Unnamed: 3'],inplace=True)

    return __default_setup_validation(data, df)

def __get_validation_f8(data: CatalystData) -> CatalystData:
    df = data.validation.copy()
        
    # Drop additional columns. Only two columns should remain:
        # The first containing the Challenge's names
        # The second containing the Challenge's budget
    df.drop(columns=['Fund size:'],inplace=True)

    return __default_setup_validation(data, df)


def __default_setup_validation(data: CatalystData, df:pd.DataFrame) -> CatalystData:
    '''
    Modifies CatalystData.validation
    '''
    df.columns = VALIDATION_COLS
    df.dropna(subset=['challenge'],inplace=True)
    df.reset_index(drop=True, inplace=True)
    df['budget'] = df['budget'].astype(int)
    data.validation = df
    return data


# ----------------------------------------
#    BUDGET EXTRACTION FUNCTIONS
#
# explanation
#
#  TEMPLATE:
#
# def __input_budget_fN(data: dict) -> dict:
#     # In case of between the challenge's names in CatalystData.data.keys() and CatalystData.validation.columns
#     # Provide a dictionary {CatalystData.data name : CatalystData.validation name}
#     
#     # In case of missing challenge budget, the value can be found on Catalyst website https://cardanocataly.st/voter-tool/#/
#     # Provide a dictionary {CatalystData.data name : budget (int)}
#
# return __default_input_budget(data, fund='fN', replace_validation=replace_dict)
# ----------------------------------------

def __input_budget_f3(data: CatalystData) -> CatalystData:
    return __default_input_budget(data)

def __input_budget_f4(data: CatalystData) -> CatalystData:
    replace_dict = {
        'DApp&Integrations': 'DApps&Integrations ',
        'Distributed decision making': 'Distributed Decision Making',
        'Sponsored by leftovers': 'Leftovers from regular challenges'
    }
    return __default_input_budget(data, replace_validation=replace_dict)

def __input_budget_f5(data: CatalystData) -> CatalystData:
    replace_dict = {
        'DApp&Integrations': 'DApps&Integrations ',
        'Distributed decision making': 'Distributed Decision Making',
        'Grow Africa, Grow Cardano wv': 'Grow Africa, Grow Cardano',
        'Scale-UP Cardanos DeFi Ecosyste': "Scale-UP Cardano's DeFi Ecosystem",
        'Fund7 Challenge Setting wv': 'Fund7 Challenge Setting',
        'Sponsored by leftovers': 'Leftovers from regular challenges'
    }
    return __default_input_budget(data, replace_validation=replace_dict)

def __input_budget_f6(data: CatalystData) -> CatalystData:
    replace_dict = {
        'Metadata': 'Metadata challenge',
        'Scale-UP Cardano’s DeFi Ecosyst': "Scale-UP Cardano's DeFi Ecosystem",
        'DeFi and Microlending for Afric': 'DeFi and Microlending for Africa',
        'Partnerships for Global Adoptio': 'Partnerships for Global Adoption',
        'Atala PRISM DID Mass-Scale Adop': 'Atala PRISM DID Mass-Scale Adoption',
        'Disaster When all is at stake': 'Disaster: When all is at stake',
        'Scale-UP Cardano’s Community Hu': "Scale-UP Cardano’s Community Hubs",
        'Fund7 challenge setting': 'Fund7 Challenge Setting',
        'Sponsored by leftovers': 'Leftovers from regular challenges'
    }
    return __default_input_budget(data, replace_validation=replace_dict)

def __input_budget_f7(data: CatalystData) -> CatalystData:
    replace_dict = {
        'A.I. & SingularityNet a $5T mar': 'A.I. & SingularityNet a $5T market',
        'Boosting Cardanos DeFi': "Boosting Cardano's DeFi",
        'Catalyst - Rapid Funding Mechan': "Catalyst - Rapid Funding Mechanisms",
        'Catalyst Natives COTI Pay with ': 'Catalyst Natives COTI: Pay with ADA Plug-in',
        'Connecting Japan日本 Community': "Connecting Japan/日本 Community",
        'DAOs ❤ Cardano': "DAOs <3 Cardano",
        'Disarm cyber disinformation att': 'Disarm cyber disinformation attacks',
        'Global Sustainable Indep. SPOs': "Global Sustainable Indep. SPO's",
        'Grow Latin America, Grow Cardan': 'Grow Latin America, Grow Cardano',
        'Lobbying for favorable legislat': 'Lobbying for favorable legislation',
        'MiniLow-Budget Dapps & Integrat': 'Mini/Low-Budget Dapps &Integrations',
        'Scale-UP Cardanos Community Hub': "Scale-UP Cardano's Community Hubs",
        'Seeding Cardanos Grassroots DeF': "Seeding Cardano's Grassroots DeFi",
        'Fund8 challenge setting': 'Fund8 Challenge Setting',
        'Sponsored by leftovers': 'Sum of the leftovers'
    }
    input_bud = {
        'Accelerate Decentralized Identi': 425000,
    }
    return __default_input_budget(data, replace_validation=replace_dict, input_bud=input_bud)

def __input_budget_f8(data: CatalystData) -> CatalystData:
    replace_dict = {
        'Accelerate Decentralized Identi': 'Accelerate Decentralized Identity',
        'Film + Media (FAM) creatives un': 'Film + Media (FAM) creatives unite!',
        'Lobbying for favorable legislat': 'Lobbying for favorable legislation',
        'Open Source Development Ecosyst': 'Open Source Development Ecosystem',
        'Open Standards & Interoperabili': 'Open Standards & Interoperability',
        'Scale-UP Cardanos Community Hub': "Scale-UP Cardano's Community Hubs",
        'The Great Migration (from Ether': 'The Great Migration (from Ethereum)',
        'Funded by leftovers': 'Sum of the leftovers'
    }
    return __default_input_budget(data, replace_validation=replace_dict)

def __default_input_budget(data: CatalystData, replace_validation: dict={}, input_bud:dict={}) -> CatalystData:
    dfs = data.data
    for challenge in dfs.keys():
        if challenge in input_bud:
            bud = input_bud[challenge]
        else:
            if challenge in replace_validation: ch = replace_validation[challenge]
            else: ch = challenge
            try:
                bud = data.validation.loc[data.validation.challenge==ch]['budget'].item()
            except:
                warnings.warn(WAR_BUDGET_NOT_FOUND.format(data.fund, challenge))
                bud = np.nan
        dfs[challenge]['challenge'] = challenge
        dfs[challenge]['Budget'] = bud
    return data 


# ----------------------------------------
#    FEATURE PROCESSING FUNCTIONS
#
# explanation
# Additional __format functions are provided for further processing, if necessary
#
#  TEMPLATE:
#
# DEFAULT_COLS = ['challenge', 'Budget', 'Proposal', 'SCORE', 'YES', 'NO', 'Unique Yes', 'Unique No', 'Result','STATUS','REQUESTED $', 'REQUESTED %']
# def __process_f4(data: CatalystData) -> CatalystData:
#   # In case a DEFAULT_COLS has a different name from the ones defined in the global variable
#   #    provide a dictionary {old_name : default_name} for renaming the pd.DataFrame columns 
#     rename = {
#         'Overall score': 'SCORE'
#     }
#     return __default_process(data, rename_default_cols=rename)
# ----------------------------------------

def __process_f3(data: CatalystData) -> CatalystData:
    return __default_process(data)

def __process_f4(data: CatalystData) -> CatalystData:
    # In case a DEFAULT_COLS has a different name from the ones defined in the global variable
    #    provide a dictionary {old_name : default_name} for renaming the pd.DataFrame columns 
    rename = {
        'Overall score': 'SCORE'
    }
    return __default_process(data, rename_default_cols=rename)

def __process_f5(data: CatalystData) -> CatalystData:
    rename = {
        'Overall score': 'SCORE'
    }
    return __default_process(data, rename_default_cols=rename)

def __process_f6(data: CatalystData) -> CatalystData:
    rename = {
        'Overall score': 'SCORE'
    }
    return __default_process(data, rename_default_cols=rename)

def __process_f7(data: CatalystData) -> CatalystData:
    rename = {
        'Overall score': 'SCORE'
    }
    return __default_process(data, rename_default_cols=rename)

def __process_f8(data: CatalystData) -> CatalystData:
    rename = {
        'Overall score': 'SCORE'
    }
    return __default_process(data, rename_default_cols=rename)

def __default_process(data: CatalystData, rename_default_cols:dict={}) -> CatalystData:
    '''
    modifies: CatalystData.data[fund] : DataFrame
              CatalystData.results
    '''
    to_concat = []
    for challenge, df in data.data.items():
        # rename columns 
        df.rename(columns=rename_default_cols, inplace=True)
        
        # adjust type int
        df = __format_int(df)
        
        # format default features
        df['REQUESTED %'] = 100*df['REQUESTED $']/df['Budget']
        df = __format_status(df)

        data.data[challenge] = df.copy()
        default_cols = list(set(df.columns).intersection(DEFAULT_COLS))
        to_concat.append(df[default_cols].copy())
    
    # concatenate all challenges' default data 
    data.results = pd.concat(to_concat, axis='index')
    data.results.reset_index(drop=True, inplace=True)

    # rearrange columns
    cols = [c for c in DEFAULT_COLS if c in data.results.columns]
    data.results = data.results[cols] 
    return data 

def __format_int(df: pd.DataFrame) -> pd.DataFrame:
    to_int = list(set(df.columns).intersection(INT_COLS))
    df[to_int] = df[to_int].astype(int)
    return df

def __format_status(df: pd.DataFrame) -> pd.DataFrame:
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

def __format_currency_cols(df: pd.DataFrame, cols_to_format=[]) -> pd.DataFrame:
    for feat in cols_to_format:
        df[feat] = df.loc[:,feat].str.replace('₳', '')
        df[feat] = df.loc[:,feat].str.replace(',', '').astype(int)
    return df

def __format_requested_col(df: pd.DataFrame) -> pd.DataFrame:
    df['REQUESTED $'] = df.loc[:,'REQUESTED $'].str.replace('$', '')
    df['REQUESTED $'] = df.loc[:,'REQUESTED $'].str.replace(',', '').astype(float).astype(int)
    return df