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
    config = json.load(open("../config.json"))
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


    q = DLQuery(database='my_database')
    q.select_all().from_tables('my_schema.my_table').search('hello world')

    result = client.query(q)

    print json.dumps(result, indent=2)

except DLException as e:
    print repr(e)
    sys.exit(1)
