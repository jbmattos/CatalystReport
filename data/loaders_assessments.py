'''
DATA LOADERS FOR VOTING-RESULTS DATA

This file provides fund-specific functions to properly load `datafiles_votingresults` data
into `catalyst_votingresults.CatalystVotingResults` objects.

For adding new Fund data to the repository, 
follow the comments provided in this file
to implement the necessary new-fund specific functions.
'''

from typing import Type
import numpy as np
import pandas as pd
import os

PATH = os.path.dirname(__file__)+'/datafiles_assessments/'
ERR_DEF_ASSESSMENTS_FEAT = "Error while loading {} assessments: missing default features.\nPlease,assure the returning pd.DataFrame to contain the following features: {}."

# ---------------------------------------------------------------
# MANUAL INPUT: For new fundings, add the file reference bellow
# ---------------------------------------------------------------
FUNDS_FILES = {      
    # "f3": PATH+"Final_vCA Aggregated - fund3.xlsx",
    "f4": PATH+"Final_vCA Aggregated - fund4.xlsx",
    "f5": PATH+"vCA Aggregated - Fund 5.xlsx",
    "f6": PATH+"vCA Aggregated - Fund 6.xlsx",
    "f7": PATH+"vCA Aggregated - Fund 7.xlsx",
    # "f8": PATH+"vCA Aggregated - Fund 8.xlsx"
}
DEFAULT_ASSESSMENTS_FEATS = ['CA','PROPOSAL_TITLE','CA_RATING','QA_STATUS','REASON','QA_CLASS']

def available_data() -> dict:
    return FUNDS_FILES


##################################################
# GET ASSESSMENTS 
#
# Returns a dictionary of parameters to be used in the structure 
# of CatalystAssessments.__get_assessments data
#
# TEMPLATE:
#
# ----------------------------------------
# def get_assessments_fN(xlsx_obj:pd.ExcelFile) -> pd.DataFrame:
#     '''
#     This function receives a xlsx file containing all Fund's Assessments data
#     and return a pd.DataFrame [assessments x DEFAULT_ASSESSMENTS_FEATS]

#     !!! It is important that the final dataframe contains all DEFAULT_ASSESSMENTS_FEATS
#     '''
#     # Setup the valid assessments dataframe
#     df_valid = df_valid[DEFAULT_ASSESSMENTS_FEATS]

#     # Setup the excluded assessments dataframe
#     df_exc = df_exc[DEFAULT_ASSESSMENTS_FEATS]

#     df_final = pd.concat([df_valid,df_exc], axis='index').reset_index(drop=True)
#     if set(df_final.columns)==set(DEFAULT_ASSESSMENTS_FEATS): return df_final
#     else: raise TypeError(ERR_DEF_ASSESSMENTS_FEAT.format('get_assessments_fN', DEFAULT_ASSESSMENTS_FEATS))
##################################################


# def get_assessments_f3(xlsx_obj:pd.ExcelFile) -> pd.DataFrame:
#     '''
#     This function receives a xlsx file containing all Fund's Assessments data
#     and return a pd.DataFrame [assessments x DEFAULT_ASSESSMENTS_FEATS]

#     !!! It is important that the final dataframe contains all DEFAULT_ASSESSMENTS_FEATS
#     '''
#     # Setup the valid assessments dataframe
#     df_valid = df_valid[DEFAULT_ASSESSMENTS_FEATS]

#     # Setup the excluded assessments dataframe
#     df_exc = df_exc[DEFAULT_ASSESSMENTS_FEATS]

#     df_final = pd.concat([df_valid,df_exc], axis='index').reset_index(drop=True)
#     if set(df_final.columns)==set(DEFAULT_ASSESSMENTS_FEATS): return df_final
#     else: raise TypeError(ERR_DEF_ASSESSMENTS_FEAT.format('get_assessments_f3', DEFAULT_ASSESSMENTS_FEATS))

def get_assessments_f4(xlsx_obj:pd.ExcelFile) -> pd.DataFrame:
    '''
    This function receives a xlsx file containing all Fund's Assessments data
    and return a pd.DataFrame [assessments x DEFAULT_ASSESSMENTS_FEATS]

    !!! It is important that the final dataframe contains all DEFAULT_ASSESSMENTS_FEATS
    '''
    # Setup the valid assessments dataframe
    val_columns = {
        'Idea Title' : 'PROPOSAL_TITLE',
        'Assessor': 'CA',
        'Rating Given': 'CA_RATING'
    }
    df_valid = xlsx_obj.parse(sheet_name='Valid Assessments')[val_columns.keys()].rename(columns=val_columns)
    df_valid['QA_STATUS'] = 'Valid'
    df_valid['REASON'] = 'Valid'
    df_valid['QA_CLASS'] = np.nan
    df_valid = df_valid[DEFAULT_ASSESSMENTS_FEATS]

    # Setup the excluded assessments dataframe
    exc_columns = {
        'Idea Title' : 'PROPOSAL_TITLE',
        'Assessor': 'CA',
        'Rating Given': 'CA_RATING',
        'reason': 'REASON'
    }
    df_exc = xlsx_obj.parse(sheet_name='Excluded Assessments')[exc_columns.keys()].rename(columns=exc_columns)
    df_exc['QA_STATUS'] = 'Excluded'
    df_exc['QA_CLASS'] = np.nan
    df_exc = df_exc[DEFAULT_ASSESSMENTS_FEATS]

    df_final = pd.concat([df_valid,df_exc], axis='index').reset_index(drop=True)
    if set(df_final.columns)==set(DEFAULT_ASSESSMENTS_FEATS): return df_final
    else: raise TypeError(ERR_DEF_ASSESSMENTS_FEAT.format('get_assessments_f4', DEFAULT_ASSESSMENTS_FEATS))

def get_assessments_f5(xlsx_obj:pd.ExcelFile) -> pd.DataFrame:
    '''
    This function receives a xlsx file containing all Fund's Assessments data
    and return a pd.DataFrame [assessments x DEFAULT_ASSESSMENTS_FEATS]

    !!! It is important that the final dataframe contains all DEFAULT_ASSESSMENTS_FEATS
    '''
    # Setup the valid assessments dataframe
    val_columns = {
        'proposal_id' : 'proposal_id',
        'Idea Title' : 'PROPOSAL_TITLE',
        'Assessor': 'CA',
        'Rating Given': 'CA_RATING'
        }
    df_valid = xlsx_obj.parse(sheet_name='Valid Assessments')[val_columns.keys()].rename(columns=val_columns)
    df_valid['QA_STATUS'] = 'Valid'
    df_valid['REASON'] = 'Valid'
    df_valid['QA_CLASS'] = np.nan

    # Setup the excluded assessments dataframe
    exc_columns = {
        'proposal_id' : 'proposal_id',
        'Assessor': 'CA',
        'Rating Given': 'CA_RATING',
        'reason': 'REASON'
        }
    df_exc = xlsx_obj.parse(sheet_name='Excluded Assessments')[exc_columns.keys()].rename(columns=exc_columns)
    map_proposal = df_valid.loc[df_valid.proposal_id.isin(df_exc.proposal_id.unique()),['PROPOSAL_TITLE','proposal_id']].drop_duplicates(subset='proposal_id')
    df_exc['PROPOSAL_TITLE'] = df_exc.proposal_id.apply(lambda p_id: map_proposal[map_proposal.proposal_id==p_id]['PROPOSAL_TITLE'].item())
    df_exc['QA_STATUS'] = 'Excluded'
    df_exc['QA_CLASS'] = np.nan

    df_valid = df_valid[DEFAULT_ASSESSMENTS_FEATS]
    df_exc = df_exc[DEFAULT_ASSESSMENTS_FEATS]
    df_final = pd.concat([df_valid,df_exc], axis='index').reset_index(drop=True)

    if set(df_final.columns)==set(DEFAULT_ASSESSMENTS_FEATS): return df_final
    else: raise TypeError(ERR_DEF_ASSESSMENTS_FEAT.format('get_assessments_f5', DEFAULT_ASSESSMENTS_FEATS))

def get_assessments_f6(xlsx_obj:pd.ExcelFile) -> pd.DataFrame:
    '''
    This function receives a xlsx file containing all Fund's Assessments data
    and return a pd.DataFrame [assessments x DEFAULT_ASSESSMENTS_FEATS]

    !!! It is important that the final dataframe contains all DEFAULT_ASSESSMENTS_FEATS
    '''
    # Setup the valid assessments dataframe
    valid = xlsx_obj.parse(sheet_name='vCA Aggregated')
    val_columns = {
        'Idea Title' : 'PROPOSAL_TITLE',
        'Assessor': 'CA'
    }
    df_valid = valid[val_columns.keys()].rename(columns=val_columns)
    df_valid['CA_RATING'] = valid[['Impact / Alignment Rating', 'Feasibility Rating','Auditability Rating']].mean(axis=1)

    status_df = valid[['Result Excellent','Result Good','Result Filtered Out']].replace({'[xX]':True, np.nan: False}, regex=True)
    ### QA_CLASS = excelent/good assessments:  status and reason valid
    df_valid['QA_CLASS'] = status_df.apply(lambda row: row[row == True].index.values, axis='columns').replace({'Result Good':'Good', 'Result Excellent':'Excelent', 'Result Filtered Out':'Filtered Out'})
    df_valid['QA_STATUS'] = 'Valid'
    df_valid['REASON'] = 'Valid'
    ### QA_CLASS = filtered out assessments:  status excluded and reason filtered out
    filtered_out = (df_valid['QA_CLASS']=='Filtered Out')
    df_valid.loc[filtered_out,'QA_STATUS'] = 'Excluded'
    df_valid.loc[filtered_out,'REASON'] = 'Filtered Out'
    df_valid = df_valid[DEFAULT_ASSESSMENTS_FEATS]

    # Setup the excluded blank assessments dataframe
    exc = xlsx_obj.parse(sheet_name='Excluded Assessments')
    exc_columns = {
        'Idea Title' : 'PROPOSAL_TITLE',
        'Assessor': 'CA'
    }
    df_exc = exc[exc.Blank.replace({'[xX]':True, np.nan: False}, regex=True)][exc_columns.keys()].rename(columns=exc_columns)
    df_exc['CA_RATING'] = exc[['Impact / Alignment Rating', 'Feasibility Rating','Auditability Rating']].mean(axis=1)
    df_exc['QA_STATUS'] = 'Excluded'
    df_exc['QA_CLASS'] = np.nan
    df_exc['REASON'] = 'Blank'
    df_exc = df_exc[DEFAULT_ASSESSMENTS_FEATS]

    df_final = pd.concat([df_valid,df_exc], axis='index').reset_index(drop=True)
    if set(df_final.columns)==set(DEFAULT_ASSESSMENTS_FEATS): return df_final
    else: raise TypeError(ERR_DEF_ASSESSMENTS_FEAT.format('get_assessments_f6', DEFAULT_ASSESSMENTS_FEATS))

def get_assessments_f7(xlsx_obj:pd.ExcelFile) -> pd.DataFrame:
    '''
    This function receives a xlsx file containing all Fund's Assessments data
    and return a pd.DataFrame [assessments x DEFAULT_ASSESSMENTS_FEATS]

    !!! It is important that the final dataframe contains all DEFAULT_ASSESSMENTS_FEATS
    '''
    # Setup the valid assessments dataframe
    valid = xlsx_obj.parse(sheet_name='vCA Aggregated')
    val_columns = {
        'Idea Title' : 'PROPOSAL_TITLE',
        'Assessor': 'CA'
    }
    df_valid = valid[val_columns.keys()].rename(columns=val_columns)
    df_valid['CA_RATING'] = valid[['Impact / Alignment Rating', 'Feasibility Rating','Auditability Rating']].mean(axis=1)

    status_df = valid[['Result Excellent','Result Good','Result Filtered Out']].replace({'[xX]':True, np.nan: False}, regex=True)
    ### QA_CLASS = excelent/good assessments:  status and reason valid
    df_valid['QA_CLASS'] = status_df.apply(lambda row: row[row == True].index.values, axis='columns').replace({'Result Good':'Good', 'Result Excellent':'Excelent', 'Result Filtered Out':'Filtered Out'})
    df_valid['QA_STATUS'] = 'Valid'
    df_valid['REASON'] = 'Valid'
    ### QA_CLASS = filtered out assessments:  status excluded and reason filtered out
    filtered_out = (df_valid['QA_CLASS']=='Filtered Out')
    df_valid.loc[filtered_out,'QA_STATUS'] = 'Excluded'
    df_valid.loc[filtered_out,'REASON'] = 'Filtered Out'
    df_valid = df_valid[DEFAULT_ASSESSMENTS_FEATS]

    # Setup the excluded blank assessments dataframe
    exc = xlsx_obj.parse(sheet_name='Excluded Assessments')
    exc_columns = {
        'Idea Title' : 'PROPOSAL_TITLE',
        'Assessor': 'CA'
    }
    df_exc = exc[exc.Blank.replace({'[xX]':True, np.nan: False}, regex=True)][exc_columns.keys()].rename(columns=exc_columns)
    df_exc['CA_RATING'] = exc[['Impact / Alignment Rating', 'Feasibility Rating','Auditability Rating']].mean(axis=1)
    df_exc['QA_STATUS'] = 'Excluded'
    df_exc['QA_CLASS'] = np.nan
    df_exc['REASON'] = 'Blank'
    df_exc = df_exc[DEFAULT_ASSESSMENTS_FEATS]

    df_final = pd.concat([df_valid,df_exc], axis='index').reset_index(drop=True)
    if set(df_final.columns)==set(DEFAULT_ASSESSMENTS_FEATS): return df_final
    else: raise TypeError(ERR_DEF_ASSESSMENTS_FEAT.format('get_assessments_f7', DEFAULT_ASSESSMENTS_FEATS))

# def get_assessments_f8(xlsx_obj:pd.ExcelFile) -> pd.DataFrame:
#     '''
#     This function receives a xlsx file containing all Fund's Assessments data
#     and return a pd.DataFrame [assessments x DEFAULT_ASSESSMENTS_FEATS]

#     !!! It is important that the final dataframe contains all DEFAULT_ASSESSMENTS_FEATS
#     '''
#     # Setup the valid assessments dataframe
#     df_valid = df_valid[DEFAULT_ASSESSMENTS_FEATS]

#     # Setup the excluded assessments dataframe
#     df_exc = df_exc[DEFAULT_ASSESSMENTS_FEATS]

#     df_final = pd.concat([df_valid,df_exc], axis='index').reset_index(drop=True)
#     if set(df_final.columns)==set(DEFAULT_ASSESSMENTS_FEATS): return df_final
#     else: raise TypeError(ERR_DEF_ASSESSMENTS_FEAT.format('get_assessments_f8', DEFAULT_ASSESSMENTS_FEATS))


##################################################
# GET COMUNITY ADVISORS 
#
# Returns a dictionary of parameters to be used in the structure 
# of CatalystAssessments.__get_comunity_advisors data
#
# TEMPLATE:
#
# ----------------------------------------
# def get_cas_fN() -> dict:
#     # Setup the following parameters
#     params = {
#         "sheet":"",         # xlsx sheet to load data
#     }
#     return params
##################################################


# def get_cas_f3() -> dict:
#     # Setup the following parameters
#     params = {
#         "sheet":"",         # xlsx sheet to load data
#     }
#     return params

def get_cas_f4() -> dict:
    # Setup the following parameters
    params = {
        "sheet":"",         # xlsx sheet to load data
    }
    return params

def get_cas_f5() -> dict:
    # Setup the following parameters
    params = {
        "sheet":"Community Advisors",         # xlsx sheet to load data
    }
    return params

def get_cas_f6() -> dict:
    # Setup the following parameters
    params = {
        "sheet":""
    }
    return params

def get_cas_f7() -> dict:
    # Setup the following parameters
    params = {
        "sheet":"" 
    }
    return params

# def get_cas_f8() -> dict:
#     # Setup the following parameters
#     params = {
#         "sheet":"",         # xlsx sheet to load data
#     }
#     return params


##################################################
# GET VETERAN COMUNITY ADVISORS 
#
# Returns a dictionary of parameters to be used in the structure 
# of CatalystAssessments.__get_comunity_advisors data
#
# TEMPLATE:
#
# ----------------------------------------
# def get_vcas_fN() -> dict:
#     # Setup the following parameters
#     params = {
#         "sheet":"",         # xlsx sheet to load data
#     }
#     return params
##################################################


# def get_vcas_f3() -> dict:
#     # Setup the following parameters
#     params = {
#         "sheet":"",         # xlsx sheet to load data
#     }
#     return params

def get_vcas_f4() -> dict:
    # Setup the following parameters
    params = {
        "sheet":"",         # xlsx sheet to load data
    }
    return params

def get_vcas_f5() -> dict:
    # Setup the following parameters
    params = {
        "sheet":"Veteran Community Advisors",         # xlsx sheet to load data
    }
    return params

def get_vcas_f6() -> dict:
    # Setup the following parameters
    params = {
        "sheet":"Veteran Community Advisors"
    }
    return params

def get_vcas_f7() -> dict:
    # Setup the following parameters
    params = {
        "sheet":"Veteran Community Advisors" 
    }
    return params

# def get_vcas_f8() -> dict:
#     # Setup the following parameters
#     params = {
#         "sheet":"",         # xlsx sheet to load data
#     }
#     return params
