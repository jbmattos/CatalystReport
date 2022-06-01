'''
This file stores a class to perform Exploratory Data Analysis
on the data related to a specific Catalyst Fund. 

The data used in the analysis is preprocessed with data.datasets.get_catalyst_data
and stored as CatalystData object.

This file provides a CatalystResults class 
containing a collection data analysis methods.
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

from catalyst_data_votingresults import CatalystVotingResults
from catalyst_data_assessments import CatalystAssessments

warnings.filterwarnings( "ignore", module = "matplotlib\..*" )
warnings.simplefilter('ignore', category=UserWarning)

# Class messages (error/warnings)
ERR_STATS_FEAT = 'Unidentified statistical feature {}. Please, select one of the following options: {}'

# Repository paths and files
ROOT = 'CatalystReport'
SIMPLE_REPORT_FILE = 'SIMPLE_REPORT_FILE.txt'
FULL_REPORT_FILE = 'FULL_REPORT_FILE.txt'

class CatalystFund():

    AVAILABLE_FUNDS = list(set(CatalystAssessments.FUNDS_FILES.keys()).intersection(
                            set(CatalystVotingResults.FUNDS_FILES.keys())))
    AVAILABLE_FUNDS.sort()

    def __init__(self, fund: str) -> None:
        self.__catalyst_results = CatalystVotingResults(fund)
        self.__catalyst_assessments = CatalystAssessments(fund)
        self.__default_score_feat = 'SCORE'
        self.__default_stats_feats = ['SCORE','YES','NO','Unique Yes','Unique No','Result','REQUESTED $','REQUESTED %']
        self.__palette_status = {"FUNDED": '#0570b0', # blue
                                 "NOT FUNDED": '#ec7014', # orange
                                 "NOT APPROVED": '#cb181d'} # red
        self.__report_path = os.path.dirname(__file__).split(ROOT)[0]+ROOT+'/report_CatalystFund-{}_{}/'.format(fund, date.today().strftime('%Y%m%d'))
    
    @property
    def fund(self) -> str:
        return self.__catalyst_results.fund
    @property
    def results(self) -> pd.DataFrame:
        return self.__catalyst_results.results.copy()
    @property
    def challenges(self) -> pd.Series:
        return pd.Series(self.__catalyst_results.results['challenge'].unique(), name='challenge').copy()
    @property
    def proposals(self) -> pd.DataFrame:
        return self.__catalyst_results.results['Proposal'].copy()
    @property
    def budgets(self) -> pd.Series:
        return self.__catalyst_results.validation.set_index(CatalystVotingResults.VALIDATION_COLS[0]) 
    @property
    def stats_feats(self) -> list:
        return list(set(self.__default_stats_feats).intersection(set(self.results.columns)))
        
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

    def get_challenge_results(self, challenge:str) -> pd.DataFrame:
        return self.__catalyst_results.get_challenge_results(challenge)
    
    def get_statistics(self, feats:list=[], metrics:list=[]) -> pd.DataFrame:
        if not feats: feats = self.stats_feats
        df_stats = self.__get_stats(feats)

        if metrics:
            m_selector = zip([f for f in feats for i in range(len(metrics))],
                            metrics*len(feats))
            return df_stats[m_selector]
        else: return df_stats
    
    def get_rating_stats_by_proposal(self) -> pd.DataFrame:
        return self.__catalyst_assessments.assessments.groupby('PROPOSAL_TITLE')['CA_RATING'].describe().sort_index()

    def get_ca_retention(self) -> pd.DataFrame:
        last_id = 'f{}'.format(int(self.fund[-1])-1)
        if last_id in CatalystAssessments.FUNDS_FILES.keys():
            return self.__ca_retention(f_last=last_id)
        else:
            print("!! No previous Fund to analyse retention.")
            return 
    
    def get_vca_retention(self) -> pd.DataFrame:
        pass

    def plot_distribution(self, feat:str='SCORE') -> None:
        if feat in self.stats_feats:
            self.__plot_dist(feat)
        else: 
            raise TypeError(ERR_STATS_FEAT.format(feat, self.stats_feats))
        return
    

    def plot_swarm(self, feat:str='SCORE') -> None:
        if feat in self.stats_feats:
            self.__plot_swarm(feat)
        else: 
            raise TypeError(ERR_STATS_FEAT.format(feat, self.stats_feats))
        return

    def plot_lm(self, x_feat:str, y_feat:str, fit_reg:bool=False) -> None:
        if (x_feat in self.stats_feats) and (y_feat in self.stats_feats):
            self.__plot_lm(x_feat, y_feat, fit_reg)
        else: 
            raise TypeError(ERR_STATS_FEAT.format((x_feat, y_feat), self.stats_feats))
        return
    
    def plot_budget_availability(self) -> None:
        
        # self.__plot_budavail(self.results, idx='overall')
        for challenge in self.challenges.to_list():
            df = self.results[self.results['challenge']==challenge].copy()
            self.__plot_budavail(df, idx=challenge)
        return

    def plot_budget_distribution(self) -> None:

        self.__plot_buddist(self.results, idx='overall')
        for challenge in self.challenges.to_list():
            df = self.results[self.results['challenge']==challenge].copy()
            self.__plot_buddist(df, idx=challenge)
        return
    
    def plot_assessments_by_proposals_hist(self) -> None:
        rcParams["font.size"] = 20
        rows = 1
        cols = 2
        bins = 10
        rcParams['figure.figsize'] = 9*cols, 6*rows
        fig, axes = plt.subplots(nrows=rows, ncols=cols, num='ass_dist', clear=True, sharex=True, sharey=True)

        # All proposals
        ax = axes[0]
        self.__catalyst_assessments.assessments.PROPOSAL_TITLE.value_counts().plot.hist(bins=bins, 
                                                                                        ax=ax, 
                                                                                        color=self.__palette_status['FUNDED'])
        ax.set_title("Overall Assessments Histogram")
        ax.set_ylabel('Proposal count')
        ax.set_xlabel('Number of Assessments')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        # ax.set_xticks(range(0,
        #                     self.__catalyst_assessments.assessments.PROPOSAL_TITLE.value_counts().max(), 
        #                     5))

        # Valid assessments
        ax = axes[1]
        self.__catalyst_assessments.assessments[self.__catalyst_assessments.assessments.QA_STATUS=='Valid']\
                                                .PROPOSAL_TITLE.value_counts().plot.hist(bins=bins, 
                                                                                        ax=ax, 
                                                                                        color=self.__palette_status['FUNDED'])
        ax.set_title("Valid Assessments Histogram")
        ax.set_ylabel('Proposal count')
        ax.set_xlabel('Number of Assessments')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.show()
        return
    
    def plot_assessments_status_overview(self) -> None:
        rcParams["font.size"] = 20
        rcParams['figure.figsize'] = 15, 6
        palette = ['#8dd3c7','#ffffb3','#bebada','#fb8072','#80b1d3','#fdb462','#b3de69','#fccde5','#d9d9d9','#bc80bd','#ccebc5','#ffed6f']
        pointer = 0

        print("This fund had a total number of {} assessments.".format(self.__catalyst_assessments.assessments.shape[0]))

        # Assessments Status (valid/excluded): overall assessments
        x = list(self.__catalyst_assessments.assessments.QA_STATUS.unique())
        y = [len(self.__catalyst_assessments.assessments[self.__catalyst_assessments.assessments['QA_STATUS']==status]) 
                                                         for status in x]
        c = palette[pointer:len(x)+pointer]
        pointer = len(x)
        
        fig = plt.figure()
        ax = fig.add_axes([0,0,1,1])
        ax.axis('equal')
        explode = [0.03]*len(x)
        ax.pie(y,
            labels=x,
            autopct='%1.2f%%',
            colors=c,
            shadow=True,
            pctdistance=0.5,
            labeldistance=1.2,
            explode = explode)
        ax.set_title("Overall Assessments status")
        plt.legend(bbox_to_anchor=(1.05, 0), loc=3, borderaxespad=0.)
        centre_circle = plt.Circle((0,0),0.70,fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        plt.show()

        # If QA assessments: assessments' classification (excelent, good, filtered out)
        if self.__catalyst_assessments.assessments.QA_CLASS.count() > 0:
            db = self.__catalyst_assessments.assessments.dropna(subset=['QA_CLASS'])
            x = list(db.QA_CLASS.unique())
            y = [len(db['QA_CLASS']==status) for status in x]
            c = palette[pointer:len(x)+pointer]
            pointer = len(x)

            fig = plt.figure()
            ax = fig.add_axes([0,0,1,1])
            ax.axis('equal')
            explode = [0.03]*len(x)
            ax.pie(y,
                labels=x,
                autopct='%1.2f%%',
                colors=c,
                shadow=True,
                pctdistance=0.5,
                labeldistance=1.2,
                explode = explode)
            ax.set_title("QA Assessments results")
            plt.legend(bbox_to_anchor=(1.05, 0), loc=3, borderaxespad=0.)
            centre_circle = plt.Circle((0,0),0.70,fc='white')
            fig = plt.gcf()
            fig.gca().add_artist(centre_circle)
            plt.show()

        # Excluded assessments (blanks, filtered out, less min_char...)
        db = self.__catalyst_assessments.assessments[self.__catalyst_assessments.assessments.QA_STATUS=='Excluded']
        x = list(db.REASON.unique())
        y = [len(db['REASON']==status) for status in x]
        c = palette[pointer:len(x)+pointer]
        pointer = len(x)

        fig = plt.figure()
        ax = fig.add_axes([0,0,1,1])
        ax.axis('equal')
        explode = [0.03]*len(x)
        ax.pie(y,
            labels=x,
            autopct='%1.2f%%',
            colors=c,
            shadow=True,
            pctdistance=0.5,
            labeldistance=1.2,
            explode = explode)
        ax.set_title("Excluded Assessments")
        centre_circle = plt.Circle((0,0),0.70,fc='white')
        fig = plt.gcf()
        plt.legend(bbox_to_anchor=(1.05, 0), loc=3, borderaxespad=0.)
        fig.gca().add_artist(centre_circle)
        plt.show()
        return

    def __plot_buddist(self, df:pd.DataFrame, idx:str) -> None:

        x = list(df.STATUS.unique())
        y = [len(df[df['STATUS']==status]) for status in x]

        rcParams["font.size"] = 20
        rcParams['figure.figsize'] = 15, 6

        fig = plt.figure()
        ax = fig.add_axes([0,0,1,1])
        ax.axis('equal')
        explode = [0.03]*len(x)
        ax.pie(y,
            labels=x,
            autopct='%1.2f%%',
            colors=[self.__palette_status[status] for status in x],
            shadow=True,
            pctdistance=0.5,
            labeldistance=1.2,
            explode = explode)
        ax.set_title("{} budget distribution".format(idx))
        plt.legend(bbox_to_anchor=(1.05, 0), loc=3, borderaxespad=0.)
        centre_circle = plt.Circle((0,0),0.70,fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        plt.show()
        return

    def __ca_retention(self, f_last:str) -> pd.DataFrame:
        f_last = CatalystAssessments(f_last)
        f_this = self.__catalyst_assessments
        retention = set(f_last.cas.index).intersection(set(f_this.cas.index))
        return pd.concat([f_last.cas.loc[retention], 
                          f_this.cas.loc[retention]], 
                          axis='columns', keys=['FUND {}'.format(f.fund) for f in [f_last, f_this]], 
                          names=['Fund','CA info']).sort_index()

    def __plot_budavail(self, df:pd.DataFrame, idx:str) -> None:
        df.sort_values(by=['Result'], ascending=False, inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.index += 1
        df['Ranking'] = [i+1 for i in range(df.shape[0])]
        remaining_budget = []
        if idx == 'overall':
            remaining_budget.append(self.budgets.sum().item())
        else:
            remaining_budget.append(df['Budget'].max())

        for index in df.index:
            if df.loc[index,'STATUS'] == 'FUNDED':
                remaining_budget.append(remaining_budget[-1]-df.loc[index,'REQUESTED $'])
            else:
                remaining_budget.append(remaining_budget[-1])
        df['Remaining Budget'] = remaining_budget[:-1]
        
        # set figure
        rcParams["font.size"] = 20
        rcParams['figure.figsize'] = 30, 6
        plot = sns.lmplot(x='Ranking',
                        y='REQUESTED $',
                        data=df,
                        fit_reg=False,
                        aspect=2.1,
                        hue="STATUS", 
                        palette=self.__palette_status,
                        legend=False)
        df['Remaining Budget'].plot.area(stacked=False,
                                        legend=False)
        # set axes
        ax = plt.gca()
        ax.set_title("{} proposals".format(idx))
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.legend(bbox_to_anchor=(1.05, 0), loc=3, borderaxespad=0.)
        plt.show()
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
        plt.show()
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
            title = '\n\n# Catalyst Fund Image Reports'
            explanation = '\nHere you will find compact reports in figure format, easy to share!'
            f.write(title)
            f.write(explanation)
            f.close()

        # REPORT-FOLDER README.md FILE
        readme_path = self.__report_path+'README.md'
        f = open(readme_path, 'w')
        # head info
        title = '\n\n# Catalyst Fund Report: FUND {}'.format(self.fund)
        explanation = '\nFind information and data analysis on Catalyt Fund {}'.format(self.fund[-1])
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
    parser = argparse.ArgumentParser(description='Catalyst Fund Analysis & Report')
    parser.add_argument("--fund", required=True,
                        choices=CatalystFund.AVAILABLE_FUNDS,
                        type=str,
                        help="Catalyst Fund to provide a report on.")
    # parser.add_argument("--simple", action='store_true',
    #                     help="Generates only simple report")
    # parser.add_argument("--notfig", action='store_false',
    #                     help="Deactivates the Figures' report")
    args = parser.parse_args()

    fund = CatalystFund(args.fund)
    fund.report(simple_report=True, 
                full_report=True, 
                fig_report=True)