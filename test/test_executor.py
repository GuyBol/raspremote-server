#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import unittest
from executor import Executor


class RequestMock(object):
    def __init__(self):
        self.json = None

class ExecutorMock(Executor):
    
    def __init__(self):
        self.process_without_json_count = 0
        self.process_with_json_count = 0
    
    def process_without_json(self):
        self.process_without_json_count += 1
        return True
    
    def process_with_json(self, json):
        self.process_with_json_count += 1
        return True


class TestExecutor(unittest.TestCase):
    
    def test_process_without_json_called(self):
        executor = ExecutorMock()
        request = RequestMock()
        self.assertTrue(executor.process(request))
        self.assertEqual(executor.process_without_json_count, 1)
    
    def test_process_with_json_called(self):
        executor = ExecutorMock()
        request = RequestMock()
        request.json = {'test': 'test'}
        self.assertTrue(executor.process(request)) 
        self.assertEqual(executor.process_with_json_count, 1)
    
    def test_process_without_json_not_implemented(self):
        executor = Executor()
        request = RequestMock()
        self.assertFalse(executor.process(request))
        self.assertEqual(executor.error, 400)
    
    def test_process_with_json_not_expected(self):
        executor = Executor()
        request = RequestMock()
        request.json = {'test': 'test'}
        self.assertFalse(executor.process(request))
        self.assertEqual(executor.error, 400)
        
        
if __name__ == '__main__':
    unittest.main()
