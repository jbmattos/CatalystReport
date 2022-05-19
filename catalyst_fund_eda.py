'''
This file stores a class to perform Exploratory Data Analysis
on the data related to a specific Catalyst Fund. 

The data used in the analysis is preprocessed with data.datasets.get_catalyst_data
and stored as CatalystData object.

This file provides a CatalystResults class 
containing a collection data analysis methods.
'''

import re
import numpy as np
import pandas as pd

# review
import itertools
import json
import matplotlib.backends.backend_pdf
import pathlib
import seaborn as sns

from matplotlib import pyplot as plt
from matplotlib.gridspec import SubplotSpec
from matplotlib.pylab import rcParams
from mpl_toolkits.axes_grid1 import make_axes_locatable


from catalyst_votingresults import CatalystVotingResults


class CatalystFundEDA():
    def __init__(self, fund: str) -> None:
        self.__catalyst_data = CatalystVotingResults(fund)  # CatalystData
        self.__default_score_feat = 'SCORE'
        self.__default_stats_feats = ['SCORE','YES','NO','Unique Yes','Unique No','Result','REQUESTED $','REQUESTED %']
        self.__palette_status = {"FUNDED": '#0570b0', # blue
                                 "NOT FUNDED": '#ec7014', # orange
                                 "NOT APPROVED": '#cb181d'} # red
    
    @property
    def fund(self) -> str:
        return self.__catalyst_data.fund
    @property
    def results(self) -> pd.DataFrame:
        return self.__catalyst_data.results.copy()
    @property
    def challenges(self) -> pd.Series:
        return pd.Series(self.__catalyst_data.results['challenge'].unique(), name='challenge').copy()
    @property
    def proposals(self) -> pd.DataFrame:
        return self.__catalyst_data.results['Proposal'].copy()
    @property
    def __stats_feats(self) -> list:
        return list(set(self.__default_stats_feats).intersection(set(self.results.columns)))

    def get_challenge_results(self, challenge:str) -> pd.DataFrame:
        return self.__catalyst_data.data[challenge].copy()

    def report_statistics(self) -> None:
        '''
        Reports statistic data...
        '''
        if self.__score_feat in self.results:
            self.plot_score_overview()
        # add other analysis
        return
    
    def get_statistics(self, feats:list=[], metrics:list=[]) -> pd.DataFrame:
        if not feats: feats = self.__stats_feats
        df_stats = self.__get_stats(feats)

        if metrics:
            m_selector = zip([f for f in feats for i in range(len(metrics))],
                            metrics*len(feats))
            return df_stats[m_selector]
        else: return df_stats

    def plot_distribution(self, feat:str='SCORE') -> None:
        if feat in self.__stats_feats:
            self.__plot_dist(feat)
        else: 
            raise TypeError('Unidentified statistical feature {}. Please, select one of the following options: {}'.format(feat, self.__stats_feats))
        return
    

    def plot_swarm(self, feat:str='SCORE') -> None:
        if feat in self.__stats_feats:
            self.__plot_swarm(feat)
        else: 
            raise TypeError('Unidentified statistical feature {}. Please, select one of the following options: {}'.format(feat, self.__stats_feats))
        return

    def plot_lm(self, x_feat:str, y_feat:str, fit_reg:bool=False) -> None:
        if (x_feat in self.__stats_feats) and (y_feat in self.__stats_feats):
            self.__plot_lm(x_feat, y_feat, fit_reg)
        else: 
            raise TypeError('Unidentified statistical features {}. Please, select one of the following options: {}'.format((x_feat, y_feat), self.__stats_feats))
        return

    def __plot_lm(self, x_feat:str, y_feat:str, fit_reg:bool) -> None:
        height = 6
        rcParams["font.size"] = 20
        rcParams['figure.figsize'] = 30, height

        # PLOT 1: Overall results
        plot = sns.lmplot(x=x_feat,
                        y=y_feat,
                        data=self.results,
                        fit_reg=fit_reg,
                        height=height, aspect=2.1,
                        hue="STATUS", 
                        palette=self.__palette_status,
                        legend=False)
        # set axes
        ax = plt.gca()
        ax.set_title("Overall proposals")
        ax.set_ylabel(y_feat)
        ax.set_xlabel(x_feat)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.legend(bbox_to_anchor=(1.05, 0), loc=3, borderaxespad=0.)

        # PLOT 2: Plot by challenges
        rcParams['figure.figsize'] = 15, 6
        plot = sns.lmplot(x=x_feat,
                        y=y_feat,
                        data=self.results,
                        fit_reg=fit_reg,
                        height=(height-1), aspect=1.5,
                        col='challenge',
                        col_wrap=2,
                        hue="STATUS", 
                        palette=self.__palette_status,
                        legend=False)
        # set axes
        ax = plt.gca()
        ax.set_ylabel(y_feat)
        ax.set_xlabel(x_feat)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        return
    
    def __plot_swarm(self, feat:str) -> None:
        rcParams["font.size"] = 20
        rows = 2
        cols = 1
        point_size = 4
        nchallenges = len(self.results.challenge.unique())
        rcParams['figure.figsize'] = 12*cols, (nchallenges+1)
        fig, axes = plt.subplots(nrows=rows, ncols=cols, 
                                num='plot_swarm', facecolor='white', 
                                clear=True, sharex=True, sharey=False,
                                gridspec_kw={'height_ratios': [3, nchallenges]})

        # PLOT 1: Overall results
        ax = axes[0]
        sns.swarmplot(y="STATUS", x=feat,
                    palette=self.__palette_status, 
                    data=self.results,
                    size=point_size, 
                    ax=ax)
        # set axes
        ax.set_title("Overall proposals")
        ax.set_ylabel('')
        ax.set_xlabel('')
        ax.set_yticklabels(list(map(lambda i: '{} proposals'.format(i.get_text().capitalize()), ax.get_yticklabels())))
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)


        # PLOT 2: Plot by challenges
        ax = axes[1]
        sns.swarmplot(y="challenge", x=feat, hue="STATUS",
                    palette=self.__palette_status, 
                    data=self.results,
                    size=point_size+1,
                    ax=ax)
        # set axes
        ax.set_title("Proposals by Challenge".format(feat))
        ax.set_ylabel('')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.legend(bbox_to_anchor=(1.05, 0), loc=3, borderaxespad=0.)
        plt.show()
        return
    
    def __plot_dist(self, feat:str) -> None:
        rcParams["font.size"] = 20
        rows = 2
        cols = 1
        nchallenges = len(self.results.challenge.unique())
        rcParams['figure.figsize'] = 12*cols, (nchallenges+1)
        fig, axes = plt.subplots(nrows=rows, ncols=cols, 
                                num='plot_dist', facecolor='white', 
                                clear=True, sharex=True, sharey=False,
                                gridspec_kw={'height_ratios': [2, nchallenges]})

        # PLOT 1: Overall results
        ax = axes[0]
        sns.boxplot(y="STATUS", x=feat,
                    palette=self.__palette_status,
                    data=self.results,
                    ax=ax,
                    orient='h')
        # set axes
        ax.set_title("Overall {} distribution".format(feat))
        ax.set_ylabel('')
        ax.set_xlabel('')
        ax.set_yticklabels(list(map(lambda i: '{} proposals'.format(i.get_text().capitalize()), ax.get_yticklabels())))
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)


        # PLOT 2: Plot by challenges
        ax = axes[1]
        sns.boxplot(y="challenge", x=feat, 
                    hue="STATUS",
                    palette=self.__palette_status,
                    data=self.results,
                    ax=ax,
                    orient='h')
        # set axes
        ax.set_title("{} distribution by Challenge".format(feat))
        ax.set_ylabel('')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.legend(bbox_to_anchor=(1.05, 0), loc=3, borderaxespad=0.)
        plt.show()
        return    
    
    def __get_stats(self, feats:list) -> pd.DataFrame:
        ch_stats = self.results.groupby(['challenge','STATUS'])[feats].describe()
        all_stats = self.results.groupby(['STATUS'])[feats].describe()
        all_stats.index = pd.MultiIndex.from_tuples(zip(['ALL CHALLENGES']*all_stats.index.shape[0],
                                                        all_stats.index.get_level_values(0)),
                                                        names=["challenge", "STATUS"])
        df_stats = pd.concat([all_stats,ch_stats])

        ### NEW STATISTICS: COUNT %
        count_sum = df_stats.groupby('challenge').sum()[zip(feats, ['count']*len(feats))]
        df_sum = pd.concat([count_sum.loc[c[0]] for c in df_stats.index], axis=1).T
        df_sum.index = df_stats.index   # multiindex dataframe with 'count' statistics for each feat in feats
        # adding new feat to each feat level
        new_dfs = [] 
        for feat, nf in zip(feats, ['count%']*len(feats)):
            df = df_stats[feat].copy()
            df[nf] = df_stats[[(feat,'count')]] / df_sum[[(feat,'count')]]
            new_dfs.append(df.copy())
        df_stats = pd.concat(new_dfs, axis='columns', keys=feats)
        return df_stats
    



if __name__ == "__main__":
    pass