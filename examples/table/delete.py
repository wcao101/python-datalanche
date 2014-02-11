#! /usr/bin/python
#
# Delete rows from the given table. Must have write access for the given database.
#
# equivalent SQL:
# DELETE FROM my_schema.my_table WHERE col3 = 'hello';
#
import json
from datalanche import *
import sys

try:

    config = json.load(open("../../config.json"))

    # Please found your API credentials here: datalanche.com/account/login before use
    YOUR_API_KEY = config['api_key']
    YOUR_API_SECRET = config['api_secret']
    
    client = DLClient(key = YOUR_API_KEY, secret = YOUR_API_SECRET)

    q = DLQuery(database='my_database')
    q.delete_from('my_schema.my_table')
    q.where(q.expr(q.column('col3'), '=', 'hello'));

    result = client.query(q)

    print json.dumps(result, indent=2)

except DLException as e:
    print repr(e)
    sys.exit(1)
