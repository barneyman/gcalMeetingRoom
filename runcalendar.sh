#!/bin/sh

cd /
cd /home/pi/py
#rm logs/calendar.log

filename="logs/calendar.log"
current_time=$(date "+%Y.%m.%d-%H.%M.%S")
logfile=$filename.$current_time

echo "Sleeping for 15 secs ..." > $logfile
sleep 15
python -u local.py -s >> $logfile 2>&1
cd /

