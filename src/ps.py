#! /usr/bin/python
# -*- coding:utf-8 -*-

from command_line import CommandLine
import subprocess
import re


''' Class to process ps entry and to format the reply '''
class Ps(CommandLine):
    
    ''' Process a request without json data in input
        Apply default -ef option
    '''
    def process_without_json(self):
        return self.execute_command(['ps', '-ef'])
        
    ''' Process a request with json data in input
        Return an error as this is not implemented yet
    '''
    def process_with_json(self, json):
        self.error = 400
        return False
        
    ''' Parse a ps line '''
    def parse_line(self, line):
        result = {}
        regex = re.compile(r'(?P<uid>[\w\d]+)\s+(?P<pid>\d+)\s+(?P<ppid>\d+)\s+(?P<c>\d+)\s+(?P<stime>[\w\d:]+)\s+(?P<tty>\S+)\s+(?P<time>[\w:]+)\s+(?P<cmd>\S+)')
        match = regex.match(line)
        if match:
            for key in ['uid', 'pid', 'ppid', 'c', 'stime', 'tty', 'time', 'cmd']:
                result[key] = match.group(key)
        return result
