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
                
        if (query.params['is_private'] != None):
            body['is_private'] = query.params['is_private']
        
        if (query.params['license'] != None):
            body['license'] = query.params['license']
        
        if (query.params['sources'] != None):
            body['sources'] = query.params['sources']
            
    elif (query.base_url == '/delete_from'):

        if (query.params['name'] != None):
            body['name'] = query.params['name']
        
        if (query.params['where'] != None): 
            body['where'] = query.params['where']
        
    elif (query.base_url == '/insert_into'):

        if (query.params['name'] != None):
            body['name'] = query.params['name']
        
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

        if (query.params['name'] != None):
            body['name'] = query.params['name']
        
        if (query.params['set'] != None):
            body['set'] = query.params['set']
        
        if (query.params['where'] != None):
            body['where'] = query.params['where']
               
    print json.dumps(body)
    return body
        
   
# For POST, all parameters are in the body so that they are also encrypted.
# For example, the WHERE clause may have unique identifiers, plain-text
# passwords, and other potentially sensitive information.
def get_url(query = None):

    # if (query.base_url ==  '/create_table'):
    #     if ('name' not in query.params.keys()):
    #         print "the there is no name for creating the table"
    #         return None
    #     pass

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
   
    if (query_str != ''):
        print "the query_str is: ", query_str
        print "\n"
        url += '?' + query_str
        
    #print "the url and the query_str is: ", url
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
            r = self.client.delete(
                url = self.url + get_url(q),
                auth = HTTPBasicAuth(self.auth_key, self.auth_secret),
                headers ={'Content-type':'application/json'},
                verify = self.verify_ssl
            )
            if not 200 <= r.status_code < 300:
               raise DLException(r.status_code, r.json(), r.url)

            return r.json(object_pairs_hook=collections.OrderedDict)


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
                
            return r.json(object_pairs_hook=collections.OrderedDict)
                
        elif (q.url_type == 'get'):
            r = self.client.get(
                url = self.url + get_url(q),
                auth = HTTPBasicAuth(self.auth_key, self.auth_secret),
                headers ={'Content-type':'application/json'},
                verify = self.verify_ssl
            )
            if not 200 <= r.status_code < 300:
                raise DLException(r.status_code, r.json(), r.url)
                
            return r.json(object_pairs_hook=collections.OrderedDict)
                
        else:
            raise DLException(r.status_code, r.json(), r.url)
