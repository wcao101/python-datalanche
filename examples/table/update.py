#! /usr/bin/python
#
# Update rows in the given table. Must have write access for the given database.
#
# equivalent SQL:
# UPDATE my_schema.my_table SET col3 = 'hello world' WHERE col3 = 'hello';
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

    q = DLQuery(database='my_database')
    q.update('my_schema.my_table')
    q.set({
        'col3': 'hello world'
    })
    q.where(q.expr(q.column('col3'), '=', 'hello'))

    result = client.query(q)

    print json.dumps(result, indent=2)

except DLException as e:
    print repr(e)
    sys.exit(1)
