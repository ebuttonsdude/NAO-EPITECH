#!/bin/sh
## Author(s):
##  - Cedric GESTES <gestes@aldebaran-robotics.com>
##
## Copyright (C) 2010 Aldebaran Robotics

#start a dbus-session for user. only one by user.

DBUS_LOCK_FILE=/var/lock/dbus.$USER.lock
DBUS_ADDR_FILE=/tmp/dbus.$USER.session

if [ -f $DBUS_LOCK_FILE ] ; then
  if ! [ kill -0 $(cat $DBUS_LOCK_FILE) 2>/dev/null ] ; then
    # No DBus session found
    rm -rf $DBUS_LOCK_FILE $DBUS_ADDR_FILE 2>/dev/null >/dev/null
  fi
fi
if ! [ -e $DBUS_ADDR_FILE ] ; then
  dbus-daemon --session --print-address=1 --print-pid=2 --fork >$DBUS_ADDR_FILE 2>$DBUS_LOCK_FILE
fi
export DBUS_SESSION_BUS_ADDRESS=$(cat $DBUS_ADDR_FILE)
