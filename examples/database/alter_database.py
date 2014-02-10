#! /usr/bin/python
#
# Alter the given database's properties. Must have admin access for the database.
#
# equivalent SQL:
# ALTER DATABASE my_database RENAME TO my_new_database;
#
import json
from datalanche import *
import sys

try:

    # Load config.json for setting API_KEY, API_SECRET, host, port and verify_ssh
    # change the settings in config.json before running examples
    config = json.load(open("../../config.json"))

    # Please change YOUR_API_KEY and YOUR_API_SECRET before use
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
