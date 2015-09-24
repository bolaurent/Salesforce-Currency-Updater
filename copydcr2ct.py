#!/usr/bin/env python

# utility for copying latest DatedConversionRate.ConversionRate to CurrencyType.ConversionRate
#

# https://developer.salesforce.com/docs/atlas.en-us.api.meta/api/sforce_api_objects_datedconversionrate.htm?search_text=dated
# https://developer.salesforce.com/docs/atlas.en-us.api.meta/api/sforce_api_objects_currencytype.htm?search_text=dated

import simple_salesforce
import optparse
import getpass


parser = optparse.OptionParser("usage: %prog [options] username csvfile")
parser.add_option('-s', action='store_true', default=False, dest='sandbox')


(options, args) = parser.parse_args()


username = args[0]


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



# For each configured currency, update currencytype from datedconversionrate
for isocode in currencies:
    dcrResult = sf.query("select ConversionRate " +
                         "from DatedConversionRate " +
                         "where IsoCode = '" + isocode + "' " +
                         "order by startdate desc " +
                         "limit 1")
    for r in dcrResult['records']:
        updateResult = sf.CurrencyType.update(currencies[isocode], {'ConversionRate': r['ConversionRate']})
        assert(updateResult==204)
        
