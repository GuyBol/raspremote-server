#!/usr/bin/env python3
# -*- coding:utf-8 -*-


class Executor:
    ''' Base class to execute any query '''
    
    def __init__(self):
        self.result = {}
    
    def process(self, request):
        '''
        Entry point to process a request.
        Return True if processed OK.
        '''
        if not request.json:
            return self.process_without_json()
        else:
            return self.process_with_json(request.json)
    
    def process_without_json(self):
        ''' Process a request without json data in input '''
        # Default implem (set error)
        self.error = 400
        return False
    
    def process_with_json(self, json):
        ''' Process a request with json data in input '''
        # Default implem (set error)
        self.error = 400
        return False
