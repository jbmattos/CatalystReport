'''
This file stores a class to generate the Catalyst Results Report
using data from all available Catalyst Fund results. 

It builds on the CatalystFundEDA and CatalystData 
to provide a structured report over the Fund's history.

Running this file generates a local folder containing all analysis
- pdf report
- images
- file to input report analysis
'''

import argparse
import errno
from datetime import date
from matplotlib import pyplot as plt
from matplotlib.pylab import rcParams
import os
import pandas as pd
import seaborn as sns
import warnings

from catalyst_fund import CatalystFund

warnings.filterwarnings( "ignore", module = "matplotlib\..*" )
warnings.simplefilter('ignore', category=UserWarning)

# Class messages (error/warnings)

# Repository paths and files
ROOT = 'CatalystReport'
SIMPLE_REPORT_FILE = 'SIMPLE_REPORT_FILE.txt'
FULL_REPORT_FILE = 'FULL_REPORT_FILE.txt'

class CatalystProjectReport():
    def __init__(self) -> None:                                      # ['f\d']
        # self.__catalyst_f_eda = {f: CatalystFund(f) for f in funds}      # {'f\d' : CatalystFundEDA}
        # self.__df_evolution = self.__comput_evolution()
        self.__report_path = os.path.dirname(__file__).split(ROOT)[0]+ROOT+'/report_ProjectCatalyst_{}/'.format(date.today().strftime('%Y%m%d'))

    @property
    def funds(self) -> list:
        return list(self.__catalyst_f_eda.keys())
    @property
    def evolution(self) -> pd.DataFrame:
        return self.__df_evolution
    @property
    def _catalyst_funds(self) -> list: # [ CatalystFundEDA ]
        return list(self.__catalyst_f_eda.values())
    
    def report(self, simple_report:bool=True, 
                     full_report:bool=True, 
                     fig_report:bool=True) -> None:
        '''
        Generate a fund report:
        
        > Overall information
            - Number of assessments
            - Number of CAs (retention percentage)
            - Number of vCAs 
            - Voting Results information?
        
        > Plots information
            
        '''
        self.__create_report_folder(simple_report=simple_report,
                                    full_report=full_report,
                                    fig_folder=fig_report)
        return

    def __comput_evolution(self) -> pd.DataFrame:
        '''
        Evolution of Catalyst over time. Numbers of: 
            proposals, 
            challenges, 
            active CAs, 
            active vCAs, 
            voting power, 
            unique wallets
        '''

        # Evolution Time Series
        prop_evol = pd.Series(map(lambda c: c.proposals.shape[0], self._catalyst_funds), 
                      index=self.funds,
                      name='proposals_evolution',
                      dtype=int)
        ch_evol = pd.Series(map(lambda c: c.challenges.shape[0], self._catalyst_funds), 
                            index=self.funds,
                            name='challenges_evolution',
                            dtype=int)

        df_evol = pd.concat([prop_evol,
                            ch_evol], 
                            axis='columns', ignore_index=False)
        return df_evol

    def plot_evolution(self, save:str='') -> None:
        '''
        Plots all feat in CatalystReport.evolution in a sigle plot
        '''

        # set figure
        rcParams["font.size"] = 20
        rows = 1
        cols = len(self.evolution.columns)
        rcParams['figure.figsize'] = 9*cols, 6*rows
        fig, axes = plt.subplots(nrows=rows, ncols=cols, num='plot_evol', clear=True, sharex=True, sharey=False)


        for idx, metric in enumerate(self.evolution.columns):
            
            ax = axes[idx]
            self.evolution[metric].plot(kind='bar', ax=ax, color='#045a8d')
            
            # set axes
            if idx==0: ax.set_ylabel('Count')
            else: ax.set_ylabel('')
            ax.set_xlabel('Funds')
            
            ax.set_title('{}'.format(metric.replace('_',' ').capitalize()))
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            # plt.subplots_adjust(wspace=0.05)
        
        if save:
            pass
        return
    
    def plot_single_evolution(self, feat:str, save:str='') -> None:
        '''
        Feat must be a CatalystReport.evolution feature
        '''
        # set figure
        rcParams["font.size"] = 20
        rcParams['figure.figsize'] = 9, 6
        fig, ax = plt.subplots(nrows=1, ncols=1, num='plot_sing_evol', clear=True)

        self.evolution[feat].plot(kind='bar', ax=ax, color='#045a8d')

        # set axes
        ax.set_ylabel('Count')
        ax.set_xlabel('Funds')

        ax.set_title('{}'.format(feat.replace('_',' ').capitalize()))
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        # plt.subplots_adjust(wspace=0.05)

        if save:
            pass
        return
    
    def __create_report_folder(self, simple_report:bool, 
                                     full_report:bool, 
                                     fig_folder:bool) -> None:

        # REPORT FOLDER
        if not os.path.exists(os.path.dirname(self.__report_path)):
            try:
                os.makedirs(os.path.dirname(self.__report_path))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        
        # FIGURES SUBFOLDER
        if fig_folder:
            fig_folder_name = 'figs/'
            fig_path = self.__report_path+fig_folder_name
            if not os.path.exists(os.path.dirname(fig_path)):
                try:
                    os.makedirs(os.path.dirname(fig_path))
                except OSError as exc: # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
            # README.md FILE
            readme_path = fig_path+'README.md'
            f = open(readme_path, 'w')
            # head info
            title = '\n\n# Project Catalyst Image Reports'
            explanation = '\nHere you will find compact reports in figure format, easy to share!'
            f.write(title)
            f.write(explanation)
            f.close()

        # REPORT-FOLDER README.md FILE
        readme_path = self.__report_path+'README.md'
        f = open(readme_path, 'w')
        # head info
        title = '\n\n# Project Catalyst Report'
        explanation = '\nFind information and data analysis on all Project Catalyt Funds'
        f.write(title)
        f.write(explanation)
        # files' info
        if simple_report:
            f.write('\n\n## {}'.format(SIMPLE_REPORT_FILE))
            f.write('\nWrite here some explanation')
        if full_report:
            f.write('\n\n## {}'.format(FULL_REPORT_FILE))
            f.write('\nWrite here some explanation')
        if fig_folder:
            f.write('\n\n## {}'.format(fig_folder_name))
            f.write('\nWrite here some explanation')
        f.close()
        return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Project Catalyst Analysis & Report:\
                                                  Generate data analysis report on all Catalyst Funds')
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')               
    # required.add_argument("--fund", required=True,
    #                                 choices=CatalystFund.AVAILABLE_FUNDS,
    #                                 type=str,
    #                                 help="Catalyst Fund to provide a report on.")
    # optional.add_argument("--simple", action='store_true',
    #                     help="Generates only simple report")
    # optional.add_argument("--notfig", action='store_false',
    #                     help="Deactivates the Figures' report")
    
    args = parser.parse_args()

    catalyst = CatalystProjectReport()
    catalyst.report(simple_report=True, 
                    full_report=True, 
                    fig_report=True)