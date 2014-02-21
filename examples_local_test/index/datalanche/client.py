# -*- coding: utf-8 -*-

import json
import requests
import collections
import urllib
from .exception import DLException
from requests.auth import HTTPBasicAuth

class DLClient(object):
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

    def key(self, key):
        self.auth_key = key

    def secret(self, secret):
        self.auth_secret = secret

    def get_debug_info(self, r):
        info = collections.OrderedDict()

        info['request'] = collections.OrderedDict()
        info['request']['method'] = r.request.method
        info['request']['url'] = r.request.url
        info['request']['headers'] = r.request.headers
        info['request']['body'] = r.request.body

        info['response'] = collections.OrderedDict()
        info['response']['http_status'] = r.status_code
        info['response']['headers'] = r.headers

        return info
        
    def query(self, q = None):
        if q == None:
            raise Exception('query == None')

        params = collections.OrderedDict(q.params)

        url = self.url
        if 'database' in params:
            url = url + '/' + urllib.quote_plus(str(params['database']))
            del params['database']
        url = url + '/query'

        r = self.client.post(
            url = url,
            auth = HTTPBasicAuth(self.auth_key, self.auth_secret),
            headers = {
                'Accept-Encoding': 'gzip',
                'Content-Type': 'application/json',
                'User-Agent': 'Datalanche Python Client'
            },
            data = json.dumps(params),
            verify = self.verify_ssl
        )

        result = collections.OrderedDict()
        debug_info = self.get_debug_info(r)

        try:
            result['data'] = r.json(object_pairs_hook = collections.OrderedDict)            
        except Exception as e:
            result['data'] = None

        result['response'] = debug_info['response']
        result['request'] = debug_info['request']

        if not 200 <= r.status_code < 300:
            raise DLException(r.status_code, result['data'], debug_info)

        return result

