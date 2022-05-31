# Catalyst Data storage

**This folder stores raw data from different _stages_ of the Project Catalyst Funds.** \
Each available _Catalyst Stage_ is provided in a `datafiles_{CatalystStageData}/` folder, which contains _CatalystStageData_ from different Funds 
(see the specific folder for data information and sources).

Because the available _Catalyst raw data_ structure may change from Fund to Fund, `loaders_data_{CatalystStageData}.py` files provide Fund-specific methods 
for preprocessing and loading data from different funds. Each loader refers to a _Catalyst Structured Data Class_.

## Adding data of new Funds
To make new Catalyst Funds available to [Catalyst classes](https://github.com/jbmattos/CatalystReport), one should follow the steps:

#### 1. Add the Fund raw data:
Add the new fund raw data file to the respective `datafiles_{CatalystStageData}/`, following the data specifications provided in the folder.\
_IMPORTANT: the current version of this repository can only hadle xlsx files._

#### 2. Edit the loader files:
For each data file added to `datafiles_{CatalystStageData}/`, the `loaders_data_{CatalystStageData}.py` file 
should be edited according to the following steps:

- **Add the data file path:** \
Input the file's reference (key: path) on the `FUNDS_FILES` global variable.

- **Add specific functions to load structured data:** \
Each `loaders_data_{CatalystStageData}.py` file contains groups of mandatory tailored functions to load the structured data from each available fund.
Each group of mandatory functions present a commented heading containing some explanation and a function template to guide the implementation. 
Follow the comments on the specific files for properly adding new fundings to the repository.
