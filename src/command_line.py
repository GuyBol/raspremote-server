#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from executor import Executor
import subprocess


class CommandLine(Executor):
    ''' Class to process a command line request '''

    def process_with_json(self, json):
        ''' Process a request with json data in input '''
        command = self.extract_command(json)
        if command:
            return self.execute_command(command)
        else:
            if not hasattr(self, 'error'):
                self.error = 400
            return False

    def extract_command(self, json):
        if 'command' in json:
            return json['command'].split(' ')

    def execute_command(self, command):
        p = self.popen(command)
        if hasattr(self, 'error'):
            return False
        if p.stdout:
            stdout = []
            for line in p.stdout:
                stdout.append(line.decode('utf-8'))
            self.result['stdout'] = stdout
        if p.stderr:
            stderr = []
            for line in p.stderr:
                stderr.append(line.decode('utf-8'))
            self.result['stderr'] = stderr
        return True

    def popen(self, command):
        try:
            return subprocess.Popen(command, stdout=subprocess.PIPE,
                                    stderr=subprocess.STDOUT)
        except:
            self.error = 500
