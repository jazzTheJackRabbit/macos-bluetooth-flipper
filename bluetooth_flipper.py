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
        self.prev_external_connection_state = self.is_connected_to_external_displays()

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

    def is_connected_to_external_displays(self):
        displays = self.get_displays()
        if len(displays) == 1 and displays[0] == "Color LCD":
            return False
        return True

    def get_displays(self):
        result = subprocess.check_output(['system_profiler', 'SPDisplaysDataType'])
        o_lines = result.split("\n")
        lines = [line.strip() for line in result.split("\n")]
        display_lines = o_lines[lines.index("Displays:"):]
        displays = [line.split("        ") for line in display_lines]
        displays=displays[1:]
        displays = [display[1] for display in displays if len(display) > 1]
        displays = [display.strip().split(':')[0] for display in displays if not display[1].startswith(' ')]
        return displays

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
        is_connected_to_external_disp = self.is_connected_to_external_displays()

        if is_connected_to_external_disp != self.prev_external_connection_state:
            print("switching external display state")
            self.prev_external_connection_state = is_connected_to_external_disp
            if is_connected_to_external_disp:
                if not self.is_bluetooth_on():
                    subprocess.check_output(bluetooth_on)
            else:
                if self.is_bluetooth_on():
                    subprocess.check_output(bluetooth_off)

        # if lid_closed_state != self.prev_lid_closed_state:            
        #     self.prev_lid_closed_state = lid_closed_state
        #     if lid_closed_state:
        #         # LID CLOSED
        #         if self.is_connected_to_external_displays():
        #             if not self.is_bluetooth_on():
        #                 subprocess.check_output(bluetooth_on)
        #         else:
        #             if self.is_bluetooth_on():
        #                 subprocess.check_output(bluetooth_off)
        #     else:
        #         # LID OPEN
        #         if self.is_connected_to_external_displays():
        #             if not self.is_bluetooth_on():
        #                 subprocess.check_output(bluetooth_on)
        #         else:
        #             if self.is_bluetooth_on():
        #                 subprocess.check_output(bluetooth_off)

def main():
    flipper = Flipper()
    while True:
        flipper.flip_bluetooth()
        time.sleep(3)

main()