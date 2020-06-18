#!/usr/bin/env python

import unittest

import check_smartctl


class ArgumentsTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_parse_arguments(self):
        args = check_smartctl.parse_arguments(["--warning-errors", "5"])
        self.assertEqual(args.warning_errors, 5)
