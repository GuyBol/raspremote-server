#! /usr/bin/python
# -*- coding:utf-8 -*-

import unittest
from ls import Ls
from test_executor import RequestMock
from test_command_line import PopenMock



class LsMock(Ls):

    def popen(self, command):
        self.executed_command = command
        p = PopenMock()
        p.stdout.append('total 92\n')
        p.stdout.append('drwxr-xr-x   2 root root  4096 Apr 22  2014 bin\n')
        p.stdout.append('lrwxrwxrwx   1 root root    33 Apr 22  2014 initrd.img -> boot/initrd.img-3.13.0-24-generic\n')
        p.stdout.append('-rw-rw-r-- 1 vagrant vagrant 1949 Dec 31 14:38 test_command_line.py\n')
        return p


class TestPs(unittest.TestCase):

    def test_parse_line_directory(self):
        ls = Ls()
        line = "drwxr-xr-x   2 root root  4096 Apr 22  2014 bin\n"
        parsed = ls.parse_line(line)
        self.assertEqual(parsed['name'], 'bin')
        self.assertEqual(parsed['type'], 'directory')

    def test_parse_line_file(self):
        ls = Ls()
        line = "-rw-rw-r-- 1 vagrant vagrant 1949 Dec 31 14:38 test_command_line.py\n"
        parsed = ls.parse_line(line)
        self.assertEqual(parsed['name'], 'test_command_line.py')
        self.assertEqual(parsed['type'], 'file')

    def test_parse_line_link(self):
        ls = Ls()
        line = "lrwxrwxrwx   1 root root    33 Apr 22  2014 initrd.img -> boot/initrd.img-3.13.0-24-generic\n"
        parsed = ls.parse_line(line)
        self.assertEqual(parsed['name'], 'initrd.img')
        self.assertEqual(parsed['type'], 'link')
        self.assertEqual(parsed['target'], 'boot/initrd.img-3.13.0-24-generic')

    def test_process_and_execute(self):
        self.maxDiff = 1000
        ls = LsMock()
        request = RequestMock()
        request.json = {'path': '/'}
        self.assertTrue(ls.process(request))
        self.assertEqual(ls.executed_command, ['ls', '-l', '/'])
        self.assertEqual(ls.result, {'list': [{'name': 'bin', 'type': 'directory'},
                                              {'name': 'initrd.img',
                                               'target': 'boot/initrd.img-3.13.0-24-generic',
                                               'type': 'link'},
                                              {'name': 'test_command_line.py', 'type': 'file'}]})



if __name__ == '__main__':
    unittest.main()

