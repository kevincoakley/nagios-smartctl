#!/usr/bin/env python

import json
import subprocess
import unittest
from mock import patch

import check_smartctl


class TestGetSmartctlDevstat(unittest.TestCase):
    def setUp(self):
        with open("tests/examples/sda.out", "r") as file:
            self.sda = file.read().replace("\n", "")

    @patch("subprocess.check_output")
    def test_get_smartctl_devstat(self, mock_check_output):
        #
        # Test no exceptions
        #
        mock_check_output.return_value = self.sda
        devstat = check_smartctl.get_smartctl_devstat("sda")

        self.assertEqual(devstat, json.loads(self.sda))

    @patch("subprocess.check_output")
    def test_get_smartctl_devstat_exception(self, mock_check_output):
        #
        # Test CalledProcessError exception with returncode == 2
        #
        mock_check_output.side_effect = subprocess.CalledProcessError(
            2, ["/sbin/smartctl"]
        )
        devstat = check_smartctl.get_smartctl_devstat("sda")

        self.assertEqual(devstat, [])

        #
        # Test CalledProcessError exception with returncode != 2
        #
        mock_check_output.side_effect = subprocess.CalledProcessError(
            3, ["/sbin/smartctl"]
        )
        devstat = check_smartctl.get_smartctl_devstat("sda")

        self.assertEqual(devstat, [])
