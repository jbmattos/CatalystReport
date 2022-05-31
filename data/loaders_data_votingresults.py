'''
DATA LOADERS FOR VOTING-RESULTS DATA

This file provides fund-specific functions to properly load `datafiles_votingresults` files
into `catalyst_data_votingresults.CatalystVotingResults` class format.

For adding new Fund data to the repository:
Follow the comments provided in this file to implement the necessary new-fund specific functions.
'''

import pandas as pd
import os

PATH = os.path.dirname(__file__)+'/datafiles_votingresults/'

# ---------------------------------------------------------------
# MANUAL INPUT: For new fundings, add the file reference bellow
# ---------------------------------------------------------------
FUNDS_FILES = {      
    "f3": PATH+"Fund3 Voting results.xlsx",
    "f4": PATH+"Fund4 Voting results.xlsx",
    "f5": PATH+"Fund5 Voting results.xlsx",
    "f6": PATH+"Fund6 Voting results.xlsx",
    "f7": PATH+"Fund7 Voting results.xlsx",
    "f8": PATH+"Fund8 Voting results.xlsx"
}
def available_data() -> dict:
    return FUNDS_FILES


##################################################
# FUNCTION GROUP: 
#   VALIDATION SETUP
#
# EXPLANATION:
#   This group of functions provide the necessary preprocessing 
#   to load the CatalystVotingResults validation table. 
# 
# ADD FUND:
#   To add new Fund, copy, paste and uncomment the following template.
#   !! Important: 
#       - The {N} in the function's name should be replaced with the int-referece to the new Fund
#       - The code lines should be kept or similar formatting should be provided.
#
# TEMPLATE:
#-----------------------------------------
# def validation_setup_fN(df:pd.DataFrame) -> pd.DataFrame:
#
#     # Drop unecessary rows on Challenge's columns (NaN values will be handle by default)
#     # (add optional code here)
#
#     # Drop additional columns. Only two columns should remain:
#         # The first containing the Challenge's names
#         # The second containing the Challenge's budget
#     # (add optional code here)
#
#     # Format Challenge's names
#     # (add optional code here)
#
#     return df.copy()
#-------------------------------------------
##################################################


def validation_setup_f3(df:pd.DataFrame) -> pd.DataFrame:
    # Drop unecessary rows (NaN values will be handle by default)
    df = df.iloc[:-1].copy()

    # Format Challenge's names
    func_format = lambda s: s.split('(')[1].split(')')[0] if isinstance(s, str) else s
    df.iloc[:,0] = df.iloc[:,0].map(func_format)
    
    return df.copy()

def validation_setup_f4(df:pd.DataFrame) -> pd.DataFrame:
    # Format Challenge's names
    func_format = lambda s: s.split('(')[1].split(')')[0] if isinstance(s, str) else s
    df.iloc[9:16,0] = df.iloc[9:16,0].map(func_format)

    return df.copy()

def validation_setup_f5(df:pd.DataFrame) -> pd.DataFrame:
    # Format Challenge's names
    func_format = lambda s: s.split('(')[1].split(')')[0] if isinstance(s, str) else s
    df.iloc[9:18,0] = df.iloc[9:18,0].map(func_format)
    
    return df.copy()

def validation_setup_f6(df:pd.DataFrame) -> pd.DataFrame:
    # Drop unecessary rows (NaN values will be handle by default)
    df = df.iloc[:-2].copy()

    # Drop additional columns.
    df.drop(columns='Fund size:', inplace=True)

    return df.copy()

def validation_setup_f7(df:pd.DataFrame) -> pd.DataFrame:
    # Drop additional columns.
    df.drop(columns=['Fund size:','Unnamed: 3'],inplace=True)
    
    return df.copy()

def validation_setup_f8(df:pd.DataFrame) -> pd.DataFrame:
    # Drop additional columns.
    df.drop(columns=['Fund size:'],inplace=True)
    
    return df.copy()


##################################################
# FUNCTION GROUP: 
#   BUDGET SETUP
#
# EXPLANATION:
#   This group of functions return a dictionary containing the parameters
#   to be used in the CatalystVotingResults.__pipeline processing method
# 
# ADD FUND:
#   To add new Fund, copy, paste and uncomment the following template.
#   !! Important: 
#       - The {N} in the function's name should be replaced with the int-referece to the new Fund
#       - The code lines should be kept or similar formatting should be provided.
#
# TEMPLATE:
#-----------------------------------------
# def input_budget_fN() -> dict:
#     # In case of differences between the challenge's names in the xlsx sheets and validation table
#     # Provide a dictionary {Sheet name : Validation name}
#     replace_validation = {}
#
#     # In case of missing challenge budget on Validation table, the value can be found on Catalyst website https://cardanocataly.st/voter-tool/#/
#     # Provide a dictionary {Challenge Sheet name : budget (int)}
#     input_bud = {}  
#     return {'replace_validation':replace_validation, 'input_bud':input_bud}
# ----------------------------------------
##################################################

def get_budget_f3() -> dict:
    replace_validation = {}
    input_bud = {}  
    return {'replace_validation':replace_validation, 'input_bud':input_bud}

def get_budget_f4() -> dict:
    replace_validation = {
        'DApp&Integrations': 'DApps&Integrations ',
        'Distributed decision making': 'Distributed Decision Making',
        'Sponsored by leftovers': 'Leftovers from regular challenges'
    }
    input_bud = {}  
    return {'replace_validation':replace_validation, 'input_bud':input_bud}

def get_budget_f5() -> dict:
    replace_validation = {
        'DApp&Integrations': 'DApps&Integrations ',
        'Distributed decision making': 'Distributed Decision Making',
        'Grow Africa, Grow Cardano wv': 'Grow Africa, Grow Cardano',
        'Scale-UP Cardanos DeFi Ecosyste': "Scale-UP Cardano's DeFi Ecosystem",
        'Fund7 Challenge Setting wv': 'Fund7 Challenge Setting',
        'Sponsored by leftovers': 'Leftovers from regular challenges'
    }
    input_bud = {}  
    return {'replace_validation':replace_validation, 'input_bud':input_bud}

def get_budget_f6() -> dict:
    replace_validation = {
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
    input_bud = {}  
    return {'replace_validation':replace_validation, 'input_bud':input_bud}

def get_budget_f7() -> dict:
    replace_validation = {
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
    return {'replace_validation':replace_validation, 'input_bud':input_bud}

def get_budget_f8() -> dict:
    replace_validation = {
        'Accelerate Decentralized Identi': 'Accelerate Decentralized Identity',
        'Film + Media (FAM) creatives un': 'Film + Media (FAM) creatives unite!',
        'Lobbying for favorable legislat': 'Lobbying for favorable legislation',
        'Open Source Development Ecosyst': 'Open Source Development Ecosystem',
        'Open Standards & Interoperabili': 'Open Standards & Interoperability',
        'Scale-UP Cardanos Community Hub': "Scale-UP Cardano's Community Hubs",
        'The Great Migration (from Ether': 'The Great Migration (from Ethereum)',
        'Funded by leftovers': 'Sum of the leftovers'
    }
    input_bud = {}  
    return {'replace_validation':replace_validation, 'input_bud':input_bud}


##################################################
# FUNCTION GROUP: 
#   CHALLENG DATA PROCESSING
#
# EXPLANATION:
#   This group of functions return a dictionary containing the parameters
#   to be used in the CatalystVotingResults.__challenge_data_processing() processing method,
#   which generates the standardized dataframe containing the results of all Challenges
# 
# ADD FUND:
#   To add new Fund, copy, paste and uncomment the following template.
#   !! Important: 
#       - The {N} in the function's name should be replaced with the int-referece to the new Fund
#       - The code lines should be kept or similar formatting should be provided.
#
#   For futher information:
#   DEFAULT_COLS = ['challenge', 'Budget', 'Proposal', 
#                   'SCORE', 'YES', 'NO', 'Unique Yes', 
#                   'Unique No', 'Result','STATUS','REQUESTED $','REQUESTED %']
# TEMPLATE:
#-----------------------------------------
# def get_process_fN() -> dict:
#   # In case a DEFAULT_COLS has a different name from the ones defined in the global variable (informed above)
#   #    provide a dictionary {old_name : default_name} for renaming the pd.DataFrame columns 
#     rename = {}
#     return {'rename_default_cols':rename}
# ----------------------------------------

def get_process_f3() -> dict:
    rename = {}
    return {'rename_default_cols':rename}

def get_process_f4() -> dict:
    rename = {
        'Overall score': 'SCORE'
    }
    return {'rename_default_cols':rename}

def get_process_f5() -> dict:
    rename = {
        'Overall score': 'SCORE'
    }
    return {'rename_default_cols':rename}

def get_process_f6() -> dict:
    rename = {
        'Overall score': 'SCORE'
    }
    return {'rename_default_cols':rename}

def get_process_f7() -> dict:
    rename = {
        'Overall score': 'SCORE'
    }
    return {'rename_default_cols':rename}

def get_process_f8() -> dict:
    rename = {
        'Overall score': 'SCORE'
    }
    return {'rename_default_cols':rename}
