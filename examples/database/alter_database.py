#! /usr/bin/python
#
# Alter the given database's properties. Must have admin access for the database.
#
# equivalent SQL:
# ALTER DATABASE my_database RENAME TO my_new_database;
#
import json
from datalanche import *
import sys, os

try:

    config = json.load(open(os.path.dirname(os.path.dirname(__file__))+'/config.json'))

    # Please find your API credentials here: https://www.datalanche.com/account before use            
    YOUR_API_KEY = config['api_key']
    YOUR_API_SECRET = config['api_secret']
    
    client = DLClient(key = YOUR_API_KEY, secret = YOUR_API_SECRET)

    q = DLQuery()
    q.alter_database('my_database')
    q.rename_to('my_new_database')
    q.description('my_new_database description text')

    client.query(q)

    print "alter_database succeeded!\n"

except DLException as e:
    print repr(e)
    sys.exit(1)
