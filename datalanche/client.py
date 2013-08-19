# -*- coding: utf-8 -*-

import decimal
import json
import requests
import collections
import urllib
from exception import DLException
from requests.auth import HTTPBasicAuth


class DLClient(object):
    def __init__(
        self, key = '', secret = '', 
        host = None, port = None, verify_ssl = True
    ):
        self.auth_key = key
        self.auth_secret = secret
        self.client = requests.Session()
        self.url = 'https://api.datalanche.com'
        self.verify_ssl = verify_ssl
        if host != None:
            self.url = 'https://' + host
        if port != None:
            self.url = self.url + ':' + str(port)

    def query(self,q = None):
        
        if (q == None):
           pirnt"Error: query is None."
           return self
           
        if (q.params['url_type'] == 'del'):
            self.client.delete(
            get_url(q),
            auth = HTTPBasicAuth(self.auth_key, self.auth_secret),
            verify = self.verify_ssl
            )

        elif (q.params['url_type'] = 'post'):
            self.client.post(
            get_url(q),
            get_body(q),
            auth = HTTPBasicAuth(self.auth_key, self.auth_secret),
            verify = self.verify_ssl
            )
            
        elif (q.params['url_type'] = 'get'):
            self.client.get(
            get_url(q),
            auth = HTTPBasicAuth(self.auth_key, self.auth_secret),
            verify = self.verify_ssl
            )

        else:
            raise DLException(r.status_code, r.json(), r.url)

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

        if(query.params['name'] != None):
            body['name'] = query.params['name']
            
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
        
        if (query.params['name'] != None):
            body['name'] = query.params['name']
        
        if (query.params['description'] != None):
            body['description'] = query.params['description']
                
        if (query.params['is_private'] != None) 
            body['is_private'] = query.params['is_private']
        
        if (query.params['license'] != None) 
            body['license'] = query.params['license']
        
        if (query.params['sources'] != None):
            body['sources'] = query.params['sources']
            
    else if (query.base_url == '/delete_from':

        if (query.params['name'] != None):
            body['name'] = query.params['name']
        
        if (query.params['where'] != None): 
            body['where'] = query.params['where']
        
    else if (query.base_url == '/insert_into'):

        if (query.params['name'] != None):
            body['name'] = query.params['name']
        
        if (query.params['values'] != None):
            body['values'] = query.params['values']
        
    else if (query.base_url == '/select_from'):

        if (query.params['distinct'] != None):
            body['distinct'] = query.params['distinct']
        
        if (query.params['from_table'] != None):
            body['from'] = query.params['from_table']
        
        if (query.params['groupBy'] != None):
            body['group_by'] = query.params['groupBy']
        
        if (query.params['limit'] != None):
            body['limit'] = query.params['limit']
        
        if (query.params['offset'] != None):
            body['offset'] = query.params['offset']
        
        if (query.params['orderBy'] != None):
            body['order_by'] = query.params['orderBy']
        
        if (query.params['select'] != None):
            body['select'] = query.params['select']
        
        if (query.params['total'] != None):
            body['total'] = query.params['total']
        
        if (query.params['where'] != None):
            body['where'] = query.params['where']
        
    else if (query.base_url == '/update'):

        if (query.params['name'] != None):
            body['name'] = query.params['name']
        
        if (query.params['set'] != None):
            body['set'] = query.params['set']
        
        if (query.where != None):
            body['where'] = query.params['where']
        
    return self
# For POST, all parameters are in the body so that they are also encrypted.
# For example, the WHERE clause may have unique identifiers, plain-text
# passwords, and other potentially sensitive information.
def getUrl(query):

    if (query == None):
        return '/'
    
    url = query.base_url
    parameters = {}

    if (query.params['debug'] != None):
        parameters['debug'] = query.params['debug']
    
    if (url == '/drop_table'):
        if (query.parmas['name'] != None):
            parameters['name'] = query.params['name']
        
    elif (url == '/get_table_info'):
        if (query.params['name'] != None):
            parameters['name'] = query.params['name']
        
    else if (url == '/get_table_list'):
        # do nothing

    # URL encode parameters
    query_str = urllib.urlencode(parameters)
    if (not query_str):
        url += '?' + query_str
    
    return url
