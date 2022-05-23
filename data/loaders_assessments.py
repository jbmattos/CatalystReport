'''
DATA LOADERS FOR VOTING-RESULTS DATA

This file provides fund-specific functions to properly load `datafiles_votingresults` data
into `catalyst_votingresults.CatalystVotingResults` objects.

For adding new Fund data to the repository, 
follow the comments provided in this file
to implement the necessary new-fund specific functions.
'''

import numpy as np
import pandas as pd
import os

PATH = os.path.dirname(__file__)+'/datafiles_assessments/'

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
# def get_assessments_fN() -> dict:
#     # Setup the following parameters
#     params = {
#         "sheet":"",         # xlsx sheet to load data
#         "x2bool_feat":[],   # features marked as "x" to transform to boolean
#     }
#     return params
##################################################


# def get_assessments_f3() -> dict:
#     # Setup the following parameters
#     params = {
#         "sheet":"",         # xlsx sheet to load data
#         "x2bool_feat":[],   # features marked as "x" to transform to boolean
#     }
#     return params

def get_assessments_f4() -> dict:
    # Setup the following parameters
    params = {
        "sheet":"",         # xlsx sheet to load data
        "x2bool_feat":[],   # features marked as "x" to transform to boolean
    }
    return params

def get_assessments_f5() -> dict:
    # Setup the following parameters
    params = {
        "sheet":"",         # xlsx sheet to load data
        "x2bool_feat":[],   # features marked as "x" to transform to boolean
    }
    return params

def get_assessments_f6() -> dict:
    # Setup the following parameters
    params = {
        "sheet":"vCA Aggregated", 
        "x2bool_feat":['Proposer Mark','Result Excellent','Result Good','Result Filtered Out']
    }
    return params

def get_assessments_f7() -> dict:
    # Setup the following parameters
    params = {
        "sheet":"vCA Aggregated", 
        "x2bool_feat":['Proposer Mark','Result Excellent','Result Good','Result Filtered Out']
    }
    return params

# def get_assessments_f8() -> dict:
#     # Setup the following parameters
#     params = {
#         "sheet":"",         # xlsx sheet to load data
#         "x2bool_feat":[],   # features marked as "x" to transform to boolean
#     }
#     return params


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

