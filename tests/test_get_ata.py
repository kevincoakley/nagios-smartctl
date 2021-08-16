#!/usr/bin/env python

import subprocess
import unittest
from mock import patch

import check_smartctl


class TestGetATA(unittest.TestCase):
    def setUp(self):
        pass

    @patch("subprocess.check_output")
    def test_get_ata(self, mock_check_output):
        #
        # Test no exceptions with ATA output
        #
        mock_check_output.return_value = b"[1:0:1:0]    disk    ATA      HGST HUH728080AL V7J0  /dev/sde\n[1:0:2:0]    disk    ATA      HGST HUH728080AL V7J0  /dev/sdf"
        ata = check_smartctl.get_ata()

        self.assertEqual(ata, True)

        #
        # Test no exceptions without ATA output
        #
        mock_check_output.return_value = b"[1:0:0:0]    disk    HGST     HUS726060AL5210  A7J0  /dev/sde\n[1:0:1:0]    disk    HGST     HUS726060AL5210  A7J0  /dev/sdf"
        ata = check_smartctl.get_ata()

        self.assertEqual(ata, False)

    @patch("subprocess.check_output")
    def test_get_ata_exception(self, mock_check_output):
        #
        # Test CalledProcessError exception
        #
        mock_check_output.side_effect = subprocess.CalledProcessError(
            2, ["/usr/bin/lsscsi"]
        )
        ata = check_smartctl.get_ata()

        self.assertEqual(ata, None)
