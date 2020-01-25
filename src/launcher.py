#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from executor import Executor
import os

class Launcher(Executor):
    ''' Class to launch a program in background '''
    
    def process_with_json(self, json):
        ''' Process a request with json data in input '''
        command = self.generate_command(json)
        if command:
            return self.execute_command(command)
        else:
            self.error = 400
            return False
    
    def generate_command(self, json):
        ''' Decode the json and generate the command line '''
        if 'program' in json:
            return json['program'] + ' &'
    
    def execute_command(self, command):
        ''' Run the command '''
        os.system(command)
        return True
        
