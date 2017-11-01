
#! /usr/bin/python
# -*- coding:utf-8 -*-

import unittest
from command_line import CommandLine
from test_executor import RequestMock


class PopenMock(object):
    def __init__(self):
        self.stdout = []
        self.stderr = []


class CommandLineMock(CommandLine):
    
    def popen(self, command):
        self.executed_command = command
        p = PopenMock()
        p.stdout.append('line1')
        p.stdout.append('line2')
        p.stderr.append('error1')
        p.stderr.append('error2')        
        return p


class TestCommandLine(unittest.TestCase):
    
    def test_process_without_json(self):
        commandLine = CommandLine()
        request = RequestMock()
        self.assertFalse(commandLine.process(request))
        self.assertEqual(commandLine.error, 400)
    
    def test_extract_command(self):
        commandLine = CommandLine()
        json = {'command': 'ps -ef'}
        self.assertEqual(commandLine.extract_command(json), ['ps', '-ef'])
    
    def test_bad_json(self):
        commandLine = CommandLine()
        json = {'not_a_program': 'never_mind'}
        self.assertFalse(commandLine.extract_command(json))
    
    def test_process_and_execute(self):
        commandLine = CommandLineMock()
        request = RequestMock()
        request.json = {'command': 'ps -ef'}
        self.assertTrue(commandLine.process(request))
        self.assertEqual(commandLine.executed_command, ['ps', '-ef'])
        self.assertEqual(commandLine.result, {'stdout': ['line1', 'line2'], 'stderr': ['error1', 'error2']})
    
    def test_process_error(self):
        commandLine = CommandLineMock()
        request = RequestMock()
        request.json = {'not_a_program': 'never_mind'}
        self.assertFalse(commandLine.process(request))
        self.assertFalse(hasattr(commandLine, 'executed_command'))
        self.assertEqual(commandLine.error, 400)
        

if __name__ == '__main__':
    unittest.main()
