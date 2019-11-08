# -*- coding: utf-8 -*-
import unittest

from ..suite import QUnitSuite

from utils import path_to

class TestSuccess(unittest.TestCase):
    def test_various(self):
        result = unittest.TestResult()
        suite = QUnitSuite(path_to('success.html'))
        suite(result)

        self.assertEqual(result.skipped, [])
        self.assertEqual(result.errors, [])
        self.assertEqual(result.failures, [])
        self.assertEqual(result.testsRun, 6)

class TestFailure(unittest.TestCase):
    def test_various(self):
        result = unittest.TestResult()
        suite = QUnitSuite(path_to('failure.html'))
        suite(result)

        self.assertEqual(result.skipped, [])
        self.assertEqual(result.errors, [])
        self.assertEqual(len(result.failures), 10)
        # used to check messages, but source may be randomly added
        # based on exact phantomjs version so fuck that

        self.assertEqual(result.testsRun, 8)

class TestPolyfills(unittest.TestCase):
    def test_polyfills(self):
        result = unittest.TestResult()
        suite = QUnitSuite(path_to('polyfill.html'))
        suite(result)

        self.assertEqual(result.skipped, [])
        self.assertEqual(result.errors, [])
        self.assertEqual(result.failures, [])
        self.assertEqual(result.testsRun, 1)

