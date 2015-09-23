Currency Updater

Basic Usage
-----------

    currencies.py myusername currencies.csv 


Example Usage
--------------

The following will update currencies in the sandbox, setting DatedConversionRates with starting
date 2015-09-20, using data from the csv file 'currencies.csv'.

    currencies.py -s --date 2015-09-20 myusername currencies.csv 


Optional Arguments:
--------------
    -s target a salesforce sandbox
    -d, --date yyyy-mm-dd specify starting date (default is today)

Installation
--------------

This is a python script. Dependencies are as follow:

* simple_salesforce
* datetime
* optparse
* getpass
* csv

