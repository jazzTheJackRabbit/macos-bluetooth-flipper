#!/usr/bin/env python
import sys
import os
import subprocess
import re
import time
from exceptions import OSError


def is_lid_closed():
    ioreg = "ioreg -r -k AppleClamshellState -d 4".split(" ")
    grep = "grep AppleClamshellState".split(" ")

    ioreg_op = subprocess.Popen(ioreg, stdout=subprocess.PIPE)
    grep_op = subprocess.check_output(grep, stdin=ioreg_op.stdout)

    match = re.search(r'\"(.*)\" = (.*)', grep_op)
    attribute, state = match.group(1), match.group(2)
    
    if state == "No":
        return False
    else:
        return True


def is_bluetooth_on():
    try:
        bluetooth_status = "/usr/local/bin/blueutil -p".split(" ")
        bluetooth_status_op = subprocess.check_output(bluetooth_status)
        status = int(bluetooth_status_op.split("\n")[0])
        return bool(status)
    except Exception as exception:
        print "Installing blueutil..."
        install_bluetooth = "/usr/local/bin/brew install blueutil".split(" ")
        install_op = subprocess.check_output(install_bluetooth)
        print install_op
        return is_bluetooth_on()


def flip_bluetooth():
    bluetooth_on = "/usr/local/bin/blueutil -p 1".split(" ")
    bluetooth_off = "/usr/local/bin/blueutil -p 0".split(" ")
    
    if is_lid_closed():
        if not is_bluetooth_on():
            subprocess.check_output(bluetooth_on)
    else:
        if is_bluetooth_on():
            subprocess.check_output(bluetooth_off)


print "Running bluetooth flipper..."


while True:
    flip_bluetooth()
    time.sleep(3)