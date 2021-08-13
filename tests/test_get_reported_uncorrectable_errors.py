#!/usr/bin/env python

import json
import unittest

import check_smartctl


class TestGetReportedUncorrectableErrors(unittest.TestCase):
    def setUp(self):
        with open("tests/examples/sda.out", "r") as file:
            self.sda = json.load(file)

    def test_get_reported_uncorrectable_errors(self):
        #
        # Test complete JSON
        #
        output = check_smartctl.get_reported_uncorrectable_errors(self.sda)
        self.assertEqual(output, 104)

        #
        # Test JSON missing ata_device_statistics
        #
        output = check_smartctl.get_reported_uncorrectable_errors([])
        self.assertEqual(output, None)

        #
        # Test JSON missing "General Errors Statistics"
        #
        smartctl = {"ata_device_statistics": {"pages": [{"name": "One"}]}}
        output = check_smartctl.get_reported_uncorrectable_errors(smartctl)
        self.assertEqual(output, None)

        #
        # Test JSON missing "Number of Reported Uncorrectable Errors"
        #
        smartctl = {
            "ata_device_statistics": {
                "pages": [
                    {"name": "General Errors Statistics", "table": [{"name": "Errors"}]}
                ]
            }
        }
        output = check_smartctl.get_reported_uncorrectable_errors(smartctl)
        self.assertEqual(output, None)
