# -*- coding: utf-8 -*-

###########################################################
# Aldebaran Behavior Complementary Development Kit
# Speech tools
# Aldebaran Robotics (c) 2010 All Rights Reserved - This file is confidential.
###########################################################

"Audio tools"
print( "importing abcdk.sound" );

import math
import struct
import sys
import time

# sys.path.append( "../" ); # pour pouvoir adder les modules suivant, si on est dans un subfolder "audio"

import config
import debug
import filetools
import pathtools
import naoqitools
import system
import test

def analyseSound_pause( bWaitForResume ):
    "pause some running sound analyse"
    "bWaitForResume: True => pause until resume call, False => pause a little times (5sec?)"
    try:
        analyser = naoqitools.myGetProxy( "UsageNoiseExtractor" );
        nTime = 5;
        if( bWaitForResume ):
            nTime = -1;
        analyser.inhibitSoundAnalyse( nTime );
    except BaseException, err:
        debug.debug( "analyseSound_pause: ERR: " + str( err ) );
# analyseSound_pause - end

def analyseSound_resume( bWaitForResume ):
    "resume a previously infinite paused sound analyse"
    if( bWaitForResume ):
        try:
            analyser = naoqitools.myGetProxy( "UsageNoiseExtractor" );
            analyser.inhibitSoundAnalyse( 0 );
        except BaseException, err:
            debug.debug( "analyseSound_resume: ERR: " + str( err ) );
# analyseSound_resume - end

def playSound( strFilename, bWait = True, bDirectPlay = False, nSoundVolume = 100 ):
    "Play a sound, return True if ok"
    "bDirectPlay: play it Now! (could fragilise system and video drivers"
    "nSoundVolume: if bDirectPlay is on, will play the sound with a specific volume (ndev)"
    
    print( "playSound( '%s', bWait = %s, bDirectPlay = %s, nSoundVolume = %d )" % ( strFilename, str( bWait ), str( bDirectPlay ), nSoundVolume ) );
    
    if( config.bRemoveDirectPlay ):
        print( "WRN: DISABLING_DIRECTPLAY SETTINGS for testing/temporary purpose" );
        bDirectPlay = False;
    
    try:
        # If strFilename has an absolute path, go ahead with this path !
        if strFilename.startswith( pathtools.getDirectorySeparator() ):
            strSoundFile = strFilename
        else:
            strSoundFile = pathtools.getApplicationSharedPath() + "wav/0_work_free/" + strFilename;
            if( not filetools.isFileExists( strSoundFile ) ):
                # then try another path
                strSoundFile = pathtools.getApplicationSharedPath() + "wav/1_validated/" + strFilename;
            if( not filetools.isFileExists( strSoundFile ) ):
                # and another path
                strSoundFile = pathtools.getApplicationSharedPath() + "wav/0_work_copyright/" + strFilename;
            if( not filetools.isFileExists( strSoundFile ) ):
                # and another path
                strSoundFile = pathtools.getApplicationSharedPath() + "wav/" + strFilename;
            if( not filetools.isFileExists( strSoundFile ) ):
                # and another path
                strSoundFile = pathtools.getNaoqiPath() + "/share/naoqi/wav/" + strFilename;
            if( not filetools.isFileExists( strSoundFile ) ):
                print( "ERR: appu.playSound: can't find file '%s'" % strFilename );
                return False;

        analyseSound_pause( bWait );
        if( bDirectPlay ):
            system.mySystemCall( "aplay -q " + strSoundFile, bWait );
        else:
            global_proxyAudioPlayer = naoqitools.myGetProxy( "ALAudioPlayer" );            
            if( global_proxyAudioPlayer == None ):
                print( "ERR: sound.playSound: can't find module 'ALAudioPlayer'" );
            else:
                if( bWait ):
                    global_proxyAudioPlayer.playFile( strSoundFile );
                else:
                    global_proxyAudioPlayer.post.playFile( strSoundFile );
        analyseSound_resume( bWait );
    except BaseException, err:
        debug.debug( "playSound: ERR: " + str( err ) );
        print( "errr: " + str( err ) );
    return True;
# playSound - end

def playMusic( strFilename, bWait ):
  print( "appuPlaySound: avant cnx sur audioplayer (ca lagge?)" );
  #myAP = naoqitools.myGetProxy( "ALAudioPlayer" );
  print( "appuPlaySound: apres cnx sur audioplayer (ca lagge?)" );
  ap = naoqitools.myGetProxy( "ALAudioPlayer" );
  if( bWait ):
    ap.playFile( getApplicationSharedPath() + "/mp3/" + strFilename );
  else:
    ap.post.playFile( getApplicationSharedPath() + "/mp3/" + strFilename );

  #if( not bNaoqiSound ):
  #  strSoundFile = getApplicationSharedPath() + "/mp3/" + strFilename;
  #else:
  #  strSoundFile = getNaoqiPath() + "/data/mp3/" + strFilename;
  #system.mySystemCall( getSystemMusicPlayerName() + " " +  strSoundFile, bWait );

# playMusic - end

def playSoundHearing():
  "play the standard appu sound before earing user command"
#  time.sleep( 0.4 ); # time to empty all sound buffers
  playSound( "jingle_earing.wav", bDirectPlay = True );
  time.sleep( 0.05 ); # time to empty all sound buffers ?
# playSoundHearing - end

def playSoundSpeaking():
  "play the standard appu sound before speaking to user"
  playSound( "jingle_speaking.wav", bDirectPlay = True );
# playSoundSpeaking - end

def playSoundUnderstanding():
  "play the standard appu sound to show a command is understood"
  playSound( "jingle_understanded.wav", bDirectPlay = True );
# playSoundUnderstanding - end

# sound volume (premisse of the robot's class)

def getCurrentMasterVolume():
    "get nao master sound system volume (in %)"
    "return 0 on error or problem (not on nao or ...)"
    try:
        ad = naoqitools.myGetProxy( 'ALAudioDevice' );
        nVal = ad.getOutputVolume();
        debug.debug( "getCurrentMasterVolume: %d" % ( nVal ) );
        return nVal;
    except BaseException, err:
        print( "getCurrentMasterVolume: error '%s'" % str( err ) );
        
    print( "WRN: => using old one using fork and shell!" );
  
    strOutput = system.executeAndGrabOutput( "amixer sget Master | grep 'Front Right: Playback' | cut -d[ -f2 | cut -d% -f1", True );
    if( strOutput == '' ):
        return 0;
    nValR = int( strOutput );
    strOutput = system.executeAndGrabOutput( "amixer sget Master | grep 'Front Left: Playback' | cut -d[ -f2 | cut -d% -f1", True );
    nValL = int( strOutput );
    nVal = ( nValR + nValL ) / 2;
    debug.debug( "getCurrentMasterVolume: %d (%d,%d)" % ( nVal, nValL, nValR ) );
    return nVal;
# getCurrentMasterVolume - end

def setMasterVolume( nVolPercent ):
    "change the master volume (in %)"
    if( nVolPercent < 0 ):
        nVolPercent = 0;
    if( nVolPercent > 100 ):
        nVolPercent = 100;
    debug.debug( "setMasterVolume to %d%%" % nVolPercent );
    
    try:
        ad = naoqitools.myGetProxy( 'ALAudioDevice' );
        ad.setOutputVolume( nVolPercent );
        return;
    except BaseException, err:
        print( "getCurrentMasterVolume: error '%s'" % str( err ) );
        
    print( "WRN: => using old one using fork and shell!" );
        
    strCommand = "amixer -q sset Master " + str( nVolPercent * 32 / 100 );
    strCommand += "; amixer  -q sset \"Master Mono\" 32";
    strCommand += "; amixer  -q sset PCM 25";    
    system.mySystemCall( strCommand );
# setMasterVolume - end


def volumeFadeOut():
    "Fade out master sound system"
    nVol = getCurrentMasterVolume();
    print( "volumeFadeOut: %d -----> 0" % nVol );
    nCpt = 0;
    while( nVol > 0 and nCpt < 30 ): # when concurrent calls are made with other fade type, it could go to a dead lock. because getCurrentMasterVolume take some time, we prefere to add some counter
        ++nCpt;
        # ramping
        if( nVol > 55 ):
            nVol -= 3;
        else:
            nVol -= 9;
        setMasterVolume(nVol);
#        print( "volout: %d" % nVol );

def volumeFadeIn( nFinalVolume ):
    "Fade in master sound system"
    nVol = getCurrentMasterVolume();
    print( "volumeFadeIn: %d -----> %d" % ( nVol, nFinalVolume ) );
    nCpt = 0;
    while( nVol < nFinalVolume and nCpt < 30 ): # when concurrent calls are made with other fade type, it could go to a dead lock. because getCurrentMasterVolume take some time, we prefere to add some counter
        ++nCpt;
        if( nVol > 55 ):
            nVol += 3;
        else:
            nVol += 9;
        setMasterVolume(nVol);
#        print( "volin: %d" % nVol );

def setMasterMute( bMute ):
  "mute nao sound volume"
  if( bMute ):
    strVal = "off";
  else:
    strVal = "on";
  debug.debug( "setMasterMute: %s" % strVal );
  system.mySystemCall( "amixer -q sset Master " + strVal );
# setMasterMute - end

def isMasterMute():
  "is nao sound volume muted?"
  strOutput = system.executeAndGrabOutput( "amixer sget Master | grep 'Front Right: Playback' | cut -d[ -f4 | cut -d] -f1", True );
  strOutput = strOutput.strip();
  bMute = ( strOutput == "off" );
  debug.debug( "isMasterMute: %d (strOutput='%s')" % ( bMute, strOutput ) );
  return bMute;
# isMasterMute - end

def setMasterPanning( nPanning = 0 ):
    "change the sound master panning: 0: center -100: left +100: right"
    "current bug: currently volume is louder when at border, than at center, sorry"
    try:
        debug.debug( "setMasterPanning to %d" % nPanning );
        nVol = getCurrentMasterVolume();
        nCoefR = nVol + nVol*nPanning/100;
        nCoefL = nVol - nVol*nPanning/100;
        nCoefR = nCoefR * 32 / 100;
        nCoefL = nCoefL * 32 / 100;
        system.mySystemCall( "amixer -q sset Master %d,%d" % ( nCoefL, nCoefR ) );
        system.mySystemCall( "amixer -q sset PCM 25" );
        system.mySystemCall( "amixer -q sset \"Master Mono\" 32" );
    except BaseException, err:
        print( "setMasterPanning: error '%s'" % str( err ) );
# setMasterPanning - end

 # pause music
def pauseMusic():
  "pause the music player"
  debug.debug( "pauseMusic" );
  system.mySystemCall( "killall -STOP mpg321b" );

# restart music
def unPauseMusic():
  debug.debug( "unPauseMusic" );
  system.mySystemCall( "killall -CONT mpg321b" );

def ensureVolumeRange( nMinValue = 58, nMaxValue = 84 ):
    "analyse current volume settings, and change it to be in a specific range"
    "default range is the 'confort' range"
    nCurrentVolume = getCurrentMasterVolume();
    if( nCurrentVolume >= nMinValue and nCurrentVolume <= nMaxValue ):
        return;
    # set the volume sound nearest the min or max range
    nNewVolume = 0;
    if( nCurrentVolume < nMinValue ):
        nNewVolume = nMinValue;
    else:
        nNewVolume = nMaxValue;
    setMasterVolume( nNewVolume );
# ensureVolumeAbove - end

def removeBlankFromFile( strFilename, b16Bits = True, bStereo = False ):
  "remove blank at begin and end of a raw sound file, a blank is a 0 byte."
  "bStereo: if set, it remove only by packet of 4 bytes (usefull for raw in stereo 16 bits recording)"
  try:
    file = open( strFilename, "rb" );
  except BaseException, err:
    print( "WRN: removeBlankFromFile: ??? (err:%s)" % ( str( err ) ) );

    return False;
    
  try:
    aBuf = file.read();
  finally:
    file.close();
    
  try:  
    nNumTrimAtBegin = 0;
    nNumTrimAtEnd = 0;
    nFileSize = len( aBuf );
    for i in range( nFileSize ):
  #    print( "aBuf[%d]: %d" % (i, ord( aBuf[i] )  ) );
      if( ord( aBuf[i] ) != 0 ):
  #      print( "i1:%d" % i );
        if( bStereo and b16Bits ):
          i = (i/4)*4; # don't cut between channels
        elif( bStereo or b16Bits ):
          i = (i/2)*2;
        break;
    nNumTrimAtBegin = i;

    for i in range( nFileSize - 1, 0, -1 ):
  #    print( "aBuf[%d]: %d" % (i, ord( aBuf[i] )  ) );
      if( ord( aBuf[i] ) != 0 ):
  #      print( "i2:%d" % i );
        if( bStereo ):
          i = ((i/4)*4)+4;
        elif( bStereo or b16Bits ):
          i = ((i/2)*2)+2;
        break;
    nNumTrimAtEnd = i;

  #  debug( "sound::removeBlankFromFile: nNumTrimAtBegin: %d, nNumTrimAtEnd: %d, nFileSize: %d" % (nNumTrimAtBegin, nNumTrimAtEnd, nFileSize ) );
    if( nNumTrimAtBegin > 0 or nNumTrimAtEnd < nFileSize - 1 ):
        print( "sound::removeBlankFromFile: trim at begin: %d; pos trim at end: %d (data trimmed:%d)" % ( nNumTrimAtBegin, nNumTrimAtEnd, nNumTrimAtBegin + ( nFileSize - nNumTrimAtEnd ) ) );
        aBuf = aBuf[nNumTrimAtBegin:nNumTrimAtEnd];
        try:
            file = open( strFilename, "wb" );
        except BaseException, err:
            print( "WRN: sound::removeBlankFromFile: dest file open error (2) (err:%s)" % ( str( err ) ) );
            return False;
        try:
            file.write( aBuf );
        finally:            
            file.close();
  except BaseException, err:
    print( "sound::removeBlankFromFile: ERR: something wrong occurs (file not found or ...) err: " + str( err ) );
    return False;
  return True;
# removeBlankFromFile - end

def loadSound16( strFileIn, nNbrChannel = 1 ):
    "load a sound file and return an array of samples (16 bits) (in mono)"
    "return [] on error"
    aSamplesMono = [];    
    try:
        file = open( strFileIn, "rb" );
    except BaseException, err:
        print( "sound::loadSound16: ERR: something wrong occurs: %s" % str( err ) );
        return [];
    try:
        aBuf = file.read();  
        file.close();
        nOffset = 0;
        lenFile = len( aBuf );
        strHeaderTag = struct.unpack_from( "4s", aBuf, 0 )[0];
        if( strHeaderTag == "RIFF" ):
            print( "sound::loadSound16: skipping wav header found in %s" % strFileIn );
            nOffset += 44; # c'est en fait un wav, on saute l'entete (bourrin)
        
        print( "sound::loadSound16: reading file '%s' of size %d interpreted as %d channel(s)" % ( strFileIn, lenFile, nNbrChannel ) );
        while( nOffset < lenFile ):
            nValSample = struct.unpack_from( "h", aBuf, nOffset )[0];
            aSamplesMono.append( nValSample ); # ici c'est lourd car on alloue un par un (pas de reserve) (des essais en initialisant le tableau  avec des [0]*n, font gagner un petit peu (5.0 sec au lieu de 5.4)
            nOffset += 2;
            if( nNbrChannel > 1 ):
                nOffset += 2; # skip right channel
        # while - end
    except BaseException, err:
        print( "sound::loadSound16: ERR: something wrong occurs: %s" % str( err ) );
        pass
        
    print( "=> %d samples" %  len( aSamplesMono ) );    
    return aSamplesMono;
# loadSound16 - end

def computeEnergyBest( aSample ):
	"Compute sound energy on a mono channel sample, aSample contents signed int from -32000 to 32000 (in fact any signed value)"

	# Energy(x_centered) = Energy(x) - Nsamples * (Mean(x))^2
	# Energy = Energy(x_centered)/ ( 65535.0f * sqrtf((float)nNbrSamples ) # en fait c'est mieux sans le sqrtf

	nEnergy = 0;
#	nMean = 0;
	nNumSample = len( aSample );

	for i in xrange( 1, nNumSample ):
#		nMean += aSample[i];
		nDiff = aSample[i] - aSample[i-1];
		nEnergy += nDiff*nDiff;

#	rMean = nMean / float( nNumSample );

#	print( "computeEnergyBest: nNumSample: %s, sum: %s, mean: %s, energy: %s" % ( str( nNumSample ),  str( nMean ), str( rMean ), str( nEnergy )) );
#	print( "computeEnergyBest: nNumSample: %d, sum: %d, mean: %f, energy: %d" % ( nNumSample,  nMean, rMean, nEnergy ) );
#	nEnergy -= int( rMean * rMean * nNumSample ); # on n'enleve pas la moyenne: ca n'a aucun interet (vu que c'est deja des diff)
	nEnergyFinal = int( float( nEnergy ) / nNumSample );
#	nEnergyFinal /= 32768;
	nEnergyFinal = int( math.sqrt( nEnergyFinal ) );
#	print( "computeEnergyBest: nEnergy: %f - nEnergyFinal: %s " % ( nEnergy,  str( nEnergyFinal ) ) );
	return nEnergyFinal;
# computeEnergyBest - end

def convertEnergyToEyeColor_Intensity( nValue, nMax ):
    "convert energy[0,nMax] in eye color intensity"
    return ( nValue / float( nMax ) ) * 1.0 + 0.00; # add 0.2 pour la possibilité de ne pas etre tout noir
# convertEnergyToEyeColor_Intensity - end

def analyseSpeakSound( strRawFile, nSampleLenMs = 50, bStereo = False ):
    "Analyse a raw stereo or mono sound file, and found the light curve relative to sound (for further speaking)"
    print( "analyseSpeakSound: analysing '%s' (time:%d)" % ( strRawFile, int( time.time() ) ) );
    nNbrChannel = 1;
    if( bStereo ):
        nNbrChannel = 2;
    aMonoSound = loadSound16( strRawFile, nNbrChannel );
    if( len( aMonoSound ) < 1 ):
        return [];

    #analyse every 50ms sound portion (because 50ms is the average latency of leds)
    anLedsColorSequency = []; # for every time step, an int corresponding to the RGB colors
    nSizeAnalyse = int( (22050*nSampleLenMs)/1000 ); # *50 => un sample chaque 50ms
    nMax = 0;
    nOffset = 0;
    nNbrSample = len( aMonoSound );
    print( "analyseSpeakSound: analysing %d sample(s)" % nNbrSample );
    while( nOffset < nNbrSample ):
        anBuf = aMonoSound[nOffset:nOffset+nSizeAnalyse];
        nOffset += nSizeAnalyse;
        nValue = computeEnergyBest( anBuf );
        if( nValue > nMax ):
            nMax = nValue;
        # storenValue to nColor
        anLedsColorSequency.append( nValue );
    # while - end

    # convert nValue to nColor (using max energy)
    nOffset = 0;
    nNbrComputed = len( anLedsColorSequency );
    print( "analyseSpeakSound: converting %d energy to leds light (max=%d)" % ( nNbrComputed, nMax) );
    while( nOffset < nNbrComputed ):
        anLedsColorSequency[nOffset] = convertEnergyToEyeColor_Intensity( anLedsColorSequency[nOffset], nMax );
        nOffset += 1;
    # while - end

    print( "analyseSpeakSound: analysing '%s' (time:%d) - end" % ( strRawFile, int( time.time() ) ) );
    return anLedsColorSequency;
# analyseSpeakSound - end

def getMasterVolume():
    "get nao master sound system volume (in %)"
    try:
        ad = naoqitools.myGetProxy( 'ALAudioDevice' );
        nVal = ad.getOutputVolume();
        debug.debug( "getMasterVolume: %d%%" % ( nVal ) );
        return nVal;
    except BaseException, err:
        print( "getMasterVolume: error '%s'" % str( err ) );
        
    print( "WRN: => using old one using fork and shell!" );
  
    strOutput = system.executeAndGrabOutput( "amixer sget Master | grep 'Front Right: Playback' | cut -d[ -f2 | cut -d% -f1", True );
    nValR = int( strOutput );
    strOutput = system.executeAndGrabOutput( "amixer sget Master | grep 'Front Left: Playback' | cut -d[ -f2 | cut -d% -f1", True );
    nValL = int( strOutput );
    nVal = ( nValR + nValL ) / 2;
    debug.debug( "getMasterVolume: %d%% (%d,%d)" % ( nVal, nValL, nValR ) );
    return nVal;
# getMasterVolume - end

def setMasterVolume( nVolPercent ):
    "change the master volume (in %)"
    if( nVolPercent < 0 ):
        nVolPercent = 0;
    if( nVolPercent > 100 ):
        nVolPercent = 100;
    debug.debug( "setMasterVolume to %d%%" % nVolPercent );
    
    try:
        ad = naoqitools.myGetProxy( 'ALAudioDevice' );
        ad.setOutputVolume( nVolPercent );
        return;
    except BaseException, err:
        print( "getCurrentMasterVolume: error '%s'" % str( err ) );
        
    print( "WRN: => using old one using fork and shell!" );
        
    strCommand = "amixer -q sset Master " + str( nVolPercent * 32 / 100 );
    strCommand += "; amixer  -q sset \"Master Mono\" 32";
    strCommand += "; amixer  -q sset PCM 25";    
    system.mySystemCall( strCommand );
# setMasterVolume - end


def changeMasterVolume( nRelativeChange ):
    "change current volume, by adding a value (-100,+100)"
    setMasterVolume( getMasterVolume() + nRelativeChange );
# changeMasterVolume - end


def autoTest():
    if( test.isAutoTest() or False ):
        test.activateAutoTestOption();        
        if( not system.isOnNao() ):
            analyseSpeakSound( "d:/pythonscript/TestSoundEnergy_16bit_mono.raw" );
        playSoundHearing();
        playSound( "warning.wav", bDirectPlay = True );
        playSound( "hello.wav" );
        playSound( "ho1.wav" );
# autoTest - end
    
autoTest();