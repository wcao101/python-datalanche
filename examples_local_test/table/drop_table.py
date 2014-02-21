#! /usr/bin/python
#
# Drop the given table. Must have admin access for the given database.
#
# equivalent SQL:
# DROP TABLE my_schema.my_table CASCADE;
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
    q.drop_table('my_schema.my_table')
    q.cascade(True)

    client.query(q)

    print "drop_table succeeded!\n"

except DLException as e:
    print repr(e)
    sys.exit(1)
