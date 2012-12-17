#!/bin/sh

case "$1" in
  start)
    if [ -f /media/internal/system/boot.log ]; then
      echo 0 >/media/internal/system/boot.log
    fi
    ;;
  stop)
    if [ -f /media/internal/system/wififailed ]; then
      rm /media/internal/system/wififailed
    fi
    ;;
esac

