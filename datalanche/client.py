# -*- coding: utf-8 -*-

import decimal
import json
import requests
import collections
import urllib
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
        
        for i,value in query.params.items():
            ## print "testing...key is: ",i," value is: ",value
            
            if(i == 'add_colunms' and value != None):
                body['add_columns'] = value
            
            if(i == 'alter_columns' and value != None):
                body['alter_columns'] = value

            if(i == 'name' and value != None):
                body['name'] = value
            
            if(i == 'description' and value != None):
                body['description'] = value

            if(i == 'drop_columns' and value != None):
                body['drop_columns'] = value

            if(i == 'is_private' and value != None):
                body['is_private'] = value

            if(i == 'license' and value != None):
                body['license'] = value

            if(i == 'rename' and value != None):
                body['rename'] = value

            if(i == 'sources' and value != None):
                body['sources'] = value
        
    elif(query.base_url == '/create_table'):
        
        for i,value in query.params.items():
            ## print "testing...key is: ",i," value is: ",value

            if (i == 'columns' and value != None):
                body['columns'] = value
        
            if (i == 'name' and value != None):
                body['name'] = value
        
            if (i == 'description' and value != None):
                body['description'] = value
                
            if (i == 'is_private' and value!= None):
                body['is_private'] = value
        
            if (i == 'license' and value != None):
                body['license'] = value
        
            if (i == 'sources' and value != None):
                body['sources'] = value
            
    elif (query.base_url == '/delete_from'):

        for i,value in query.params.items():
            ## print "testing...key is: ",i," value is: ",value

            if (i == 'name' and value != None):
                body['name'] = value
        
            if (i == 'where' and value != None): 
                body['where'] = value
        
    elif (query.base_url == '/insert_into'):

        for i,value in query.params.items():
            ## print "testing...key is: ",i," value is: ",value

            if (i == 'name' and value != None):
                body['name'] = value
        
            if (i == 'values' and value != None):
                body['values'] = value
        
    elif (query.base_url == '/select_from'):

        for i,value in query.params.items():
            ## print "testing...key is: ",i," value is: ",value
            
            if (i == 'distinct' and value != None):
                body['distinct'] = value
        
            if (i == 'from_table' and value != None):
                body['from'] = value
        
            if (i == 'group_by' and value != None):
                body['group_by'] = value
        
            if (i == 'limit' and value != None):
                body['limit'] = value
        
            if (i == 'offset' and value != None):
                body['offset'] = value
        
            if (i == 'order_by' and value != None):
                body['order_by'] = value
        
            if (i == 'select' and value != None):
                body['select'] = value
        
            if (i == 'total' and value != None):
                body['total'] = value
        
            if (i == 'where' and value != None):
                body['where'] = value
        
    elif (query.base_url == '/update'):

        for i,value in query.params.items():
           # print "testing...key is: ",i," value is: ",value

            if (i == 'name' and value != None):
                body['name'] = value
        
            if (i == 'set' and value != None):
                body['set'] = value
        
            if (i == 'where' and value != None):
                body['where'] = value
                
    return body
        
   
# For POST, all parameters are in the body so that they are also encrypted.
# For example, the WHERE clause may have unique identifiers, plain-text
# passwords, and other potentially sensitive information.
def get_url(query):

    if (query == None):
        return '/'
    
    url = query.base_url
    parameters = OrderedDict()

    if (query.params['debug'] != None):
        parameters['debug'] = query.params['debug']
    
    if (url == '/drop_table'):

        if (query.params['name'] != None):
            parameters['name'] = query.params['name']

        
    elif (url == '/get_table_info'):
        if (query.params['name'] != None):
            parameters['name'] = query.params['name']

        
    elif (url == '/get_table_list'):
        pass
        # do nothing


    query_str = urllib.urlencode(parameters)

    if (not query_str):
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

    def query(self,q = None):
       # print "NOW, q.params['rename'] is: ", q.params['rename']
        
        if (q == None):
            print "Error: query is None."
            return None
            
        if (q.url_type == 'del'):
            url = self.url + get_url(q)
            print "the url is: ",url
            r = self.client.delete(
                url = self.url + get_url(q),
                auth = HTTPBasicAuth(self.auth_key, self.auth_secret),
                verify = self.verify_ssl
            )
            if not 200 <= r.status_code < 300:
               raise DLException(r.status_code, r.json(), r.url)


        elif (q.url_type == 'post'):
            r = self.client.post(
                url = self.url + get_url(q),
                auth = HTTPBasicAuth(self.auth_key, self.auth_secret),
                headers ={'Content-type':'application/json'},
                data = json.dumps(get_body(q)),
                verify = self.verify_ssl
            )
            if not 200 <= r.status_code < 300:
                raise DLException(r.status_code, r.json(), r.url)
                
        elif (q.url_type == 'get'):
            r = self.client.get(
                url = self.url + get_url(q),
                auth = HTTPBasicAuth(self.auth_key, self.auth_secret),
                verify = self.verify_ssl
            )
            if not 200 <= r.status_code < 300:
                raise DLException(r.status_code, r.json(), r.url)

        else:
            raise DLException(r.status_code, r.json(), r.url)
