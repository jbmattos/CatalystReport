# Project Catalyst Analysis & Report

**This repository aims at providing easy way of loading data from different stages of Project Catalyst Funds and providing analysis tools and structured reports.**\
_The current version offers functionalities over the Catalyst Funds 3 to 8. \
To add new Funds to the this repository, follow the instructions provided in the [data folder](https://github.com/jbmattos/CatalystReport/tree/main/data)._

## What is [Project Catalyst](https://cardano.ideascale.com/a/index)?
_"Project Catalyst is a series of experiments which seeks to generate the highest levels of community innovation. Catalyst is bringing on-chain governance to the Cardano blockchain by allowing the community to self-determine priorities for growth. It also lets participants deploy funding to proposals which tackle challenges and capitalize on opportunities that arise in the life cycle of Cardano._

_To do this, Project Catalyst is divided into a series of funds which are deployed every six weeks. These funds will illicit ideas in the form of proposals from participants. Each proposal will focus around a challenge issued by the Project Catalyst team or the Project Catalyst community. The proposals will then go through a community refinement process where they are vetted for feasibility, auditability, and impact by a group of incentivized community advisors. Once the proposals have been finalized they will be voted on by the community and funds will be distributed in the form of ada to winning projects."_

For more information, access the [Project Catalyst FAQ](https://docs.google.com/document/d/1qYtV15WXeM_AQYvISzr0a0Qj2IzW3hDvhMBvZZ4w2jE/edit#).

## Organization of this repository

The goal of this repository is to offer preprocessed and structured data from different stages of Catalyst Funds and methods to provide several analysis over such data.\
The contents of this repository may be divided into two categories:
- Classes to provide structure data (`catalyst_data_{CatalystStageData}.py` files)
- Classes to provide analysis methods (`catalyst_fund.py` & `catalyst_project_report.py`)

### Catalyst Structured Data Classes

Comprise the `catalyst_data_{CatalystStageData}.py` files, where `CatalystStageData` refers to data from different stages of the Project Catalyst Funds.
All data available through those classes are stored in the [data folder](https://github.com/jbmattos/CatalystReport/tree/main/data).
This repository offers structured data classes on the following _Catalyst Stages_:

1. **Assessments ([CatalystAssessments](https://github.com/jbmattos/CatalystReport/blob/main/catalyst_data_assessments.py))**\
Data information and sources can be found [here](https://github.com/jbmattos/CatalystReport/tree/main/data/datafiles_assessments).
Usage example can be found [here](https://github.com/jbmattos/CatalystReport/blob/main/catalyst_data_assessments_example.ipynb).

2. **Voting Results ([CatalystVotingResults](https://github.com/jbmattos/CatalystReport/blob/main/catalyst_data_votingresults.py]))**\
Data information and sources can be found [here](https://github.com/jbmattos/CatalystReport/tree/main/data/datafiles_votingresults).
Usage example can be found [here](https://github.com/jbmattos/CatalystReport/blob/main/catalyst_data_votingresults_example.ipynb).

### Catalyst Analysis Classes

They build on `catalyst_data_{CatalystStageData}.py` classes to provide several functionalities and methods to analyse overall aspects of specific _Catalyst Funds_ and the _Catalyst Project_ in all its fundings.\
This repository offers the following analysis classes:

#### 1. Catalyst Fund Analysis ([CatalystFund](https://github.com/jbmattos/CatalystReport/blob/main/catalyst_fund.py))
This class provides information, statistics and plot analysis related to an specific Catalyst _Fund_. \
Usage information on the available properties and methods can be found in this [example notebook](https://github.com/jbmattos/CatalystReport/blob/main/catalyst_fund_example.ipynb).

**To run an complete report on a specific Fund:**
```
>>python catalyst_fund.py --h

usage: catalyst_fund.py [-h] --fund {f3,f4,f5,f6,f7,f8}

Catalyst Fund Analysis & Report: Generate data analysis report on specific Catalyst Funds

required arguments:
  --fund {f3,f4,f5,f6,f7,f8}
                        Catalyst Fund to provide a report on.

```
> Running the `catalyst_fund.py` automatically creates an `report_CatalystFund-{fund}_{datestamp}/` folder containing several analysis files.

#### 2. Catalyst Project Analysis ([CatalystProjectReport](https://github.com/jbmattos/CatalystReport/blob/main/catalyst_project_report.py))
This class provides information, statistics and plot analysis related to all Funds of _Project Catalyst_. \
Usage information on the available properties and methods can be found in this [example notebook](https://github.com/jbmattos/CatalystReport/blob/main/catalyst_project_report_example.ipynb).

**To run an complete report on a specific Fund:**
```
catalyst_project_report.py usage
(to be implemented)
```
> Running the `catalyst_project_report.py` automatically creates an `report_projectCatalyst_{datestamp}/` folder containing several analysis files.
