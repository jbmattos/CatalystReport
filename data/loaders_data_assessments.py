'''
DATA LOADERS FOR VOTING-RESULTS DATA

This file provides fund-specific functions to properly load `datafiles_assessments` data
into `catalyst_data_assessments.CatalystAssessments` class format.

For adding new Fund data to the repository:
Follow the comments provided in this file to implement the necessary new-fund specific functions.
'''

import numpy as np
import pandas as pd
import os

PATH = os.path.dirname(__file__)+'/datafiles_assessments/'
ERR_DEFAULT_FEAT = "Error while loading {}: missing default features.\nPlease,assure the returning pd.DataFrame to contain the following features: {}."

# ---------------------------------------------------------------
# MANUAL INPUT: For new fundings, add the file reference bellow
# ---------------------------------------------------------------
FUNDS_FILES = {      
    "f3": PATH+"Community Aggregated - Review of Reviewers v3.xlsx",
    "f4": PATH+"Final_vCA Aggregated - fund4.xlsx",
    "f5": PATH+"vCA Aggregated - Fund 5.xlsx",
    "f6": PATH+"vCA Aggregated - Fund 6.xlsx",
    "f7": PATH+"vCA Aggregated - Fund 7.xlsx",
    "f8": PATH+"vCA Aggregated - Fund 8 (Final MVP candidate).xlsx"
}
DEFAULT_ASSESSMENTS_FEATS = ['CA','PROPOSAL_TITLE','CA_RATING','QA_STATUS','REASON','QA_CLASS']
DEFAULT_CA_FEATS = ['NUMBER_ASSESSMENTS','STATUS','REASON']
DEFAULT_VCA_FEATS = ['NAME','NUMBER_REVIEWS','URL']
DEFAULT_AGG_TXT_FEAT = ['Impact / Alignment Note', 'Feasibility Note', 'Auditability Note']

def available_data() -> dict:
    return FUNDS_FILES

##################################################
# FUNCTION GROUP: 
#   GET ASSESSMENTS 
#
# EXPLANATION:
#   This group of functions returns the standardized Assessments table
#   which contains all Fund's CAs' assessments and default features.
# 
# ADD FUND:
#   To add new Fund, copy, paste and uncomment the following template.
#   !! Important: 
#       - The {N} in the function's name should be replaced with the int-referece to the new Fund
#       - The code lines should be kept or similar formatting should be provided.
#
# TEMPLATE:
#-----------------------------------------
# def get_assessments_fN(xlsx_obj:pd.ExcelFile) -> pd.DataFrame:
#     '''
#     This function receives a xlsx file containing all Fund's Assessments data
#     and return a pd.DataFrame [assessments x DEFAULT_ASSESSMENTS_FEATS]
#
#     !!! It is important that the final dataframe contains all DEFAULT_ASSESSMENTS_FEATS
#     '''
#     # Setup the valid assessments dataframe
#     df_valid = df_valid[DEFAULT_ASSESSMENTS_FEATS]
#
#     # Setup the excluded assessments dataframe
#     df_exc = df_exc[DEFAULT_ASSESSMENTS_FEATS]
#
#     df_final = pd.concat([df_valid,df_exc], axis='index').reset_index(drop=True)
#     if set(df_final.columns)==set(DEFAULT_ASSESSMENTS_FEATS): return df_final
#     else: raise TypeError(ERR_DEFAULT_FEAT.format('get_assessments_fN', DEFAULT_ASSESSMENTS_FEATS)) # edit the function's name
##################################################

def get_assessments_f3(xlsx_obj:pd.ExcelFile) -> pd.DataFrame:
    '''
    This function receives a xlsx file containing all Fund's Assessments data
    and return a pd.DataFrame [assessments x DEFAULT_ASSESSMENTS_FEATS]

    !!! It is important that the final dataframe contains all DEFAULT_ASSESSMENTS_FEATS
    '''
    data = xlsx_obj.parse(sheet_name='Proposals')
    columns = {
        'Idea Title' : 'PROPOSAL_TITLE',
        'Assessor': 'CA'
    }
    df_final = data[columns.keys()].rename(columns=columns)
    df_final['CA_RATING'] = np.nan
    df_final['QA_CLASS'] = np.nan
    df_final['REASON'] = data['Outcome'].replace({np.nan:"NOT_VOTTED"})
    df_final['QA_STATUS'] = df_final['REASON'].map(lambda v: 'Excluded' if v=='UNJUSTIFIED' else 'Valid')
    df_final = df_final[DEFAULT_ASSESSMENTS_FEATS]

    if set(df_final.columns)==set(DEFAULT_ASSESSMENTS_FEATS): return df_final
    else: raise TypeError(ERR_DEFAULT_FEAT.format('get_assessments_f3', DEFAULT_ASSESSMENTS_FEATS))

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
    else: raise TypeError(ERR_DEFAULT_FEAT.format('get_assessments_f4', DEFAULT_ASSESSMENTS_FEATS))

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
    else: raise TypeError(ERR_DEFAULT_FEAT.format('get_assessments_f5', DEFAULT_ASSESSMENTS_FEATS))

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
    df_valid = df_valid[df_valid.PROPOSAL_TITLE!='WITHDRAW'].copy()
    df_valid['CA_RATING'] = valid[['Impact / Alignment Rating', 'Feasibility Rating','Auditability Rating']].mean(axis=1)

    status_df = valid[['Result Excellent','Result Good','Result Filtered Out']].replace({'[xX]':True, np.nan: False}, regex=True)
    ### QA_CLASS = excelent/good assessments:  status and reason valid
    df_valid['QA_CLASS'] = status_df.apply(lambda row: str(row[row == True].index.values), axis='columns')
    df_valid['QA_CLASS'] = df_valid['QA_CLASS'].apply(lambda v: v.replace('[','').replace(']','').replace('Result ','').replace("'",''))
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
    df_exc = df_exc[df_exc.PROPOSAL_TITLE!='WITHDRAW'].copy()
    df_exc = df_exc[DEFAULT_ASSESSMENTS_FEATS]

    df_final = pd.concat([df_valid,df_exc], axis='index').reset_index(drop=True)
    if set(df_final.columns)==set(DEFAULT_ASSESSMENTS_FEATS): return df_final
    else: raise TypeError(ERR_DEFAULT_FEAT.format('get_assessments_f6', DEFAULT_ASSESSMENTS_FEATS))

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
    df_valid['QA_CLASS'] = status_df.apply(lambda row: str(row[row == True].index.values), axis='columns')
    df_valid['QA_CLASS'] = df_valid['QA_CLASS'].apply(lambda v: v.replace('[','').replace(']','').replace('Result ','').replace("'",''))
    df_valid['QA_STATUS'] = 'Valid'
    df_valid['REASON'] = 'Valid'
    ### QA_CLASS = filtered out assessments:  status excluded and reason filtered out
    filtered_out = (df_valid['QA_CLASS']=='Filtered Out')
    df_valid.loc[filtered_out,'QA_STATUS'] = 'Excluded'
    df_valid.loc[filtered_out,'REASON'] = 'Filtered Out'
    ### QA_CLASS = less than min_char assessments:  status excluded and reason < min_char 
    min_char = 150
    less_minchar = valid[DEFAULT_AGG_TXT_FEAT].agg(''.join, axis=1).apply(lambda x: len(x)) < min_char
    df_valid.loc[less_minchar,'QA_STATUS'] = 'Excluded'
    df_valid.loc[filtered_out,'REASON'] = '<{} char'.format(min_char)
    #
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
    else: raise TypeError(ERR_DEFAULT_FEAT.format('get_assessments_f7', DEFAULT_ASSESSMENTS_FEATS))

def get_assessments_f8(xlsx_obj:pd.ExcelFile) -> pd.DataFrame:
    '''
    This function receives a xlsx file containing all Fund's Assessments data
    and return a pd.DataFrame [assessments x DEFAULT_ASSESSMENTS_FEATS]

    !!! It is important that the final dataframe contains all DEFAULT_ASSESSMENTS_FEATS
    '''
    valid = xlsx_obj.parse(sheet_name='vCA Aggregated')
    val_columns = {
        'Idea Title' : 'PROPOSAL_TITLE',
        'Assessor': 'CA'
    }
    df_valid = valid[val_columns.keys()].rename(columns=val_columns)
    df_valid['CA_RATING'] = valid[['Impact / Alignment Rating', 'Feasibility Rating','Auditability Rating']].mean(axis=1)

    status_df = valid[['Result Excellent','Result Good','Result Filtered Out']].replace({'[xX]':True, np.nan: False}, regex=True)
    ### QA_CLASS = excelent/good assessments:  status and reason valid
    df_valid['QA_CLASS'] = status_df.apply(lambda row: str(row[row == True].index.values), axis='columns')
    df_valid['QA_CLASS'] = df_valid['QA_CLASS'].apply(lambda v: v.replace('[','').replace(']','').replace('Result ','').replace("'",''))
    df_valid['QA_STATUS'] = 'Valid'
    df_valid['REASON'] = 'Valid'
    ### QA_CLASS = filtered out assessments:  status excluded and reason filtered out
    filtered_out = (df_valid['QA_CLASS']=='Filtered Out')
    df_valid.loc[filtered_out,'QA_STATUS'] = 'Excluded'
    df_valid.loc[filtered_out,'REASON'] = 'Filtered Out'
    ### QA_CLASS = less than min_char assessments:  status excluded and reason < min_char 
    min_char = 150
    less_minchar = valid[DEFAULT_AGG_TXT_FEAT].agg(''.join, axis=1).apply(lambda x: len(x)) < min_char
    df_valid.loc[less_minchar,'QA_STATUS'] = 'Excluded'
    df_valid.loc[filtered_out,'REASON'] = '<{} char'.format(min_char)
    #
    df_valid = df_valid[DEFAULT_ASSESSMENTS_FEATS]

    # Setup the excluded blank assessments dataframe
    exc = xlsx_obj.parse(sheet_name='Excluded Assessments')
    exc_columns = {
        'Idea Title' : 'PROPOSAL_TITLE',
        'Assessor': 'CA'
    }
    df_exc = exc[exc.Blank.replace({'[xX]':True, np.nan: False}, regex=True)][exc_columns.keys()].rename(columns=exc_columns)
    if df_exc.shape[0] > 0:
        df_exc['CA_RATING'] = exc[['Impact / Alignment Rating', 'Feasibility Rating','Auditability Rating']].mean(axis=1)
        df_exc['QA_STATUS'] = 'Excluded'
        df_exc['QA_CLASS'] = np.nan
        df_exc['REASON'] = 'Blank'
        df_exc = df_exc[DEFAULT_ASSESSMENTS_FEATS]

        df_final = pd.concat([df_valid,df_exc], axis='index').reset_index(drop=True)
    else:
        df_final = df_valid.reset_index(drop=True)
    if set(df_final.columns)==set(DEFAULT_ASSESSMENTS_FEATS): return df_final
    else: raise TypeError(ERR_DEFAULT_FEAT.format('get_assessments_f8', DEFAULT_ASSESSMENTS_FEATS))


##################################################
# FUNCTION GROUP: 
#   GET COMUNITY ADVISORS 
#
# EXPLANATION:
#   This group of functions returns the standardized CAs' table
#   which contains information on all CA's that had participated on the Fund
# 
# ADD FUND:
#   To add new Fund, copy, paste and uncomment the following template.
#   !! Important: 
#       - The {N} in the function's name should be replaced with the int-referece to the new Fund
#       - The code lines should be kept or similar formatting should be provided.
#
# TEMPLATE:
#-----------------------------------------
# def get_cas_fN(df_assess:pd.DataFrame, xlsx_obj:pd.ExcelFile) -> pd.DataFrame:
#     # Build dataframe from Unique Assessments' CAs and Default Features
#     df_ca = pd.DataFrame(index=df_assess.CA.unique(), columns=DEFAULT_CA_FEATS)
#     df_ca.sort_index(inplace=True)
#
#     # input NUMBER_ASSESSMENTS
#     df_ca['NUMBER_ASSESSMENTS'] = df_assess.CA.value_counts()
#
#     # input ca's STATUS
#
#     # input ca's status REASON
#
#     return df_ca
##################################################

def get_cas_f3(df_assess:pd.DataFrame, xlsx_obj:pd.ExcelFile) -> pd.DataFrame:
    # Build dataframe from Unique Assessments' CAs and Default Features
    df_ca = pd.DataFrame(index=df_assess.CA.unique(), columns=DEFAULT_CA_FEATS)
    df_ca.sort_index(inplace=True)

    # input NUMBER_ASSESSMENTS
    df_ca['NUMBER_ASSESSMENTS'] = df_assess.CA.value_counts()

    return df_ca

def get_cas_f4(df_assess:pd.DataFrame, xlsx_obj:pd.ExcelFile) -> pd.DataFrame:
    # Build dataframe from Unique Assessments' CAs and Default Features
    df_ca = pd.DataFrame(index=df_assess.CA.unique(), columns=DEFAULT_CA_FEATS)
    df_ca.sort_index(inplace=True)

    # input NUMBER_ASSESSMENTS
    df_ca['NUMBER_ASSESSMENTS'] = df_assess.CA.value_counts()

    # input ca's STATUS
    df_ca['STATUS'] = 'Included'
    exc = xlsx_obj.parse(sheet_name='Excluded assessors')
    df_ca.loc[exc.name,'STATUS'] = 'Excluded'

    # input ca's status REASON
    df_ca['REASON'] = 'Included'
    exc.set_index('name', inplace=True)
    exc.sort_index(inplace=True)
    df_ca.loc[exc.index.values,'REASON'] = exc[['By Card', 'By Blanks']].apply(lambda row: row[row == True].index.values, axis='columns').replace({'By Card':'By Card', 'By Blanks':'By Blanks'})
    
    return df_ca

def get_cas_f5(df_assess:pd.DataFrame, xlsx_obj:pd.ExcelFile) -> pd.DataFrame:
    # Build dataframe from Unique Assessments' CAs and Default Features
    df_ca = pd.DataFrame(index=df_assess.CA.unique(), columns=DEFAULT_CA_FEATS)
    df_ca.sort_index(inplace=True)

    # input NUMBER_ASSESSMENTS
    df_ca['NUMBER_ASSESSMENTS'] = df_assess.CA.value_counts()

    # input ca's STATUS
    cas = xlsx_obj.parse(sheet_name='Community Advisors')
    cas.set_index('assessor', inplace=True)
    cas.sort_index(inplace=True)
    df_ca['STATUS'] = cas.excluded.map(lambda v: 'Excluded' if v == True else 'Included')

    # input ca's status REASON
    
    return df_ca

def get_cas_f6(df_assess:pd.DataFrame, xlsx_obj:pd.ExcelFile) -> pd.DataFrame:
    # Build dataframe from Unique Assessments' CAs and Default Features
    df_ca = pd.DataFrame(index=df_assess.CA.unique(), columns=DEFAULT_CA_FEATS)
    df_ca.sort_index(inplace=True)

    # input NUMBER_ASSESSMENTS
    df_ca['NUMBER_ASSESSMENTS'] = df_assess.CA.value_counts()

    # input ca's STATUS
    counts = df_assess.groupby('CA')['QA_STATUS'].value_counts().unstack(fill_value=0)
    excluded = counts.Excluded > 0.2* counts.sum(axis='columns')
    df_ca['STATUS'] = excluded.map(lambda v: 'Excluded' if v else 'Included')

    # input ca's status REASON
    df_ca['REASON'] =  excluded.map(lambda v: '(Excluded) > 20% (Valid+Excluded)' if v else 'Included')

    return df_ca


def get_cas_f7(df_assess:pd.DataFrame, xlsx_obj:pd.ExcelFile) -> pd.DataFrame:
    # Build dataframe from Unique Assessments' CAs and Default Features
    df_ca = pd.DataFrame(index=df_assess.CA.unique(), columns=DEFAULT_CA_FEATS)
    df_ca.sort_index(inplace=True)

    # input NUMBER_ASSESSMENTS
    df_ca['NUMBER_ASSESSMENTS'] = df_assess.CA.value_counts()

    # input ca's STATUS
    counts = df_assess.groupby('CA')['QA_STATUS'].value_counts().unstack(fill_value=0)
    excluded = counts.Excluded > 0.2* counts.sum(axis='columns')
    df_ca['STATUS'] = excluded.map(lambda v: 'Excluded' if v else 'Included')

    # input ca's status REASON
    df_ca['REASON'] =  excluded.map(lambda v: '(Excluded) > 20% (Valid+Excluded)' if v else 'Included')

    return df_ca


def get_cas_f8(df_assess:pd.DataFrame, xlsx_obj:pd.ExcelFile) -> pd.DataFrame:
    # Build dataframe from Unique Assessments' CAs and Default Features
    df_ca = pd.DataFrame(index=df_assess.CA.unique(), columns=DEFAULT_CA_FEATS)
    df_ca.sort_index(inplace=True)

    # input NUMBER_ASSESSMENTS
    df_ca['NUMBER_ASSESSMENTS'] = df_assess.CA.value_counts()

    # input ca's STATUS
    counts = df_assess.groupby('CA')['QA_STATUS'].value_counts().unstack(fill_value=0)
    excluded = counts.Excluded > 0.2* counts.sum(axis='columns')
    df_ca['STATUS'] = excluded.map(lambda v: 'Excluded' if v else 'Included')

    # input ca's status REASON
    df_ca['REASON'] =  excluded.map(lambda v: '(Excluded) > 20% (Valid+Excluded)' if v else 'Included')

    return df_ca


##################################################
# FUNCTION GROUP: 
#   GET VETERAN COMUNITY ADVISORS  
#
# EXPLANATION:
#   This group of functions returns the standardized vCAs' table
#   which contains information on all vCA's that had participated on the Fund
# 
# ADD FUND:
#   To add new Fund, copy, paste and uncomment the following template.
#   !! Important: 
#       - The {N} in the function's name should be replaced with the int-referece to the new Fund
#       - The code lines should be kept or similar formatting should be provided.
#
# TEMPLATE:
#-----------------------------------------
# def get_vcas_fN(xlsx_obj:pd.ExcelFile) -> pd.DataFrame:
#     # Load vCAs information
#     vcas = xlsx_obj.parse(sheet_name='')
#
#     # Input NAME feature
#
#     # Input NUMBER_REVIEWS feature 
#
#     # Input URL feature 
#
#     vcas = vcas[DEFAULT_VCA_FEATS]
#     if set(vcas.columns)==set(DEFAULT_VCA_FEATS): return vcas
#     else: raise TypeError(ERR_DEFAULT_FEAT.format('get_assessments_fN', DEFAULT_VCA_FEATS))   # edit the function's name
##################################################


def get_vcas_f3(xlsx_obj:pd.ExcelFile) -> pd.DataFrame:
    vcas_names = ['Rene M','Łukasz K','Robert T', 'Olexiy M','Filip B','Michael P',
                'Cryptostig','2072 [ANFRA]','Rodrigo P','RescuedCookie22',
                'CryptoPrime','Steve A','Matias P','Jaime S','Ilija','Anthony',
                'Greg P','James A','Thiago','Danny R']
    df = xlsx_obj.parse(sheet_name='Proposals')[vcas_names]
    vcas = pd.DataFrame(columns=DEFAULT_VCA_FEATS)
    vcas['NAME'] = df.count().index
    vcas['NUMBER_REVIEWS'] = df.count().values
    
    if set(vcas.columns)==set(DEFAULT_VCA_FEATS): return vcas
    else: raise TypeError(ERR_DEFAULT_FEAT.format('get_vcas_f3', DEFAULT_VCA_FEATS))

def get_vcas_f4(xlsx_obj:pd.ExcelFile) -> pd.DataFrame:
    
    # local vars
    vca_cols = ["Fair","Constructive Feedback","Profanity","Score doesn't match","Copy","Wrong challenge","Wrong criteria","General Infraction","General Infraction: rationale"]
    sheet_name_mask = 'vCA Master File Fund 4 - '
    vca_sheets = [s for s in xlsx_obj.sheet_names if sheet_name_mask in s]

    # vcas dataframe
    vcas = pd.DataFrame(columns=DEFAULT_VCA_FEATS)

    # Input NAME feature
    func_names = lambda sheet_name: sheet_name.replace(sheet_name_mask, '')
    vcas['NAME'] = list(map(func_names, vca_sheets))

    # Input NUMBER_REVIEWS feature
    func_n_reviews = lambda name: xlsx_obj.parse(sheet_name=sheet_name_mask+name)[vca_cols].dropna(axis='index', how='all').shape[0]
    vcas['NUMBER_REVIEWS'] = vcas['NAME'].map(func_n_reviews)

    vcas = vcas[DEFAULT_VCA_FEATS]
    if set(vcas.columns)==set(DEFAULT_VCA_FEATS): return vcas
    else: raise TypeError(ERR_DEFAULT_FEAT.format('get_vcas_f4', DEFAULT_VCA_FEATS))

def get_vcas_f5(xlsx_obj:pd.ExcelFile) -> pd.DataFrame:
    # Load vCAs information
    vcas = xlsx_obj.parse(sheet_name='Veteran Community Advisors').rename(columns={'link':'URL'})
    # Input NAME feature
    vcas['NAME'] = np.nan
    # Input NUMBER_REVIEWS feature 
    vcas['NUMBER_REVIEWS'] = np.nan

    vcas = vcas[DEFAULT_VCA_FEATS]
    if set(vcas.columns)==set(DEFAULT_VCA_FEATS): return vcas
    else: raise TypeError(ERR_DEFAULT_FEAT.format('get_vcas_f5', DEFAULT_VCA_FEATS))

def get_vcas_f6(xlsx_obj:pd.ExcelFile) -> pd.DataFrame:
    rename = {
        'name' : 'NAME',
        'vca_link': 'URL',
        'No. of Reviews': 'NUMBER_REVIEWS'
    }
    vcas = xlsx_obj.parse(sheet_name='Veteran Community Advisors').rename(columns=rename)
    vcas = vcas[DEFAULT_VCA_FEATS]

    if set(vcas.columns)==set(DEFAULT_VCA_FEATS): return vcas
    else: raise TypeError(ERR_DEFAULT_FEAT.format('get_vcas_f6', DEFAULT_VCA_FEATS))

def get_vcas_f7(xlsx_obj:pd.ExcelFile) -> pd.DataFrame:
    rename = {
        'Name' : 'NAME',
        'vca_link': 'URL',
        'No. of Reviews': 'NUMBER_REVIEWS'
    }
    vcas = xlsx_obj.parse(sheet_name='Veteran Community Advisors').rename(columns=rename)
    vcas = vcas[DEFAULT_VCA_FEATS]

    if set(vcas.columns)==set(DEFAULT_VCA_FEATS): return vcas
    else: raise TypeError(ERR_DEFAULT_FEAT.format('get_vcas_f7', DEFAULT_VCA_FEATS))

def get_vcas_f8(xlsx_obj:pd.ExcelFile) -> pd.DataFrame:
    rename = {
        'name' : 'NAME',
        'vca_link': 'URL',
        'No. of Reviews': 'NUMBER_REVIEWS'
    }
    vcas = xlsx_obj.parse(sheet_name='Veteran Community Advisors').rename(columns=rename)
    vcas['NUMBER_REVIEWS'] = vcas['NUMBER_REVIEWS'].astype(int)
    vcas = vcas[DEFAULT_VCA_FEATS]

    if set(vcas.columns)==set(DEFAULT_VCA_FEATS): return vcas
    else: raise TypeError(ERR_DEFAULT_FEAT.format('get_vcas_f8', DEFAULT_VCA_FEATS))

