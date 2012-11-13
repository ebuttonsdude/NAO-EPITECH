#-*- coding: iso-8859-15 -*-

import config
import motion
import time

def moveLegs(motionProxy, pChainName, pAngle = None, pSpeed = 0.5):
    '''
    Function to make NAO bump on his Torso or Head with his arm
    '''

    # Set the fraction of max speed for the arm movement.
    pMaxSpeedFraction = pSpeed
    # Define the final position.

    if (pChainName == "RHipYawPitch"):
        pChainName = "LHipYawPitch"
        pTargetAngles = pAngle;
    elif (pChainName == "HipYawPitch"):
        pChainName = "LHipYawPitch"
        pTargetAngles = pAngle;
    elif (pChainName == "LHipYawPitch"):
        pTargetAngles = pAngle
    elif (pChainName == "RHipPitch"):
        pTargetAngles = pAngle
    elif (pChainName == "LHipPitch"):
        pTargetAngles = pAngle
    elif (pChainName == "RKneePitch"):
        pTargetAngles = pAngle
    elif (pChainName == "LKneePitch"):
        pTargetAngles = pAngle
    elif (pChainName == "RHipRoll"):
        pTargetAngles = pAngle
    elif (pChainName == "LHipRoll"):
        pTargetAngles = pAngle
    else:
        print "ERROR: chainName is unknown"
        print "Must be HeadYaw or HeadPitch"
        print "---------------------"
        exit(1)

    # Convert to radians.
    pTargetAngles = pTargetAngles * motion.TO_RAD

    # Move the arm to the final position.
    motionProxy.angleInterpolationWithSpeed(pChainName, pTargetAngles, pMaxSpeedFraction)