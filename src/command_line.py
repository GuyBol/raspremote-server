#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import request, jsonify
import subprocess
import os


''' Class to process a command line request '''
class CommandLine(object):
    
    def __init__(self):
        self.error = 200
    
    def process(self, req):
        if not 'command' in request.json:
            return False
        command = request.json['command']
        self.result = self.execute(command)
        return True
    
    def execute(self, command):
        splitted = command.split(' ')
        retDict = {}
        # Use Popen in most cases, except if query to run in background (ending with &)
        if splitted[-1][-1] != '&':
            p = subprocess.Popen(splitted, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            if p.stdout:
                stdout = []
                for line in p.stdout:
                    stdout.append(line)
                retDict['stdout'] = stdout
            if p.stderr:
                stderr = []
                for line in p.stderr:
                    stderr.append(line)
                retDict['stderr'] = stderr
        else:
            # Query to run in background
            os.system(command)
        return jsonify(retDict)
