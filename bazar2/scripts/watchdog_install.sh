#!/bin/sh
cd /home/nao

mv bin/watchdog ./
chmod +x watchdog
mv watchdog /opt/naoqi/bin/
cd /etc/init.d/
echo -n "# " > watchdogd
echo -n ! >> watchdogd
echo /bin/sh >> watchdogd
echo "/opt/naoqi/bin/watchdog -a -rs 10080 &" >> watchdogd
echo "logread -f > ""/home/nao/logread_\$(date '+%Y-%m-%d_%Hh%Mm%S').log"" &" >> watchdogd

chmod 700 /etc/init.d/watchdogd
cd /etc/rc5.d
# ln -s ../init.d/watchdogd S98watchdogd # install the daemon
/etc/init.d/watchdogd