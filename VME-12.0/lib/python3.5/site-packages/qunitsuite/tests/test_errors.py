# -*- coding: utf-8 -*-
import unittest

from ..suite import QUnitSuite

from utils import path_to

class TestErrors(unittest.TestCase):
    def test_notfound(self):
        result = unittest.TestResult()
        suite = QUnitSuite('bullshit_file.html')
        suite(result)

        self.assertEqual(result.skipped, [])
        self.assertEqual(result.testsRun, 1)
        self.assertEqual(result.failures, [])
        self.assertEqual(len(result.errors), 1)
        test, message = result.errors[0]
        self.assertEqual(str(test), "phantomjs: startup")
        self.assertTrue(message.startswith("PhantomJS unable to load "))

    def test_timeout(self):
        result = unittest.TestResult()
        # lower timeout to not blow up test suite runtime worse than now
        suite = QUnitSuite(path_to('timeout.html'), timeout=500)
        suite(result)

        self.assertEqual(result.skipped, [])
        self.assertEqual(result.testsRun, 1)
        self.assertEqual(result.failures, [])
        self.assertEqual(len(result.errors), 1)
        test, message = result.errors[0]
        self.assertEqual(str(test), "phantomjs: startup")
        self.assertTrue(message.startswith("PhantomJS timed out"))
