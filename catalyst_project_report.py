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

import numpy as np
import pandas as pd

# review
import seaborn as sns

from matplotlib import pyplot as plt
from matplotlib.pylab import rcParams

from catalyst_fund import CatalystFund

class CatalystReport():
    def __init__(self) -> None:                                      # ['f\d']
        # self.__catalyst_f_eda = {f: CatalystFund(f) for f in funds}      # {'f\d' : CatalystFundEDA}
        self.__df_evolution = self.__comput_evolution()

    @property
    def funds(self) -> list:
        return list(self.__catalyst_f_eda.keys())
    @property
    def evolution(self) -> pd.DataFrame:
        return self.__df_evolution
    @property
    def _catalyst_funds(self) -> list: # [ CatalystFundEDA ]
        return list(self.__catalyst_f_eda.values())

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

if __name__ == "__main__":
    pass