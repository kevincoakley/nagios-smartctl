#!/usr/bin/env python

import json
import subprocess
import sys
import unittest
from mock import patch

import check_smartctl


class TestMain(unittest.TestCase):

    def setUp(self):
        with open("tests/examples/sda.out", "r") as file:
            self.sda = json.load(file)

    @patch('check_smartctl.get_smartctl_devstat')
    @patch('check_smartctl.get_disk_list')
    def test_main(self, mock_get_disk_list, mock_get_smartctl_devstat):
        #
        # Test with no issues
        #
        with patch.object(sys, 'argv', ["check_smartctl.py"]):
            #
            # Test OK
            #
            smartctl = {
                "ata_device_statistics": {
                    "pages": [
                        {
                            "name": "General Errors Statistics",
                            "table": [
                                {
                                    "name": "Number of Reported Uncorrectable Errors",
                                    "value": 1
                                }
                            ]
                        }
                    ]
                }
            }

            mock_get_disk_list.return_value = ["sda"]
            mock_get_smartctl_devstat.return_value = smartctl

            self.assertEqual(check_smartctl.main(), 0)

            #
            # Test WARNING
            #
            smartctl["ata_device_statistics"]["pages"][0]["table"][0]["value"] = 100

            self.assertEqual(check_smartctl.main(), 1)

    @patch('subprocess.check_output')
    def test_main_disk_list_exception(self, mock_check_output):
        #
        # Test failed lsblk command or no disks
        #
        with patch.object(sys, 'argv', ["check_smartctl.py"]):

            mock_check_output.side_effect = subprocess.CalledProcessError(2, ["/bin/lsblk"])

            self.assertEqual(check_smartctl.main(), 3)
