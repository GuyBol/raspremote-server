
#! /usr/bin/python
# -*- coding:utf-8 -*-

import unittest
from ps import Ps
from test_executor import RequestMock
from test_command_line import PopenMock


class PsMock(Ps):
    
    def popen(self, command):
        self.executed_command = command
        p = PopenMock()
        p.stdout.append('UID        PID  PPID  C STIME TTY          TIME CMD\n')
        p.stdout.append('root         1     0  0 18:17 ?        00:00:01 /sbin/init splash\n')
        p.stdout.append('tanguy    1662  1133  0 18:18 ?        00:00:00 /usr/lib/x86_64-linux-gnu/indicator-bluetooth/indicator-bluetooth-service\n')
        return p


class TestPs(unittest.TestCase):
    
    def test_process_with_json(self):
        ps = Ps()
        request = RequestMock()
        request.json = {'command': 'ps -ef'}
        self.assertFalse(ps.process(request))
        self.assertEqual(ps.error, 400)
        
    def test_process_and_execute(self):
        ps = PsMock()
        request = RequestMock()
        self.assertTrue(ps.process(request))
        self.assertEqual(ps.executed_command, ['ps', '-ef'])
        #self.assertEqual(commandLine.result, {'stdout': ['line1', 'line2'], 'stderr': ['error1', 'error2']})
        
    def test_parse_first_line(self):
        ps = Ps()
        line = "UID        PID  PPID  C STIME TTY          TIME CMD\n"
        self.assertEqual(ps.parse_line(line), {})
    
    def test_parse_line(self):
        ps = Ps()
        line = "root         1     0  0 18:17 ?        00:00:01 /sbin/init splash\n"
        parsed = ps.parse_line(line)
        self.assertEqual(parsed['uid'], 'root')


if __name__ == '__main__':
    unittest.main()
