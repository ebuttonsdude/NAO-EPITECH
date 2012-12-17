#!/bin/sh
##
## Author(s):
##  - Cedric GESTES <gestes@aldebaran-robotics.com>
##
## Copyright (C) 2010 Aldebaran Robotics
##

LOCK_FILE="/var/lock/naoqi-${NAME}.lock"

case "$1" in
  start)

    #still a pid file?
    if [ -f $LOCK_FILE ] ; then
      #still the running process?
      if kill -0 $(cat $LOCK_FILE) 2>/dev/null ; then
	echo "!! Warning ${NAME} is already running !!"
	echo "if you are sure it is not running"
	echo "remove $LOCK_FILE"
	exit 1
      fi
    fi

    echo "starting ${NAME}"
    if [ nao = `whoami` ]; then
      #user nao, already have a dbus session
      /opt/naoqi/bin/${NAME} --daemon --pid "${LOCK_FILE}" ${ARGS} >/dev/null
    else
      #we want a dbus session
      su -c ". /etc/profile.d/dbus-session.sh; /opt/naoqi/bin/${NAME} --daemon --pid ${LOCK_FILE} ${ARGS}" - nao >/dev/null
    fi
    ;;

  stop)
    if [ -f $LOCK_FILE ] ; then
        kill $(cat $LOCK_FILE)
        #waiting for naoqi to shutdown
        while kill -0 $(cat $LOCK_FILE) 2>/dev/null ; do
          echo "waiting for ${NAME} to shutdown"
	  sleep 1
        done
        echo "${NAME} stopped"
        rm $LOCK_FILE
    fi
    ;;

  log)
    logread -f | grep 'naoqi'
    ;;

  restart)
    $0 stop
    sleep 2
    $0 start
    ;;

  *)
    echo "Usage: /etc/init.d/${NAME} {start|stop|restart}"
    exit 1
    ;;

esac

exit 0

