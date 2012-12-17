# -*- coding: utf-8 -*-

###########################################################
# Aldebaran Behavior Complementary Development Kit
# Diagnostic tools
# Aldebaran Robotics (c) 2010 All Rights Reserved - This file is confidential.
###########################################################

"Diagnostic tools (this is not specifically diagnostic, but I don't the real name)"
print( "importing abcdk.diagnostic" );

import motiontools
import naoqitools

global_getBodyHigherTemperature_listKeyTemp = [];
def getBodyHigherTemperature():
    mem = naoqitools.myGetProxy( "ALMemory" );

    global global_getBodyHigherTemperature_listKeyTemp;

    # first time: generate key list
    if( len( global_getBodyHigherTemperature_listKeyTemp ) < 1 ):
        listJointName = motiontools.getDcmBodyJointName();
        for strJointName in listJointName:
            global_getBodyHigherTemperature_listKeyTemp.append( "Device/SubDeviceList/%s/Temperature/Sensor/Value" % strJointName );

    # get all temp value
    arVal = mem.getListData( global_getBodyHigherTemperature_listKeyTemp );

    rMax = 0;
    nHigherJoint = -1;
    for rVal in arVal:
        if( rVal > rMax ):
            rMax = rVal;
#    debug( "getBodyHigherTemperature: higher: joint '%s': %5.2f" % ( strHigherJoint, rMax ) );
    return rMax;
# getBodyListTemperature - end
