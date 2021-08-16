#!/usr/bin/env python

import json
import unittest

import check_smartctl


class TestGetReportedUncorrectableErrors(unittest.TestCase):
    def setUp(self):
        with open("tests/examples/sda.out", "r") as file:
            self.sda = json.load(file)
        with open("tests/examples/sdb.out", "r") as file:
            self.sdb = json.load(file)

    def test_get_reported_uncorrectable_errors(self):
        #
        # Test complete JSON for ata devices
        #
        output = check_smartctl.get_reported_uncorrectable_errors(self.sda)
        self.assertEqual(output, 104)

        #
        # Test complete JSON for non-ata devices
        #
        output = check_smartctl.get_reported_uncorrectable_errors(self.sdb)
        self.assertEqual(output, 6)

        #
        # Test JSON missing ata_device_statistics and scsi_error_counter_log
        #
        output = check_smartctl.get_reported_uncorrectable_errors([])
        self.assertEqual(output, None)
