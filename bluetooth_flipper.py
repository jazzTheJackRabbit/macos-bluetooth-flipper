#!/usr/bin/env python
import sys
import os
import subprocess
import re
import time
from exceptions import OSError

class Flipper:
    def __init__(self):
        self.prev_lid_closed_state = self.is_lid_closed()

    def is_lid_closed(self):
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

    def is_bluetooth_on(self):
        try:
            bluetooth_status = "/usr/local/bin/blueutil -p".split(" ")
            bluetooth_status_op = subprocess.check_output(bluetooth_status)
            status = int(bluetooth_status_op.split("\n")[0])
            return bool(status)
        except Exception as exception:
            print exception.message
            print "Installing blueutil..."
            install_bluetooth = "/usr/local/bin/brew install blueutil".split(" ")
            install_op = subprocess.check_output(install_bluetooth)
            print install_op
            return self.is_bluetooth_on()


    def flip_bluetooth(self):
        bluetooth_on = "/usr/local/bin/blueutil -p 1".split(" ")
        bluetooth_off = "/usr/local/bin/blueutil -p 0".split(" ")
        lid_closed_state = self.is_lid_closed()

        if lid_closed_state != self.prev_lid_closed_state:
            self.prev_lid_closed_state = lid_closed_state
            if lid_closed_state:
                if not self.is_bluetooth_on():
                    subprocess.check_output(bluetooth_on)
            else:
                if self.is_bluetooth_on():
                    subprocess.check_output(bluetooth_off)

def main():
    flipper = Flipper()
    while True:
        flipper.flip_bluetooth()
        time.sleep(3)

main()