#! /usr/bin/python
#
# Join multiple tables and retrieve the rows. Must have read access for the given database.
#
# equivalent SQL:
# SELECT * FROM t1
#     JOIN t2 ON t1.c1 = t2.c1
#     JOIN t3 ON t1.c1 = t3.c1;
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
    q.select_all()
    q.from_tables(q.expr(
        q.table('t1'),
        '$join', q.table('t2'), '$on', q.column('t1.c1'), '=', q.column('t2.c1'),
        '$join', q.table('t3'), '$on', q.column('t1.c1'), '=', q.column('t3.c1')
    ))

    result = client.query(q)

    print json.dumps(result, indent=2)

except DLException as e:
    print repr(e)
