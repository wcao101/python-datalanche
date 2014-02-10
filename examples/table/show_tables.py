#! /usr/bin/python
#
# Show all tables you have access to.
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
    q.show_tables()

    result = client.query(q)

    print json.dumps(result, indent=2)

except DLException as e:
    print repr(e)
