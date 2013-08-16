# -*- coding: utf-8 -*-

import decimal
import json
import requests
import collections
from exception import DLException
from requests.auth import HTTPBasicAuth

def is_boolean(s):
    if s == True or s == False:
        return True
    return False

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    except TypeError:
        return False

def is_string(s):
    return isinstance(s, basestring)

# handle cases where value may not be a list of strings
def list2str(value):
    newstr = ''

    if is_boolean(value):
        newstr = str(value).lower()
    elif is_number(value) or is_string(value):
        newstr = str(value)
    else:
        for i in range(0, len(value)):
            if is_boolean(value[i]):
                newstr = newstr + str(value[i]).lower()
            else:
                newstr = newstr + str(value[i])

            if i < len(value) - 1:
                newstr = newstr + ','
    
    return newstr

class Client(object):
    def __init__(self, key = '', secret = '', host = None, port = None, verify_ssl = True):
        self.auth_key = key
        self.auth_secret = secret
        self.client = requests.Session()
        self.url = 'https://api.datalanche.com'
        self.verify_ssl = verify_ssl
        if host != None:
            self.url = 'https://' + host
        if port != None:
            self.url = self.url + ':' + str(port)

    def add_columns(self, dataset_name, columns):
        url = self.url + '/add_columns'

        parameters = {}

        if dataset_name != None:
            parameters['dataset'] = dataset_name

        body = {
            'num_columns': len(columns),
            'columns': columns
        }

        r = self.client.post(
            url,
            auth = HTTPBasicAuth(self.auth_key, self.auth_secret),
            headers = {'Content-type': 'application/json'},
            params = parameters,
            data = json.dumps(body),
            verify = self.verify_ssl
        )
        if not 200 <= r.status_code < 300:
            raise DLException(r.status_code, r.json(), r.url)

    def create_dataset(self, schema):
        url = self.url + '/create_dataset'

        r = self.client.post(
            url,
            auth = HTTPBasicAuth(self.auth_key, self.auth_secret),
            headers = {'Content-type': 'application/json'},
            data = json.dumps(schema),
            verify = self.verify_ssl
        )
        if not 200 <= r.status_code < 300:
            raise DLException(r.status_code, r.json(), r.url)

    def delete_dataset(self, dataset_name):
        url = self.url + '/delete_dataset'

        parameters = {}

        if dataset_name != None:
            parameters['dataset'] = dataset_name

        r = self.client.delete(
            url,
            auth = HTTPBasicAuth(self.auth_key, self.auth_secret),
            params = parameters,
            verify = self.verify_ssl
        )
        if not 200 <= r.status_code < 300:
            raise DLException(r.status_code, r.json(), r.url)

    def delete_records(self, dataset_name, query_filter = None):
        url = self.url + '/delete_records'

        parameters = {}

        if dataset_name != None:
            parameters['dataset'] = dataset_name
        if query_filter != None:
            parameters['filter'] = str(query_filter)

        r = self.client.delete(
            url,
            auth = HTTPBasicAuth(self.auth_key, self.auth_secret),
            params = parameters,
            verify = self.verify_ssl
        )
        if not 200 <= r.status_code < 300:
            raise DLException(r.status_code, r.json(), r.url)

    def get_dataset_list(self):
        url = self.url + '/get_dataset_list'

        r = self.client.get(
            url,
            auth = HTTPBasicAuth(self.auth_key, self.auth_secret),
            verify = self.verify_ssl
        )
        if not 200 <= r.status_code < 300:
            raise DLException(r.status_code, r.json(), r.url)
        return r.json(object_pairs_hook=collections.OrderedDict)

    def get_schema(self, dataset_name):
        url = self.url + '/get_schema'

        parameters = {}

        if dataset_name != None:
            parameters['dataset'] = dataset_name

        r = self.client.get(
            url,
            auth = HTTPBasicAuth(self.auth_key, self.auth_secret),
            params = parameters,
            verify = self.verify_ssl
        )
        if not 200 <= r.status_code < 300:
            raise DLException(r.status_code, r.json(), r.url)
        return r.json(object_pairs_hook=collections.OrderedDict)

    def insert_records(self, dataset_name, records):
        url = self.url + '/insert_records'

        parameters = {}

        if dataset_name != None:
            parameters['dataset'] = dataset_name

        body = {
            'num_records': len(records),
            'records': records
        }

        r = self.client.post(
            url,
            auth = HTTPBasicAuth(self.auth_key, self.auth_secret),
            headers = {'Content-type': 'application/json'},
            params = parameters,
            data = json.dumps(body),
            verify = self.verify_ssl
        )
        if not 200 <= r.status_code < 300:
            raise DLException(r.status_code, r.json(), r.url)

    def read_records(self, dataset_name, params = None):
        url = self.url + '/read_records'

        parameters = {}

        if dataset_name != None:
            parameters['dataset'] = dataset_name
        if params and params.columns != None:
            parameters['columns'] = list2str(params.columns)
        if params and params.filter != None:
            parameters['filter'] = str(params.filter)
        if params and params.limit != None:
            parameters['limit'] = params.limit
        if params and params.skip != None:
            parameters['skip'] = params.skip
        if params and params.sort != None:
            parameters['sort'] = list2str(params.sort)
        if params and params.total != None:
            parameters['total'] = str(params.total).lower()

        r = self.client.get(
            url,
            auth = HTTPBasicAuth(self.auth_key, self.auth_secret),
            params = parameters,
            verify = self.verify_ssl
        )
        if not 200 <= r.status_code < 300:
            raise DLException(r.status_code, r.json(), r.url)
        return r.json(object_pairs_hook=collections.OrderedDict)

    def remove_columns(self, dataset_name, columns):
        url = self.url + '/remove_columns'

        parameters = {}

        if dataset_name != None:
            parameters['dataset'] = dataset_name
        if columns != None:
            parameters['columns'] = list2str(columns)

        r = self.client.delete(
            url,
            auth = HTTPBasicAuth(self.auth_key, self.auth_secret),
            params = parameters,
            verify = self.verify_ssl
        )
        if not 200 <= r.status_code < 300:
            raise DLException(r.status_code, r.json(), r.url)

    def set_details(self, dataset_name, details):
        url = self.url + '/set_details'

        parameters = {}

        if dataset_name != None:
            parameters['dataset'] = dataset_name

        r = self.client.post(
            url,
            auth = HTTPBasicAuth(self.auth_key, self.auth_secret),
            headers = {'Content-type': 'application/json'},
            params = parameters,
            data = json.dumps(details),
            verify = self.verify_ssl
        )
        if not 200 <= r.status_code < 300:
            raise DLException(r.status_code, r.json(), r.url)

    def update_columns(self, dataset_name, columns):
        url = self.url + '/update_columns'

        parameters = {}

        if dataset_name != None:
            parameters['dataset'] = dataset_name

        r = self.client.post(
            url,
            auth = HTTPBasicAuth(self.auth_key, self.auth_secret),
            headers = {'Content-type': 'application/json'},
            params = parameters,
            data = json.dumps(columns),
            verify = self.verify_ssl
        )
        if not 200 <= r.status_code < 300:
            raise DLException(r.status_code, r.json(), r.url)

    def update_records(self, dataset_name, records, query_filter = None):
        url = self.url + '/update_records'

        parameters = {}

        if dataset_name != None:
            parameters['dataset'] = dataset_name
        if query_filter != None:
            parameters['filter'] = str(query_filter)

        r = self.client.post(
            url,
            auth = HTTPBasicAuth(self.auth_key, self.auth_secret),
            headers = {'Content-type': 'application/json'},
            params = parameters,
            data = json.dumps(records),
            verify = self.verify_ssl
        )
        if not 200 <= r.status_code < 300:
            raise DLException(r.status_code, r.json(), r.url)
