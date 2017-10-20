#! /usr/bin/python
# -*- coding:utf-8 -*-


''' Base class to execute any query '''
class Executor:
    
    def __init__(self):
        self.result = {}
    
    '''
    Entry point to process a request.
    Return True if processed OK.
    '''
    def process(self, request):
        if not request.json:
            return self.process_without_json()
        else:
            return self.process_with_json(request.json)
    
    ''' Process a request without json data in input '''
    def process_without_json(self):
        # Default implem (set error)
        self.error = 400
        return False
    
    ''' Process a request with json data in input '''
    def process_with_json(self, json):
        # Default implem (set error)
        self.error = 400
        return False
