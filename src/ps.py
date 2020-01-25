#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from command_line import CommandLine
import subprocess
import re


class Ps(CommandLine):
    ''' Class to process ps entry and to format the reply '''
    
    def process_without_json(self):
        ''' Process a request without json data in input
            Apply default -ef option
        '''
        if not self.execute_command(['ps', '-ef']):
            if not hasattr(self, 'error'):
                self.error = 400
            return False
        # Post process stdout to extract processes
        stdout = self.result['stdout']
        self.result = {}
        self.result['processes'] = []
        for line in stdout:
            parsed = self.parse_line(line)
            if parsed:
                self.result['processes'].append(parsed)
        return True
        
    def process_with_json(self, json):
        ''' Process a request with json data in input
            Return an error as this is not implemented yet
        '''
        self.error = 400
        return False
        
    def parse_line(self, line):
        ''' Parse a ps line '''
        line = line
        result = {}
        regex = re.compile(r'(?P<uid>[\w\d]+)\s+(?P<pid>\d+)\s+(?P<ppid>\d+)\s+(?P<c>\d+)\s+(?P<stime>[\w\d:]+)\s+(?P<tty>\S+)\s+(?P<time>[\w:]+)\s+(?P<cmd>[\S ]+)')
        match = regex.match(line)
        if match:
            for key in ['uid', 'pid', 'ppid', 'c',
                        'stime', 'tty', 'time', 'cmd']:
                result[key] = match.group(key)
        return result
