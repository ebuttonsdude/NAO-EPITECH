#!/bin/sh
##
## nao-profile.sh
## Login : <ctaf@localhost.localdomain>
## Started on  Fri Jul 17 16:14:07 2009 Cedric GESTES
## $Id$
##
## Author(s):
##  - Cedric GESTES <gestes@aldebaran-robotics.com>
##
## Copyright (C) 2009 Aldebaran Robotics

export PS1='\u@\h '"[\${?}]"' [\w]\$ '
export PATH=$PATH:/usr/local/sbin:/usr/sbin:/sbin
umask 022

LS_OPTIONS='--color=auto'
alias ls='ls $LS_OPTIONS'
alias l='ls $LS_OPTIONS'
alias ll='ls $LS_OPTIONS -l'
alias la='ls $LS_OPTIONS -lA'


alias nao='/etc/init.d/naoqi'
alias core='/etc/init.d/core'
alias user='/etc/init.d/user'
alias video='/etc/init.d/video'
alias audio='/etc/init.d/audio'
