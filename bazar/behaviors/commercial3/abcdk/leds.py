# -*- coding: utf-8 -*-

###########################################################
# Aldebaran Behavior Complementary Development Kit
# Leds tools
# Aldebaran Robotics (c) 2010 All Rights Reserved - This file is confidential.
###########################################################

# this module should be called file, but risk of masking with the class file.

"""Leds"""
print( "importing abcdk.leds" );

import time

import naoqitools
import test

def getSide( nIndex ):
  """ get side left/right from 0..1 """
  aSide = [ "Left", "Right" ];
  if( nIndex < 0 or nIndex > 1 ):
    print( "ERR: leds.getSide: index %d out of range" % nIndex );
    nIndex = 0;
  return aSide[nIndex];
# getSide - end

def getEarLedName( nIndex, nSideIndex = 0 ):
    "get dcm leds ears device name from index"
    nNbrMax = 10;
    if( nIndex >= nNbrMax or nIndex < 0 ):
        print( "ERR: leds.getEarLedName: index out of range (%d)" % nIndex );
        return "";
    nAngle = (360/nNbrMax) * nIndex;
    strName = "Ears/Led/%s/%dDeg/Actuator/Value" % ( getSide( nSideIndex ), nAngle );
    return strName;
# getEarLedName - end


def circleLedsEyes( nColor, rTime, nNbrTurn ):
  # launch a leds animation using one color
  leds = naoqitools.myGetProxy( "ALLeds" );
  nNbrSegment = 8;
  for i in range( nNbrSegment*nNbrTurn ):
    leds.post.fadeRGB( "FaceLed%d" % (i%nNbrSegment) , nColor, rTime );
    leds.post.fadeRGB( "FaceLed%d" % (i%nNbrSegment) , 0x000000, rTime*1.25 );
    time.sleep( rTime*0.25 );
  time.sleep( rTime*0.5 ); # wait last time
# circleLedsEyes - end

def circleLedsEars( rTime, nNbrTurn ):
  # launch a leds animation using one color
  leds = naoqitools.myGetProxy( "ALLeds" );
  nNbrSegment = 10;
  for i in range( nNbrSegment*nNbrTurn ):
    leds.post.fade( "LeftEarLed%d" % (i%nNbrSegment+1) , 1., rTime );
    leds.post.fade( "RightEarLed%d" % (i%nNbrSegment+1) , 1., rTime );
    leds.post.fade( "LeftEarLed%d" % (i%nNbrSegment+1) , 0., rTime*1.25 );
    leds.post.fade( "RightEarLed%d" % (i%nNbrSegment+1) , 0., rTime*1.25 );
    time.sleep( rTime*0.25 );
  time.sleep( rTime*0.5 ); # wait last time
# circleLedsEars - end

def getBrainLedName( nNumLed ):
    "get the name of the dcm led device by it's number"
    "0 => front left; 1 => next in clock wise"
    
       #~ names = [
            #~ 'Head/Led/Front/Right/1/Actuator/Value',
            #~ 'Head/Led/Front/Right/0/Actuator/Value',
            #~ 'Head/Led/Middle/Right/0/Actuator/Value',
            #~ 'Head/Led/Rear/Right/0/Actuator/Value',
            #~ 'Head/Led/Rear/Right/1/Actuator/Value',
            #~ 'Head/Led/Rear/Right/2/Actuator/Value',
            #~ 'Head/Led/Rear/Left/2/Actuator/Value',
            #~ 'Head/Led/Rear/Left/1/Actuator/Value',
            #~ 'Head/Led/Rear/Left/0/Actuator/Value',
            #~ 'Head/Led/Middle/Left/0/Actuator/Value',
            #~ 'Head/Led/Front/Left/0/Actuator/Value',
            #~ 'Head/Led/Front/Left/1/Actuator/Value']
            
    if( nNumLed <= 1 ):
        return "Head/Led/Front/Right/%d/Actuator/Value" % (1-nNumLed);
    if( nNumLed >= 10 ):
        return "Head/Led/Front/Left/%d/Actuator/Value" % (nNumLed-10);

    if( nNumLed <= 2 ):
        return "Head/Led/Middle/Right/%d/Actuator/Value" % (2-nNumLed);
    if( nNumLed >= 9 ):
        return "Head/Led/Middle/Left/%d/Actuator/Value" % (nNumLed-9);

    if( nNumLed <= 5 ):
        return "Head/Led/Rear/Right/%d/Actuator/Value" % (nNumLed-3);
    if( nNumLed >= 6 ):
        return "Head/Led/Rear/Left/%d/Actuator/Value" % (8-nNumLed);

    print( "ERR: getBrainLedName: index out of range (%d)" % nNumLed );
    return "";
# getBrainLedName - end

def setBrainLedsIntensity( rIntensity = 1.0, rTimeMs = 20, bDontWait = False ):
    "light on/off all the brain leds"
    dcm = naoqitools.myGetProxy( "DCM" );
    riseTime = dcm.getTime(rTimeMs);
    for i in range( 12 ):
        strDeviceName = getBrainLedName( i );
        dcm.set( [ strDeviceName, "Merge",  [[ rIntensity, riseTime ]] ] );    
    if( not bDontWait ):
        time.sleep( rTimeMs / 1000. );
# setBrainLedsIntensity - end

def setOneBrainIntensity( nLedIndex, rIntensity = 1.0, bDontWait = False ):
    "set one led beyond all the brain leds"
    "nLedIndex in [0,11]"
    dcm = naoqitools.myGetProxy( "DCM" );
    rTime = 0.05
    riseTime = dcm.getTime(int( rTime*1000 ));
    strDeviceName = getBrainLedName( nLedIndex );
    dcm.set( [ strDeviceName, "Merge",  [[ float( rIntensity ), riseTime ]] ] );         # le float ici est ultra important car sinon venant de chorégraphe 1.0 => 1 (depuis les sliders de params)
    if( not bDontWait ):
        time.sleep( rTime );
# setOneBrainIntensity - end

def setBrainVuMeter( nLeftLevel, nRightLevel, rIntensity = 1.0, bDontWait = False, bInverseSide = False ):
    "use the brain leds as vu meter (left and right separated)"
    "the 0 is in the front of Nao"
    "nXxxLevel in [0,6] => 0: full lightoff; 6 => full litten"
    "bInverseSide: the 0 becomes at bottom of Nao"
    dcm = naoqitools.myGetProxy( "DCM" );
    rTime = 0.05
    riseTime = dcm.getTime(int( rTime*1000 ));
    for i in range( 6 ):
        if( not bInverseSide ):
            strDeviceNameR = getBrainLedName( i );
            strDeviceNameL = getBrainLedName( 11-i );
        else:
            strDeviceNameR = getBrainLedName( 5-i );
            strDeviceNameL = getBrainLedName( 11-(5-i) );            
        if( i < nLeftLevel ):
            rIntL = rIntensity;
        else:
            rIntL = 0.;
        if( i < nRightLevel ):
            rIntR = rIntensity;
        else:
            rIntR = 0.;        
        dcm.set( [ strDeviceNameL, "Merge",  [[ float( rIntL ), riseTime ]] ] );         # le float ici est ultra important car sinon venant de chorégraphe 1.0 => 1 (depuis les sliders de params)
        dcm.set( [ strDeviceNameR, "Merge",  [[ float( rIntR ), riseTime ]] ] );
    if( not bDontWait ):
        time.sleep( rTime );
# setOneBrainIntensity - end

def setColorToEyes( anList8Color, rTime = 1.,  nEyesMask = 0x3 ):
    "set a list of 8 color to eyes"
    "rTime: time in sec of the fade"
    "nEyesMask: 1: left, 2: right, 3: both"
#    print( "anList8Color: %s" % str( anList8Color ) );
    leds = naoqitools.myGetProxy( 'ALLeds' );
    for nNumSide in range( 2 ):
        nSideValMask = 1 << nNumSide;
        if( True ): # nEyesMask & nSideValMask ): TODO: bien gerer le mask
            for nNumLed in range( len( anList8Color ) ):
                strName = "FaceLed%s%d" % ( getSide(nNumSide), nNumLed );
                nColor = anList8Color[nNumLed];
                # no need of a mirror: already handled in ALLeds !
                # nIndexMirror = 7 - nNumLed;
#                print( "strName: %s, color: %x, time: %f" % ( strName, nColor, rTime ) );
                leds.post.fadeRGB( strName, nColor, rTime );
        # if - end
    # for - end
# setColorToEyes - end

def getEyeLedName( nNumLed, nSide, nColor = 3 ):
    "get the name of the dcm led device by it's number"
    "nNumLed: 0 => Top internal led, 1 => internal high led, 2 => internal low led, 3 => bottom internal led ..."
    "nSide: 0 => left; 1 => right"
    "nColor: 0 => Blue, 1 => Green, 2 => Red, 3 => all"
    "return name or an array of 3 name (when nColor is set 3)"
    
    # device are on the form of  "Face/Led/Red/Right/315Deg/Actuator/Value"
    strTemplate = "Face/Led/%s/%s/%dDeg/Actuator/Value";

    if( nNumLed > 7 or nNumLed < 0 ):
        print( "ERR: abcdk.led.getEyeLedName: index out of range (%d)" % nNumLed );
        return;
    if( nSide > 1 or nSide < 0 ):
        print( "ERR: abcdk.led.getEyeLedName: side out of range (%d)" % nSide );
        return;
    if( nColor > 3 or nColor < 0 ):
        print( "ERR: abcdk.led.getEyeLedName: color out of range (%d)" % nColor );
        return;

    astrColor = [ "Blue", "Green", "Red"];
    astrSide = [ "Left", "Right"];
    anAngle = [0, 45, 90, 135, 180, 225, 270, 315];
    if( nSide == 1 ):
        nNumLed = 7 - nNumLed;
    if( nColor < 3 ):
        return strTemplate % ( astrColor[nColor], astrSide[nSide], anAngle[nNumLed] );
    
    return  [
                    strTemplate % ( astrColor[0], astrSide[nSide], anAngle[nNumLed] ),
                    strTemplate % ( astrColor[1], astrSide[nSide], anAngle[nNumLed] ),
                    strTemplate % ( astrColor[2], astrSide[nSide], anAngle[nNumLed] )
                ];
    
    return "";
# getEyeLedName - end

def getEyeColor( nNumLed, nSide, nColor = 3 ):
    "return the color of one RGB leds, only one channel or the 3"
    "nNumLed: 0 => Top internal led, 1 => internal high led, 2 => internal low led, 3 => bottom internal led ..."
    "nSide: 0 => left; 1 => right"
    "nColor: 0 => Blue, 1 => Green, 2 => Red, 3 => all"
    "return a value 0..0xff or a value [r,g,b] if nColor == 3"
    leds = naoqitools.myGetProxy( "ALLeds" );
    name = getEyeLedName( nNumLed, nSide, nColor );
    if( len( name ) == 3 ):
        anRet = [];
        for i in range( 3 ):
            anRet.append( int(leds.getIntensity( name[i] ) * 255 ));
        return anRet;
    return int( leds.getIntensity( name ) * 255 );
# getEyeColor - end
    



def autoTest():
    test.activateAutoTestOption();
    print getEarLedName( 2 );
    print getEarLedName( 0, 1 );
    print getEyeLedName( 0, 0, 1 );
    print getEyeLedName( 0, 1, 3 );
    print getEyeColor( 0, 0, 3 );
    print getEyeColor( 0, 1, 3 );    
    print getEyeColor( 0, 0, 0 );
    print getEyeColor( 0, 1, 0 );
# autoTest - end

#autoTest();