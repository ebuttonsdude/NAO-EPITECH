#-*- coding: iso-8859-15 -*-

import config
import motion
import time

def moveArm(motionProxy, pRobotName, pChainName, pAngle = None, pSpeed = 0.5):
    ''' Function to make NAO bump on his Torso or Head with his arm '''

    # Set the fraction of max speed for the arm movement.
    pMaxSpeedFraction = pSpeed

    # Define the final position.
    if (len(pAngle) == 4):
        ShoulderPitchAngle, ShoulderRollAngle, ElbowYawAngle, ElbowRollAngle = pAngle
    else:
        ShoulderPitchAngle, ShoulderRollAngle, ElbowYawAngle, ElbowRollAngle = 0

    if (pChainName == "LArm"):
        pTargetAngles = [ShoulderPitchAngle, +ShoulderRollAngle, +ElbowYawAngle, +ElbowRollAngle]
    elif (pChainName == "RArm"):
        pTargetAngles = [ShoulderPitchAngle, -ShoulderRollAngle, -ElbowYawAngle, -ElbowRollAngle]
    else:
        print "ERROR: chainName is unknown"
        print "Must be LArm or RArm"
        print "---------------------"
        exit(1)

    # Set the target angles according to the robot version.
    if (pRobotName == "naoH25") or\
       (pRobotName == "naoAcademics") or\
       (pRobotName == "naoT14"):
        pTargetAngles += [0.0, 0.0]
    elif (pRobotName == "naoH21"):
        pass
    elif (pRobotName == "naoT2"):
        pTargetAngles = []
    else:
        print "ERROR: Your robot is unknown"
        print "This test is not available for your Robot"
        print "---------------------"
        exit(1)

    # Convert to radians.
    pTargetAngles = [ x * motion.TO_RAD for x in pTargetAngles]
    pTargetHead = 45 * motion.TO_RAD
    # Move the arm to the final position.
    motionProxy.post.angleInterpolationWithSpeed(pChainName, pTargetAngles, pMaxSpeedFraction)
