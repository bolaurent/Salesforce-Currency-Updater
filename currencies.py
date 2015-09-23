#!/usr/bin/env python

# utility for setting currency conversion rates into salesforce
#
# data should be prepared in a CSV file with two columns, no headers (IsoCode, conversionrate)

# https://developer.salesforce.com/docs/atlas.en-us.api.meta/api/sforce_api_objects_datedconversionrate.htm?search_text=dated
# https://developer.salesforce.com/docs/atlas.en-us.api.meta/api/sforce_api_objects_currencytype.htm?search_text=dated

import simple_salesforce
import datetime
import optparse
import getpass
import csv


parser = optparse.OptionParser("usage: %prog [options] username csvfile")
parser.add_option('-s', action='store_true', default=False, dest='sandbox')
parser.add_option('-d', '--date',
                  dest="date",
                  action = "store",
                  default=str(datetime.date.today()),
                  type="string",
                  )


(options, args) = parser.parse_args()


username = args[0]
csvfile = args[1]


# Read data file

newrates = {}

f = open(csvfile, 'rt')
try:
    reader = csv.reader(f)
    for row in reader:
        assert len(row) == 2, 'data table must have exactly two columns'
        isocode = row[0]
        rate = row[1]
        try:
            float(rate)
        except ValueError:
            assert False, rate + ' is not a float'
        newrates[isocode.upper()] = rate
finally:
    f.close()


# Login to salesforce 

password = getpass.getpass(prompt='password + token, no spaces')
security_token = ''

session_id, instance = simple_salesforce.SalesforceLogin(
                            username=username, 
                            password=password, 
                            security_token=security_token, 
                            sandbox=options.sandbox)

sf = simple_salesforce.Salesforce(instance=instance, session_id=session_id)



# Get a list of the configured currencies

currencies = {} # isocode: id
currencyResult = sf.query("select Id, IsoCode, ConversionRate, DecimalPlaces, IsActive, IsCorporate from CurrencyType")
for r in currencyResult['records']:
    currencies[r['IsoCode']] = r['Id']



# Validate that all the currencies in the data file are also configured in SFDC

for isocode in newrates:
    assert currencies.has_key(isocode), isocode + ' is not a valid currency'

# For each currency in the data file, update both the DatedConversionRate and the CurrencyType
for isocode in newrates:    
    r = sf.CurrencyType.update(currencies[isocode], {'ConversionRate': newrates[isocode]})
    assert(r==204)
    
    r = sf.DatedConversionRate.create({'IsoCode': isocode, 
                                      'ConversionRate': newrates[isocode], 
                                      'StartDate': options.date})
    assert(r['success'])
        
