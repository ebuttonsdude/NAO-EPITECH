#!/bin/sh
cd /etc/init.d/
echo -n "# " > watchdogd
echo -n ! >> watchdogd
echo /bin/sh >> watchdogd
echo "# /opt/naoqi/bin/watchdog -a -rs 10080 &" >> watchdogd
echo "logread -f > ""/home/nao/logread_\$(date '+%Y-%m-%d_%Hh%Mm%S').log"" &" >> watchdogd
killall watchdog