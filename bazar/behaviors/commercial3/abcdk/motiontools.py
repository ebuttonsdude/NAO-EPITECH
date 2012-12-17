# -*- coding: utf-8 -*-

###########################################################
# Aldebaran Behavior Complementary Development Kit
# Motion tools
# Aldebaran Robotics (c) 2010 All Rights Reserved - This file is confidential.
###########################################################

"Motion tools"

# this module should be called motion, but risk of masking with the official motion.py from Naoqi, since 1.816

print( "importing abcdk.motiontools" );

import naoqitools
import debug


def getMotionBodyJointName():
    "return a list of all joint name used by Motion"
    motion = naoqitools.myGetProxy( "ALMotion" );
    return motion.getJointNames('Body');
# getMotionBodyJointName - end

def getDcmBodyJointName():
    "return a list of all joint name used by the DCM"
    listJoint = getMotionBodyJointName();
    listJoint.remove( "RHipYawPitch" ); # when using dcm: remove this joint
    return listJoint;
# getMotionBodyJointName - end


# global variable = beurk, should be in a class !

global_getNbrMoveOrder_listKeyOrder = [];
global_getNbrMoveOrder_listKeyValue = [];
global_getNbrMoveOrder_listKeyStiffness = [];
global_getNbrMoveOrder_listOrder_prev = [];

def getNbrMoveOrder( nThreshold = 0.06 ):
    "compute current joint moving by order"
    mem = naoqitools.myGetProxy( "ALMemory" );
    global global_getNbrMoveOrder_listKeyOrder;
    global global_getNbrMoveOrder_listKeyValue;
    global global_getNbrMoveOrder_listKeyStiffness;
    global global_getNbrMoveOrder_listOrder_prev;

    # first time: generate key list
    if( len( global_getNbrMoveOrder_listKeyOrder ) < 1 ):
        listJointName = getDcmBodyJointName();
        for strJointName in listJointName:
            global_getNbrMoveOrder_listKeyOrder.append( "Device/SubDeviceList/%s/Position/Actuator/Value" % strJointName );
            global_getNbrMoveOrder_listKeyValue.append( "Device/SubDeviceList/%s/Position/Sensor/Value" % strJointName );
            global_getNbrMoveOrder_listKeyStiffness.append( "Device/SubDeviceList/%s/Hardness/Actuator/Value" % strJointName );
            global_getNbrMoveOrder_listOrder_prev = mem.getListData( global_getNbrMoveOrder_listKeyOrder ); # init first time

    # get all values
    arOrder = mem.getListData( global_getNbrMoveOrder_listKeyOrder );
    arValue = mem.getListData( global_getNbrMoveOrder_listKeyValue );
    arStiffness= mem.getListData( global_getNbrMoveOrder_listKeyStiffness );

    nNbr = 0;
    for i in range( len( arOrder ) ):
        # a joint is moving if: pos is different from order, if order changed and if stiffness
        # we can have a big difference between order and value when no stiffness (position is out of range)
        if( ( abs( arOrder[i] - arValue[i] ) > nThreshold or abs( global_getNbrMoveOrder_listOrder_prev[i] - arOrder[i] ) > 0.01 ) and arStiffness[i] > 0.01 ):
            nNbr += 1;
#            debug.debug( "getNbrMoveOrder: difference on %s: order: %f; sensor: %f; stiffness: %f" % ( global_getNbrMoveOrder_listKeyValue[i], arOrder[i], arValue[i], arStiffness[i] ) );
    global_getNbrMoveOrder_listOrder_prev = arOrder;
    return nNbr;
# getNbrMoveOrder - end

# record the activity of a joint and knows if it's moving or not and the side of the move
# classe qui enregistre l'activité d'une articulation et permet de savoir si elle est en train de bouger et dans quelle sens
# elle ne va sortir un info de bougé uniquement quand c'est l'utilisateur qui la bouge, et pas si c'est Nao qui decide de bouger
# compter a peu pres 1-2% de cpu pour un update toutes les 0.3sec (a verifier, c'est pas plus, mais peut etre moins...)
class JointMove:

  def __init__( self, strJointName ):
    self.strJointName = strJointName;
    self.stm = naoqitools.myGetProxy( "ALMemory" );
    self.strStmJointNameSensor = "Device/SubDeviceList/" + strJointName + "/Position/Sensor/Value";
    self.strStmJointNameActuator = "Device/SubDeviceList/" + strJointName + "/Position/Actuator/Value";
    self.strStmJointNameStiffness    = "Device/SubDeviceList/" + strJointName + "/Hardness/Actuator/Value";
    self.rDiffThreshold = 0.05;
    self.reset();
  # __init__ - end

  def getJointName( self ):
    return self.strJointName;
  # getJointName - end

  # assume that joint has no stiffness or that joint is not too much stiff
  def ensureJointIsSoft( self ):
    rNewValueHardness = self.stm.getData( self.strStmJointNameStiffness, 0 );
    rMin = 0.30; # below this value, arms couldn't move to the head level.
    if( rNewValueHardness > rMin ):
      dcm = naoqitools.myGetProxy( "DCM" );
      dcm.set( ["%s/Hardness/Actuator/Value" % self.strJointName, "Merge",  [[rMin, dcm.getTime( 20 ) ]] ] );
  # ensureJointIsSoft - end
  
  def setDiffThreshold( rNewVal ):
        "Change the diff threshold"
        self.rDiffThreshold = rNewVal;

  # start the event catching
  def start( self ):
    self.ensureJointIsSoft();
  # start - end

  # return 0 si l'articulation n'as presque pas bougé, 1 si elle a bougé dans le sens positif, et -1 si dans le sens negatif
  # don't call it too often, because snsor take some time to reach actuator value
  def update( self ):
    rNewValueSensor = self.stm.getData( self.strStmJointNameSensor, 0 ); # todo: en une passe avec un getDataList ?
    rNewValueActuator = self.stm.getData( self.strStmJointNameActuator, 0 );
    rNewValueHardness = self.stm.getData( self.strStmJointNameStiffness, 0 );
    # check if there was a new user command
    if( abs( rNewValueActuator - self.rLastActuatorValue ) < 0.005 or rNewValueHardness < 0.001 ):  # actuator is by nature very precise - actuator is copied from position when stifnness is 0
#      debug( "JointMove debug('" + self.strJointName + "'): rActu-old: %8.5f; new: %8.5f; rSensor-old: %8.5f; new: %8.5f" % ( self.rLastActuatorValue, rNewValueActuator, self.rLastSensorValue, rNewValueSensor ) );
      rDiff = rNewValueSensor - self.rLastSensorValue;
      self.rLastSensorValue = rNewValueSensor;
      if( abs( rDiff ) > self.rDiffThreshold ):
#        debug( "JointMove debug('" + self.strJointName + "'): rSensor-old: %8.5f; rDiff: %5.3f >>>" % ( self.rLastSensorValue, rDiff ) );
        if( rDiff > 0 ): return 1;
        return -1;
    else:
      # the joint has received a move order: update value
#      debug( "JointMove debug('" + self.strJointName + "'): rActu-old: %8.5f; new: %8.5f stiff: %5.3f" % ( self.rLastActuatorValue, rNewValueActuator, rNewValueHardness ) );
      # to skip the (rebond) rebound, we add small latency after having move, we put the actuator small by small to the new value
#      self.rLastActuatorValue = rNewValueActuator;
      self.rLastActuatorValue = ( self.rLastActuatorValue + rNewValueActuator ) / 2;
      # update sensor, so it won't trigger next frame
      self.rLastSensorValue = rNewValueSensor;
    return 0;
  # update - end

  # remet les valeurs a zero pour un nouveau catch d'evenement
  def reset( self ):
    self.ensureJointIsSoft();
    self.rLastSensorValue = self.stm.getData( self.strStmJointNameSensor, 0 );
    self.rLastActuatorValue = self.stm.getData( self.strStmJointNameActuator, 0 );
  # reset - end

# class JointMove - end