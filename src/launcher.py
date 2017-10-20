#! /usr/bin/python
# -*- coding:utf-8 -*-

from executor import Executor
import os

''' Class to launch a program in background '''
class Launcher(Executor):
    
    ''' Process a request with json data in input '''
    def process_with_json(self, json):
        command = self.generate_command(json)
        if command:
            return self.execute_command(command)
        else:
            self.error = 400
            return False
    
    ''' Decode the json and generate the command line '''
    def generate_command(self, json):
        if 'program' in json:
            return json['program'] + ' &'
    
    ''' Run the command '''
    def execute_command(self, command):
        os.system(command)
        return True
        
