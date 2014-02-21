#! /usr/bin/python
#
# Update rows in the given table. Must have write access for the given database.
#
# equivalent SQL:
# UPDATE my_schema.my_table SET col3 = 'hello world' WHERE col3 = 'hello';
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
