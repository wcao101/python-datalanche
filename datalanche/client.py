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
        
    if(query.params['debug'] != None):
        body['debug'] = query.params['debug']
        
    if(query.base_url == '/alter_table'):
        
        if(query.params['add_columns'] != None):
            body['add_columns'] = query.params['add_columns']
            
        if(query.params['alter_columns'] != None):
            body['alter_columns'] = query.params['alter_columns']
        
        if(query.params['table_name'] != None):
            body['table_name'] = query.params['table_name']
            
        if(query.params['description'] != None):
            body['description'] = query.params['description']
        
        if(query.params['drop_columns'] != None):
            body['drop_columns'] = query.params['drop_columns']
            
        if(query.params['is_private'] != None):
            body['is_private'] = query.params['is_private']
            
        if(query.params['license'] != None):
            body['license'] = query.params['license']
            
        if(query.params['rename'] != None):
            body['rename'] = query.params['rename']
            
        if(query.params['sources'] != None):
            body['sources'] = query.params['sources']
        
    elif(query.base_url == '/create_table'):
        
        if (query.params['columns'] != None):
            body['columns'] = query.params['columns']
        
        if (query.params['table_name'] != None):
            body['table_name'] = query.params['table_name']
        
        if (query.params['description'] != None):
            body['description'] = query.params['description']
                
        if (query.params['is_private'] != None):
            body['is_private'] = query.params['is_private']
        
        if (query.params['license'] != None):
            body['license'] = query.params['license']
        
        if (query.params['sources'] != None):
            body['sources'] = query.params['sources']
            
    elif (query.base_url == '/delete_from'):

        if (query.params['table_name'] != None):
            body['table_name'] = query.params['table_name']
        
        if (query.params['where'] != None): 
            body['where'] = query.params['where']
        
    elif (query.base_url == '/insert_into'):

        if (query.params['table_name'] != None):
            body['table_name'] = query.params['table_name']
                    
        if (query.params['values'] != None):
            body['values'] = query.params['values']
        
    elif (query.base_url == '/select_from'):
            
        if (query.params['distinct'] != None):
            body['distinct'] = query.params['distinct']
        
        if (query.params['from_table'] != None):
            body['from'] = query.params['from_table']
        
        if (query.params['group_by'] != None):
            body['group_by'] = query.params['group_by']
        
        if (query.params['limit'] != None):
            body['limit'] = query.params['limit']
        
        if (query.params['offset'] != None):
            body['offset'] = query.params['offset']
        
        if (query.params['order_by'] != None):
            body['order_by'] = query.params['order_by']
        
        if (query.params['select'] != None):
                body['select'] = query.params['select']
        
        if (query.params['total'] != None):
            body['total'] = query.params['total']
            
        if (query.params['where'] != None):
            body['where'] = query.params['where']
                       
    elif (query.base_url == '/update'):

        if (query.params['table_name'] != None):
            body['table_name'] = query.params['table_name']
        
        if (query.params['set'] != None):
            body['set'] = query.params['set']
                                
        if (query.params['where'] != None):
            body['where'] = query.params['where']
           
    return body
        
   
# For POST, all parameters are in the body so that they are also encrypted.
# For example, the WHERE clause may have unique identifiers, plain-text
# passwords, and other potentially sensitive information.
def get_url(query = None):

    if (query == None):
        return '/'
    
    url = query.base_url
    parameters = OrderedDict()

    
    if (query.params['debug'] != None):
        parameters['debug'] = query.params['debug']
    
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
        print "the query_str is: ", query_str
        print "\n"
        url += '?' + query_str
    
    #printnt "the url and the query_str is: ", url
    return url

def get_debug_info(r,base_url):
   
    info_obj = collections.OrderedDict()
    info_obj ['request']= collections.OrderedDict()
    info_obj ['response'] = collections.OrderedDict()
    info_obj ['data'] = {}
    
    info_obj ['request']['method'] = r.request.method
    info_obj ['request']['url'] = r.request.url
    info_obj ['request']['headers'] = r.request.headers
    info_obj ['request']['body'] = r.request.body
    
    info_obj ['response']['http_status'] = r.status_code
    info_obj ['response']['headers'] = r.headers

    if (r.request.method == 'POST' or r.request.method == 'DELETE'):
        if (base_url == '/select_from'):
            info_obj ['data'] = r.json(object_pairs_hook=collections.OrderedDict)
        else:
            pass
    else:
        info_obj ['data'] = r.json(object_pairs_hook=collections.OrderedDict)

    return info_obj

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
            debug_info = get_debug_info(r,q.base_url)
            
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
            debug_info = get_debug_info(r,q.base_url)
            if (q.base_url == '/select_from'):
                result['data'] = r.json(object_pairs_hook=collections.OrderedDict)
            
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
                verify = self.verify_ssl
            )
            
            debug_info = get_debug_info(r,q.base_url)
            result = {}

            result['data'] = r.json(object_pairs_hook=collections.OrderedDict)
            result['response'] = debug_info['response']
            result['request'] = debug_info['request']

            
            if not 200 <= r.status_code < 300:
                raise DLException(r.status_code, r.json(), debug_info)
           
            return result
                
        else:
            print "Error: unsupported query type"
