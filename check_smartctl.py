#!/usr/bin/env python

import argparse
import json
import subprocess
import sys

lsblk = "/bin/lsblk"
smartctl = "/sbin/smartctl"


def get_disk_list():
    """
    Get the list of disk device names using lsbkl
    :return: disk device names as a list
    """
    try:
        return subprocess.check_output([lsblk, "-n", "-d", "--output", "NAME"]).splitlines()
    except subprocess.CalledProcessError as ex:
        print(ex)
        return []


def get_smartctl_devstat(disk):
    """
    Get the output of smartctl devstat for disk
    :param disk: str device name
    :return: output of smartctl devstat as JSON object
    """
    try:
        return json.loads(subprocess.check_output([smartctl, "-l", "devstat", "/dev/" + disk, "-j"]))
    except subprocess.CalledProcessError as ex:
        # returncode == 2 for megaraid drives
        if ex.returncode != 2:
            print(ex)
        return []


def get_reported_uncorrectable_errors(diskstat):
    """
    Get the "Number of Reported Uncorrectable Errors" from the smartctl devstat JSON object
    :param diskstat: smartctl devstat JSON object
    :return: int of the "Number of Reported Uncorrectable Errors"
    """
    if "ata_device_statistics" in diskstat:
        for page in diskstat["ata_device_statistics"]["pages"]:
            if page["name"] == "General Errors Statistics":
                for table in page["table"]:
                    if table["name"] == "Number of Reported Uncorrectable Errors":
                        return table["value"]
    return None


def parse_arguments(args):
    """
    Parse Commandline Arguments
    :param args: *args positional arguments
    :return: Commandline arguments parsed by argparse
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--warning-errors',
                        metavar="warning_errors",
                        dest="warning_errors",
                        help="Number of Uncorrectable Errors before a WARNING Nagios Alert.",
                        type=int,
                        default=20)

    return parser.parse_args(args)


def main():
    """
    script main
    :return: exit code
    """
    exit_code = 0
    exit_message = "OK - No Errors"
    error_message = ""

    args = parse_arguments(sys.argv[1:])

    disks = get_disk_list()

    if not disks:
        print("UNKNOWN - No Disks Found")
        return 3

    for disk in disks:
        diskstat = get_smartctl_devstat(disk)
        disk_errors = get_reported_uncorrectable_errors(diskstat)

        if disk_errors >= args.warning_errors:
            error_message = error_message + "/dev/%s errors: %s; " % (disk, disk_errors)
            exit_code = 1

    if exit_code == 1:
        exit_message = "WARNING - %s" % error_message

    print(exit_message)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
