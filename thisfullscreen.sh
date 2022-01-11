#!/bin/bash
while read line
do
	#state=$(xprop -name "${line:23}" _NET_WM_STATE)
	state=$(xprop -id "${line}" _NET_WM_STATE)
	if [[ $state == *"_NET_WM_STATE_FULLSCREEN"* ]]; then
		echo "true"
		break
	fi
done
