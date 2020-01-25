#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from command_line import CommandLine
import re



class Ls(CommandLine):
    ''' Class to process ls entry and to format the reply '''

    def process_with_json(self, json):
        ''' Process a request with json data in input '''
        if 'path' in json:
            path = json['path']
            if not self.execute_command(['ls', '-l', path]):
                if not hasattr(self, 'error'):
                    self.error = 400
                return False
            # Post process stdout to extract processes
            stdout = self.result['stdout']
            self.result = {}
            self.result['list'] = []
            for line in stdout:
                parsed = self.parse_line(line)
                if parsed:
                    self.result['list'].append(parsed)
            return True

        else:
            self.error = 400
            return False
    
    def parse_line(self, line):
        ''' Parse a ls -l line '''
        result = {}
        regex = re.compile(r'(?P<type>[dl\-])[rwx\-]{9} +\d+ \w+ +\w+ +\d+ \w+ \d+ +[\d:]+ +(?P<name>.*?)( -> (?P<target>.*))?\n')
        match = regex.match(line)
        if match:
            types = {'d': 'directory', '-': 'file', 'l': 'link'}
            if match.group('type') in types:
                result['type'] = types[match.group('type')]
            for key in ['name', 'target']:
                if match.group(key):
                    result[key] = match.group(key)
        else:
            print("Don't match")
        return result
