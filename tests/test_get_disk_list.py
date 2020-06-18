#!/usr/bin/env python

import subprocess
import unittest
from mock import patch

import check_smartctl


class TestGetDiskList(unittest.TestCase):

    def setUp(self):
        pass

    @patch('subprocess.check_output')
    def test_get_disk_list(self, mock_check_output):
        #
        # Test no exceptions
        #
        mock_check_output.return_value = "sda\nsdb\nsdc"
        disk_list = check_smartctl.get_disk_list()

        self.assertEqual(disk_list, ["sda", "sdb", "sdc"])

    @patch('subprocess.check_output')
    def test_get_disk_list_exception(self, mock_check_output):
        #
        # Test CalledProcessError exception
        #
        mock_check_output.side_effect = subprocess.CalledProcessError(2, ["/bin/lsblk"])
        disk_list = check_smartctl.get_disk_list()

        self.assertEqual(disk_list, [])
