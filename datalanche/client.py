# -*- coding: utf-8 -*-

import decimal
import json
import requests
import collections
import urllib
import zlib
from StringIO import StringIO
from exception import DLException
from collections import OrderedDict
from requests.auth import HTTPBasicAuth


def get_body(query = None):

    body = {}
    
    if(query == None):
        return body

    else:
        for keys,values in query.params.items():
            body[keys] = values

    print "the body is: ", body
    return body
        
   
# For POST, all parameters are in the body so that they are also encrypted.
# For example, the WHERE clause may have unique identifiers, plain-text
# passwords, and other potentially sensitive information.
def get_url(query = None):

    if (query == None):
        return '/'
    
    url = query.base_url
    parameters = OrderedDict()
    
    if (url == '/drop_table'):

        if (query.params['table_name'] != None):
            parameters['table_name'] = query.params['table_name']
                   
    elif (url == '/get_table_info'):
        if (query.params['table_name'] != None):
            parameters['table_name'] = query.params['table_name']

        
    elif (url == '/get_table_list'):
        pass
        # do nothing


    query_str = urllib.urlencode(parameters)
   
    if (query_str != ''):
        url += '?' + query_str
    return url


class DLClient(object):
    def __init__(
            self, key = '', secret = '', 
            host = None, port = None, verify_ssl = True
    ):
        self.auth_key = key
        self.auth_secret = secret
        self.client = requests.Session()
        self.url =  'https://api.datalanche.com'
        self.verify_ssl = verify_ssl
        if host != None:
            self.url = 'https://' + host
        if port != None:
            self.url = self.url + ':' + str(port)
            
    def key (self, key = None):
        self.auth_key = key
        
    def secret (self, secret = None):
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

        
    def query(self,q = None):
        
        if (q == None):
            print "Error: query is None."
            return None
            
        if (q.url_type == 'del'):
            r = self.client.delete(
                url = self.url + get_url(q),
                auth = HTTPBasicAuth(self.auth_key, self.auth_secret),
                headers = {'Content-type':'application/json'},
                verify = self.verify_ssl
            )
            
            result = {}
            debug_info = self.get_debug_info(r)
            
            result['response'] = debug_info['response']
            result['request'] = debug_info['request']
        
            
            if not 200 <= r.status_code < 300:
                raise DLException(r.status_code, r.json(), debug_info)
                        
            return result
                        
        elif (q.url_type == 'post'):

            r = self.client.post(
                url = self.url + get_url(q),
                auth = HTTPBasicAuth(self.auth_key, self.auth_secret),
                headers ={'Content-type':'application/json'},
                data = json.dumps(get_body(q)),
                verify = self.verify_ssl
                )

            result = {}
            debug_info = self.get_debug_info(r)
            if (q.base_url == '/select_from'):
                result['data'] = r.json(
                    object_pairs_hook=collections.OrderedDict
                )            
            result['response'] = debug_info['response']
            result['request'] = debug_info['request']
            
            if not 200 <= r.status_code < 300:
                raise DLException(r.status_code, r.json(), debug_info)
          
            return result
                        
                            
        elif (q.url_type == 'get'):

            r = self.client.get(
                url = self.url + get_url(q),
                auth = HTTPBasicAuth(self.auth_key, self.auth_secret),
                headers ={'Content-type':'application/json'},
                data = json.dumps(get_body(q)),
                verify = self.verify_ssl
            )
            
            debug_info = self.get_debug_info(r)
            result = {}

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
