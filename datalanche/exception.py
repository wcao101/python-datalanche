# -*- coding: utf-8 -*-

class DLException(Exception):
    def __init__(self, status_code, response, url):
        self.status_code = status_code
        self.response = response
        self.url = url
        exception = {
            'status_code': status_code,
            'response': response,
            'url': url
        }
        Exception.__init__(self, exception)
