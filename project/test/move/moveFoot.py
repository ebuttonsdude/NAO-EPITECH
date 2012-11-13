#-*- coding: iso-8859-15 -*-

import config
import motion
import time

def moveFoot(motionProxy, pChainName, pAngle = None, pSpeed = 0.5):
    '''
    Function to make NAO bump on his Torso or Head with his arm
    '''

    # Set the fraction of max speed for the arm movement.
    pMaxSpeedFraction = pSpeed
    # Define the final position.

    if (pChainName == "RAnklePitch"):
        pTargetAngles = pAngle;
    elif (pChainName == "LAnklePitch"):
        pTargetAngles = pAngle
    elif (pChainName == "RAnkleRoll"):
        pTargetAngles = pAngle
    elif (pChainName == "LAnkleRoll"):
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