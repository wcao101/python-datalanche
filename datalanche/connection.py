# -*- coding: utf-8 -*-

import requests

class DLConnection(object):
    def __init__(self):
        self.auth_key = ''
        self.auth_secret = ''
        #self.url = 'http://api.datalanche.com'
        self.url = 'http://localhost:3000'

    def authenticate(self, key, secret):
        self.auth_key = key
        self.auth_secret = secret
        # TODO: perform OAuth
        
    def get_list(self):
        url = self.url + '/list'
        parameters = { 'key': self.auth_key }

        r = requests.get(url, params = parameters)
        if not 200 <= r.status_code < 300:
            raise DLException(r.status_code, r.json(), r.url)
        return r.json()

    def get_schema(self, dataset_name):
        url = self.url + '/' + dataset_name + '/schema'
        parameters = { 'key': self.auth_key }

        r = requests.get(url, params = parameters)
        if not 200 <= r.status_code < 300:
            raise DLException(r.status_code, r.json(), r.url)
        return r.json()

    def read(self, dataset_name, params = None):
        url = self.url + '/' + dataset_name + '/read'

        parameters = { 'key': self.auth_key }

        if params and params.fields != None:
            parameters['fields'] = ','.join(params.fields)
        if params and params.filter != None:
            parameters['filter'] = str(params.filter)
        if params and params.limit != None:
            parameters['limit'] = params.limit
        if params and params.skip != None:
            parameters['skip'] = params.skip
        if params and params.sort != None:
            parameters['sort'] = ','.join(params.sort)
        if params and params.total != None:
            parameters['total'] = str(params.total).lower()

        r = requests.get(url, params = parameters)
        if not 200 <= r.status_code < 300:
            raise DLException(r.status_code, r.json(), r.url)
        return r.json()
