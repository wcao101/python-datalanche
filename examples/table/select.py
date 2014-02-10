#! /usr/bin/python
#
# Select rows from the given table. Must have read access for the given database.
#
# equivalent SQL:
# SELECT DISTINCT col1, col2
#     FROM my_schema.my_table
#     WHERE col3 LIKE '%hello%'
#     ORDER BY col1 ASC, col2 DESC
#     OFFSET 0 LIMIT 10;
#
import json
from datalanche import *
import sys
import collections

try:

    # Load config.json for setting API_KEY, API_SECRET, host, port and verify_ssh
    # change the settings in config.json before running examples
    config_file = "../../config.json"
    config = json.load(open(config_file), object_pairs_hook=collections.OrderedDict)

    config['verify_ssl'] = config['verify_ssl'].lower()
    if config['verify_ssl'] == '0' or config['verify_ssl'] == 'false':
        config['verify_ssl'] = False
    else:
        config['verify_ssl'] = True

    client = DLClient(key = config['api_key'], 
                      secret = config['api_secret'], 
                      host = config['host'], 
                      port = config['port'], 
                      verify_ssl = config['verify_ssl'])
    
    # or you can also set your API_KEY and API_SECRET to python client like this
    # client = DLClient(key='YOUR_API_KEY', secret='YOUR_API_SECRET')


    q = DLQuery(database='my_database')
    q.select([ 'col1', 'col2' ])
    q.distinct(True)
    q.from_tables('my_schema.my_table')
    q.where(q.expr(q.column('col3'), '$like', '%hello%'))
    q.order_by([
        q.expr(q.column('col1'), '$asc'),
        q.expr(q.column('col2'), '$desc')
    ])
    q.offset(0)
    q.limit(10)

    result = client.query(q)

    print json.dumps(result, indent=2)

except DLException as e:
    print repr(e)
