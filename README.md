# CatalystReport
A report on the Catalyst Funds 

## catalyst_assessments.py
Class to load and provide information on the Assessments related to an specific Fund. \
The Funds and data available can be found [here](https://github.com/jbmattos/CatalystReport/tree/main/data/datafiles_assessments).\
The [loaders_assessments](https://github.com/jbmattos/CatalystReport/blob/main/data/loaders_assessments.py) file contains the tailored methods to read data from different funds.\
Usage information can be found in this [example](https://github.com/jbmattos/CatalystReport/blob/main/example_catalyst_assessments.ipynb).

## catalyst_votingresults.py
Class to load and provide information on the Voting Results related to an specific Fund. \
The Funds and data available can be found [here](https://github.com/jbmattos/CatalystReport/tree/main/data/datafiles_votingresults).\
The [loaders_votingresults](https://github.com/jbmattos/CatalystReport/blob/main/data/loaders_votingresults.py) file contains the tailored methods to read data from different funds.\
Usage information can be found in this [example](https://github.com/jbmattos/CatalystReport/blob/main/example_catalyst_votingresults.ipynb)

## catalyst_fund_eda.py
Class developed to use `catalyst_assessments` and `catalyst_votingresults` structured data and provide statistics and plot analysis related to an specific Fund.\
(still under development)
Usage information can be found in this [example](https://github.com/jbmattos/CatalystReport/blob/main/example_catalyst_fund_eda.ipynb)

## catalyst_report.py
(Not implemented yet)
