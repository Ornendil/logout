#!/bin/bash

# List all open windows, and for each window, run thisfullscreen script
#wmctrl -l | ./thisfullscreen.sh
#wmctrl -l|awk '{$3=""; $2=""; $1=""; print $0}' | ./thisfullscreen.sh
wmctrl -l|awk '{print $1}' | /opt/logout/thisfullscreen.sh
#wmctrl -r '$title' -b toggle,fullscreen
#xprop -name '$title'
#
