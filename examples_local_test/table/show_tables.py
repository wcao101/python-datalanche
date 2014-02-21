#! /usr/bin/python
#
# Show all tables you have access to.
#
import json
import os
import sys
from datalanche import *

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

    q = DLQuery()
    q.show_tables(database = 'my_database')

    result = client.query(q)

    print json.dumps(result, indent=2)

except DLException as e:
    print repr(e)
    sys.exit(1)
