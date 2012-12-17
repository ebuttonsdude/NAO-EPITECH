# -*- coding: utf-8 -*-

###########################################################
# Aldebaran Behavior Complementary Development Kit
# Profiler tools
# Aldebaran Robotics (c) 2010 All Rights Reserved - This file is confidential.
###########################################################

"""Profiler tools"""
print( "importing abcdk.profiler" );

import time

import debug
import naoqitools

def getBoxConstantName( strPathBoxName ):
    "extract from a long choregraphe name, a short name"
    "eg: ALFrameManager__0xad95c6c0__root__TestBattery_4  => TestBattery_4"
    strPick = "__root";
    nPos = strPathBoxName.find( strPick );
    return "Box_" + strPathBoxName[nPos+len(strPick)-4:];
# getBoxConstantName - end

#~ print( getBoxConstantName( "ALFrameManager__0xad95c6c0__root" ) );
#~ print( getBoxConstantName( "ALFrameManager__0xad95c6c0__root__TestBattery_4" ) );

def startBox( strBoxName ):
    up = naoqitools.myGetProxy( "UsageProfiler" );
    up.startMeasure ( getBoxConstantName( strBoxName ), "", "", 0 );
# startBox - end
    
def stopBox( strBoxName ):
    up = naoqitools.myGetProxy( "UsageProfiler" );
    up.stopMeasure( getBoxConstantName( strBoxName ), "", "", 0 );
# startBox - end

class UsageProfilerHelper:
    "A small helper to use UsageProfiler"
    "just create it in some methods"
    def __init__( self, pstrModuleName, pstrFunctionName = "",  pstrTaskName = "" ):
        self.up = naoqitools.myGetProxy( "UsageProfiler" );
        self.strModuleName = pstrModuleName;
        self.strFunctionName = pstrFunctionName;
        self.strTaskName = pstrTaskName;
        self.up.startMeasure( pstrModuleName, pstrFunctionName, pstrTaskName, -1 );
    # __init__ - end
    
    def __del__( self ):
        self.up.stopMeasure( self.strModuleName, self.strFunctionName, self.strTaskName );
    # __del__ - end
    
    #~ def idle( self ):
        #~ "fait croire au systme que l'objet est utilisé est donc qu'il ne faut pas le garbager tout de suite"
        #~ if( self.up == 421 ): # impossible...
            #~ self.strModuleName = "pipi";
    #~ # idle - end        
    
# class UsageProfilerHelper - end

def UsageProfilerHelperBox( strBoxName ):
    "use UsageProfilerHelper in a choregraphe box"
    return UsageProfilerHelper( getBoxConstantName( strBoxName ) );
# startBox - end

class TimeMethod:
    "mesure the time taken by a method - another implementation of a profiler, in pure python"
    "Use: define an object TimeMethod in your method, and that's all!"
    def __init__(self, strOptionnalLibelle = "" ):
        "Create the object"
        self.reset( strOptionnalLibelle );
    # __init__ - end
    
    def reset( self, strOptionnalLibelle = "" ):
        "reset the object"
        self.strCaller = debug.getFileAndLinePosition( 2 ); # callstack: reset, __init__, caller
        if( strOptionnalLibelle != "" ):
            strOptionnalLibelle = "( " + strOptionnalLibelle + " )";
        self.strOptionnalLibelle = strOptionnalLibelle;
        self.timeBegin = time.time();            
        self.intermediate = []; # optionnal pair of [time, message]
        self.bStopped = False;
    # reset - end
    
    def setIntermediate( self, strOptionnalMessageNamingFollowingPart = "" ):
        "store intermediate time and continue, the optionnal name is the name of the following part"
        if( strOptionnalMessageNamingFollowingPart != "" ):
            strOptionnalMessageNamingFollowingPart = "( " + strOptionnalMessageNamingFollowingPart + " )";
        totalTime = time.time() - self.timeBegin;
        self.intermediate.append( [ totalTime, strOptionnalMessageNamingFollowingPart ] );
        timePrev = 0;
        if( len( self.intermediate ) > 1 ):
            timePrev = self.intermediate[-2][0];
        print( "timer: %40s: intermediate time: %6.3f %s %s\n" % ( self.strCaller, totalTime-timePrev, self.strOptionnalLibelle, strOptionnalMessageNamingFollowingPart ) );
    # setIntermediate - end
    
    def getCurrentTotalTime( self ):
        return time.time() - self.timeBegin;
    # getCurrentTotalTime - end
        
    def stopAndPrint( self ):
        "stop the timer, print info, and return a string containing a printable string"
        strOut = "";
        if( self.bStopped ):
            return strOut;
        self.bStopped = True;
        totalTime = time.time() - self.timeBegin;
        if( len( self.intermediate ) < 1 ):
            strOut += "timer: %40s: executing time: %6.3f %s" % ( self.strCaller, totalTime, self.strOptionnalLibelle );
        else:
            strOut += "timer: %40s: total time: %6.3f %s\n" % ( self.strCaller, totalTime, self.strOptionnalLibelle );
            nPrev = 0.;
            for someTime in self.intermediate:
                strOut += " %57s + %6.3f %s\n" % ( "", someTime[0] - nPrev, someTime[1] );
                nPrev = someTime[0];
            strOut += " %57s + %6.3f %s" % ( "", totalTime - nPrev, "( til the end )" );
        print( strOut );
        return strOut;
    # stopAndPrint - end
    
    def __del__( self ):
        self.stopAndPrint();
    # __del__ - end
    
# class TimeMethod - end

#~ timer = TimeMethod( "coucou" );
#~ time.sleep( 1 );
#~ timer.setIntermediate( "compute" );
#~ time.sleep( 4 );
#~ timer.setIntermediate( "draw" );
#~ time.sleep( 3 );
#~ timer.stopAndPrint();
