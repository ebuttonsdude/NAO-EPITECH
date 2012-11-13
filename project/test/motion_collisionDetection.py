#-*- coding: iso-8859-15 -*-

''' Collision detection : arm collision detection '''

import config
import motion
import time
import moveHead
import moveHand
import moveLegs
import moveFoot

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


def main(pChainName = "LArm"):
    ''' Example showing the effect of collision detection
        Nao bumps his chest with his left arm with collision detection enabled
        or disabled.
    '''

    ##################
    # Initialization #
    ##################

    motionProxy = config.loadProxy("ALMotion")
    # Set NAO in stiffness On.
    config.StiffnessOn(motionProxy)

    # Send robot to Pose Init.
    config.poseZero(motionProxy)

    # Get the robot configuration.
    robotConfig = motionProxy.getRobotConfig()
    robotName = ""
    for i in range(len(robotConfig[0])):
        if (robotConfig[0][i] == "Model Type"):
            robotName = robotConfig[1][i]

    ###############################
    # Arm motion bumping on torso #
    ###############################

    # Disable collision detection on chainName.
    pEnable = True
    success = motionProxy.setCollisionProtectionEnabled(pChainName, pEnable)
    if (not success):
        print("Failed to disable collision protection")
    time.sleep(1.0)
    config.poseZero(motionProxy)
    moveHead.moveHead(motionProxy, "HeadYaw", 45)
    moveHead.moveHead(motionProxy, "HeadPitch", 45)
    moveHand.moveHand(motionProxy, "RHand", 45)
    moveLegs.moveLegs(motionProxy, "RHipYawPitch", 45)
    moveLegs.moveLegs(motionProxy, "LHipYawPitch", 45)
    moveFoot.moveFoot(motionProxy, "RAnklePitch", 45)
    time.sleep(3.0)
    # Make NAO's arm move so that it bumps its torso.
    #moveArm(motionProxy, robotName, pChainName, [0, 40, 0, 0])
    #moveArm(motionProxy, robotName, "LArm", [0, 40, 0, 0])
    #time.sleep(2.0)
    i = 0

#    while i < 3:
#        moveArm(motionProxy, robotName, pChainName, [10, 0, -90, -50], 0.3)
#        moveArm(motionProxy, robotName, "LArm", [10, 10, -90, -50], 0.3)
#        time.sleep(1.0)
#        moveArm(motionProxy, robotName, pChainName, [10, -10, -40, -50], 0.3)
#        moveArm(motionProxy, robotName, "LArm", [10, -10, -40, -50], 0.3)
#        time.sleep(1.0)
#        i += 1
    # Go back to pose init.
    config.poseZero(motionProxy)

if __name__ == "__main__":
    # The arm you want to move
    pChainName = "RArm" # "LArm" or "RArm"
    main(pChainName)
