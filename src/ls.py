#! /usr/bin/python
# -*- coding:utf-8 -*-

from command_line import CommandLine
import re



''' Class to process ls entry and to format the reply '''
class Ls(CommandLine):

    ''' Process a request with json data in input '''
    def process_with_json(self, json):
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
    
    ''' Parse a ls -l line '''
    def parse_line(self, line):
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
            print "Don't match"
        return result
