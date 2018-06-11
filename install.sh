#!/bin/sh -e

USER=$(whoami)
plist_path="$1"
plist_filename=$(basename "$plist_path")
echo $plist_filename
install_path="/Users/amoghp/Library/LaunchAgents/$plist_filename"

sudo rm -f /var/log/bluetooth_flipper.error
sudo touch /var/log/bluetooth_flipper.error
sudo chown $USER /var/log/bluetooth_flipper.error

sudo rm -f /var/log/bluetooth_flipper.output
sudo touch /var/log/bluetooth_flipper.output
sudo chown $USER /var/log/bluetooth_flipper.output

echo "installing launchctl plist: $plist_path --> $install_path"
sudo cp -f "$plist_path" "$install_path"
# sudo chown root "$install_path"
# sudo chmod 644 "$install_path"

echo "Unloading..."
launchctl unload "$install_path"

echo "Loading..."
launchctl load "$install_path"

echo "to check if it's running, run this command: sudo launchctl list | grep com.jtjr.bluetooth_flipper"
echo "to uninstall, run this command: sudo launchctl unload \"$install_path\""
