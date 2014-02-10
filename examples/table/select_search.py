#! /usr/bin/python
#
# Search the table and retrieve the rows. Must have read access for the given database.
#
# equivalent SQL:
# SELECT * FROM my_schema.my_table WHERE SEARCH 'hello world';
#
# NOTE: Search clause is sent to ElasticSearch. The search
# results are used as a filter when executing the SQL query.
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


    q = DLQuery(database='my_database')
    q.select_all().from_tables('my_schema.my_table').search('hello world')

    result = client.query(q)

    print json.dumps(result, indent=2)

except DLException as e:
    print repr(e)
    sys.exit(1)
