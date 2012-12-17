# -*- coding: utf-8 -*-

###########################################################
# Aldebaran Behavior Complementary Development Kit
# Path tools
# Aldebaran Robotics (c) 2010 All Rights Reserved - This file is confidential.
###########################################################

"""Path tools"""
print( "importing abcdk.pathtools" );


import os

#import filetools # for getFileContents, but cycling => duplicate this call
def getFileContents( szFilename, bQuiet = False ):
    "read a file and return it's contents, or '' if not found, empty, ..."
    aBuf = "";
    try:
        file = open( szFilename );
    except BaseException, err:
        if( not bQuiet ):
            debug.debug( "ERR: filetools(!).getFileContents open failure: %s" % err );
        return "";
        
    try:
        aBuf = file.read();
    except BaseException, err:
        if( not bQuiet ):
            debug.debug( "ERR: filetools(!).getFileContents read failure: %s" % err );
        file.close();
        return "";
        
    try:
        file.close();
    except BaseException, err:
        if( not bQuiet ):
            debug.debug( "ERR: filetools(!).getFileContents close failure: %s" % err );
        pass
    return aBuf;
# getFileContents - end

# import system # for isOnNao, but cycling => duplicate this call
def isOnNao():
    """Are we on THE real Nao ?"""
    szCpuInfo = "/proc/cpuinfo";
#  if not isFileExists( szCpuInfo ): # already done by the getFileContents
#    return False;
    szAllFile =  getFileContents( szCpuInfo, bQuiet = True );
    if( szAllFile.find( "Geode" ) == -1 ):
        return False;
    return True;
# isOnNao - end



def getDirectorySeparator():
  "return '/' or '\' relatively to the os"
  if os.name == 'posix':
    return "/";
  return "\\";
# getDirectorySeparator - end

def getNaoqiPath():
    "get the naoqi path"
    s = os.environ.get( 'AL_DIR' );
    if( s == None ):
        if( isOnNao() ):
            s = '/opt/naoqi/';
        else:
            s = '';
    return s;
# getNaoqiPath - end

def getUsersPath():
    "return a specific path"
    return getBehaviorRoot() + "Users" + getDirectorySeparator();
# getUsersPath - end

def getCachePath():
    "return a specific path"
    return getUsersPath() + "All" + getDirectorySeparator() + "Caches" + getDirectorySeparator();
# getCachePath - end


def getVolatilePath():
  "get the volatile path (or temp path if on a real limited computer)"
  if( isOnNao() ):
    return "/var/volatile/";
  if( os.name == 'posix' ):
    return getDirectorySeparator() + "tmp" + getDirectorySeparator(); # /tmp
  return "c:\\temp\\"; # TODO: ? trouver le dossier temp grace a la variable d'environnement
# getVolatilePath - end

def getBehaviorRoot():
    "return the roots of all our tree"
    if( isOnNao() ):
        return getDirectorySeparator() + "home" + getDirectorySeparator() + "nao" + getDirectorySeparator();
    if( os.name == 'posix' ):
        return "~" + getDirectorySeparator() + "nao" + getDirectorySeparator(); # TODO: ?
    else:
        return "C:" + getDirectorySeparator() + "temp" + getDirectorySeparator();

def getApplicationsPath():
    "return a specific path"
    return getBehaviorRoot() + "Applications" + getDirectorySeparator();

def getApplicationSharedPath():
    "return a specific path"
    return getApplicationsPath() + "shared" + getDirectorySeparator();

def getABCDK_Path():
    "get the path containing the abcdk file"
    return os.path.abspath( os.path.dirname( __file__ ) ) + getDirectorySeparator();
#getABCDK_Path - end

# print( "getABCDK_Path: '%s'" % getABCDK_Path() );

print( "importing abcdk.pathtools - end" );