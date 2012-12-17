#!/bin/sh

LOAD_MODULE=modprobe
[ -e /sbin/modprobe ] || LOAD_MODULE=insmod

if [ -e /sbin/depmod -a ! -f /lib/modules/`uname -r`/modules.dep ]; then
	[ "$VERBOSE" != no ] && echo "Calculating module dependencies ..."
	depmod -Ae
fi

if [ -f /proc/modules ]; then
       if [ -f /etc/modules ]; then
               [ "$VERBOSE" != no ] && echo -n "Loading modules: "
               while read module args
               do
                       case "$module" in
                               \#*|"") continue ;;
                       esac
                       [ "$VERBOSE" != no ] && echo -n "$module "
                       eval "$LOAD_MODULE $module $args >/dev/null 2>&1"
               done < /etc/modules
               [ "$VERBOSE" != no ] && echo
       fi
fi

if [ ! -d /media/internal/system/ ]; then
  mkdir -p /media/internal/system/
fi
if [ ! -f /media/internal/system/boot.log ]; then
  touch /media/internal/system/boot.log
  echo 0 >/media/internal/system/boot.log
fi
if [ -f /media/internal/system/wififailed ]; then
  rm /media/internal/system/wififailed
fi

echo "$(( `cat /media/internal/system/boot.log` + 1 ))" >/media/internal/system/boot.log
sync
if [ `cat /media/internal/system/boot.log`  -le 2 ]; then
  modprobe zd1211rw
else
  touch /media/internal/system/wififailed
fi
modprobe cdc-acm
: exit 0
