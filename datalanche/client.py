# -*- coding: utf-8 -*-

import json
import requests
import collections
import urllib
from StringIO import StringIO
from exception import DLException
from collections import OrderedDict
from requests.auth import HTTPBasicAuth

def get_body(query=None):
    return query.params
   
# For POST, all parameters are in the body so that they are also encrypted.  
# For example, the WHERE clause may have unique identifiers, plain-text
# passwords, and other potentially sensitive information.
def get_url(query=None):
    if (query == None):
        return '/'
    url = query.url
    parameters = OrderedDict()
    query_str = None
    if (url == '/drop_table' or url == '/get_table_info'):
        query_str = urllib.urlencode(query.params['table_name'])
    if (query_str != None):
        url += '?' + query_str
    return url

class DLClient(object):
    def __init__(self, key='', secret='', 
                 host=None, port=None, verify_ssl=True):
        self.auth_key = key
        self.auth_secret = secret
        self.client = requests.Session()
        self.url = 'https://api.datalanche.com'
        self.verify_ssl = verify_ssl
        if host != None:
            self.url = 'https://' + host
        if port != None:
            self.url = self.url + ':' + str(port)
            
    def key (self, key=None):
        self.auth_key = key
        
    def secret (self, secret=None):
        self.auth_secret = secret

    def get_debug_info(self,r):
        info_obj = collections.OrderedDict()
        info_obj ['request']= collections.OrderedDict()
        info_obj ['response'] = collections.OrderedDict()
        info_obj ['request']['method'] = r.request.method
        info_obj ['request']['url'] = r.request.url
        info_obj ['request']['headers'] = r.request.headers
        info_obj ['request']['body'] = r.request.body
        info_obj ['response']['http_status'] = r.status_code
        info_obj ['response']['headers'] = r.headers
        return info_obj
        
    def query(self, q=None):
        if (q == None):
            print "Error: query is None."
            return None
        if not q.url_type:
            r = self.client.post(
                url=self.url + get_url(q),
                auth=HTTPBasicAuth(self.auth_key, self.auth_secret),
                headers={'Content-type':'application/json'},
                data=json.dumps(get_body(q)),
                verify=self.verify_ssl
            )
            result = {}
            debug_info = self.get_debug_info(r)
            if (q.url == '/select_from' or q.url_type == 'get'):
                result['data'] = r.json(
                    object_pairs_hook=collections.OrderedDict
                )            
            result['response'] = debug_info['response']
            result['request'] = debug_info['request']
            if not 200 <= r.status_code < 300:
                raise DLException(r.status_code, r.json(), debug_info)
            return result
        else:
            print "Error: unsupported query type"
