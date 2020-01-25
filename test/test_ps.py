#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import unittest
from ps import Ps
from test_executor import RequestMock
from test_command_line import PopenMock


class PsMock(Ps):
    
    def popen(self, command):
        self.executed_command = command
        p = PopenMock()
        p.stdout.append('UID        PID  PPID  C STIME TTY          TIME CMD\n'.encode())
        p.stdout.append('root         1     0  0 18:17 ?        00:00:01 /sbin/init splash\n'.encode())
        p.stdout.append('tanguy    1662  1133  0 18:18 ?        00:00:00 /usr/lib/x86_64-linux-gnu/indicator-bluetooth/indicator-bluetooth-service\n'.encode())
        return p


class TestPs(unittest.TestCase):
    
    def test_process_with_json(self):
        ps = Ps()
        request = RequestMock()
        request.json = {'command': 'ps -ef'}
        self.assertFalse(ps.process(request))
        self.assertEqual(ps.error, 400)
        
    def test_process_and_execute(self):
        self.maxDiff = 1000
        ps = PsMock()
        request = RequestMock()
        self.assertTrue(ps.process(request))
        self.assertEqual(ps.executed_command, ['ps', '-ef'])
        self.assertEqual(ps.result, {'processes':
                                        [
                                            {
                                                'uid': 'root',
                                                'pid': '1',
                                                'ppid': '0',
                                                'c': '0',
                                                'stime': '18:17',
                                                'tty': '?',
                                                'time': '00:00:01',
                                                'cmd': '/sbin/init splash'
                                            },
                                            {
                                                'uid': 'tanguy',
                                                'pid': '1662',
                                                'ppid': '1133',
                                                'c': '0',
                                                'stime': '18:18',
                                                'tty': '?',
                                                'time': '00:00:00',
                                                'cmd': '/usr/lib/x86_64-linux-gnu/indicator-bluetooth/indicator-bluetooth-service'
                                            }
                                        ]
                                    })
        
    def test_parse_first_line(self):
        ps = Ps()
        line = "UID        PID  PPID  C STIME TTY          TIME CMD\n"
        self.assertEqual(ps.parse_line(line), {})
    
    def test_parse_line(self):
        ps = Ps()
        line = "tanguy    1662  1133  0 18:18 ?        00:00:00 /usr/lib/x86_64-linux-gnu/indicator-bluetooth/indicator-bluetooth-service\n"
        parsed = ps.parse_line(line)
        self.assertEqual(parsed['uid'], 'tanguy')
        self.assertEqual(parsed['pid'], '1662')
        self.assertEqual(parsed['ppid'], '1133')
        self.assertEqual(parsed['c'], '0')
        self.assertEqual(parsed['stime'], '18:18')
        self.assertEqual(parsed['tty'], '?')
        self.assertEqual(parsed['time'], '00:00:00')
        self.assertEqual(parsed['cmd'], '/usr/lib/x86_64-linux-gnu/indicator-bluetooth/indicator-bluetooth-service')


if __name__ == '__main__':
    unittest.main()
