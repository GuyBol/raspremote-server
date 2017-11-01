#! /usr/bin/python
# -*- coding:utf-8 -*-

import unittest
from launcher import Launcher
from test_executor import RequestMock


class LauncherMock(Launcher):
    
    def execute_command(self, command):
        self.executed_command = command
        return True


class TestLauncher(unittest.TestCase):
    
    def test_process_without_json(self):
        launcher = Launcher()
        request = RequestMock()
        self.assertFalse(launcher.process(request))
        self.assertEqual(launcher.error, 400)
    
    def test_generate_command(self):
        launcher = Launcher()
        json = {'program': 'kodi'}
        self.assertEqual(launcher.generate_command(json), 'kodi &')
    
    def test_bad_json(self):
        launcher = Launcher()
        json = {'not_a_program': 'never_mind'}
        self.assertFalse(launcher.generate_command(json))
    
    def test_process_and_execute(self):
        launcher = LauncherMock()
        request = RequestMock()
        request.json = {'program': 'kodi'}
        self.assertTrue(launcher.process(request))
        self.assertEqual(launcher.executed_command, 'kodi &')
    
    def test_process_error(self):
        launcher = LauncherMock()
        request = RequestMock()
        request.json = {'not_a_program': 'never_mind'}
        self.assertFalse(launcher.process(request))
        self.assertFalse(hasattr(launcher, 'executed_command'))
        self.assertEqual(launcher.error, 400)
        

if __name__ == '__main__':
    unittest.main()
