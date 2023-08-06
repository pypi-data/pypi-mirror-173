__author__ = 'kmadac'

import os
import bitstamp.client
import logging

logging.basicConfig(level=logging.DEBUG)

try:
    bc = bitstamp.client.Trading(username=os.environ['bs_user'],
                                 key=os.environ['bs_key'],
                                 secret=os.environ['bs_secret'])
except bitstamp.client.BitstampError:
    pass

print(bc.account_balance())
#print(bc.all_open_orders())

