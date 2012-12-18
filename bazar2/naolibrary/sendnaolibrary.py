# -*- coding: utf-8 -*-

####
# Send all file and project to the nao
# Command line option:
# <scriptname> [nao_ip]
####


strNaoIp = "10.0.252.134";
strRemotePath = "/home/nao/naolibrary/";

import os
import sys

# nao ip
if( len( sys.argv ) > 1 ):
	strNaoIp = sys.argv[1];


def isOnWin32():
  "Are we on a ms windows system?"
  return os.name != 'posix';
# isOnWin32 - end

if( isOnWin32() ):
    pwd = "-pw nao";

# os.system( "ssh nao@%s mkdir -p %s" % ( strNaoIp, strRemotePath ) );
os.system( "scp %s -r * nao@%s:%s" % ( pwd, strNaoIp, strRemotePath ) );