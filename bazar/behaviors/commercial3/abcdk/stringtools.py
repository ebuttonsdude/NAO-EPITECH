# -*- coding: utf-8 -*-

###########################################################
# Aldebaran Behavior Complementary Development Kit
# String tools
# Aldebaran Robotics (c) 2010 All Rights Reserved - This file is confidential.
###########################################################


"""Tools to work with string."""

print( "importing abcdk.stringtools" );


def findNumber( strText, nMinValue = -99999999, bFindLast = False ): # todo: int_min
    "find a number (int or float) indication in a text line"
    "return the number or None"
    nLen = len( strText );
    nBegin = -1;
    nValueToRet = None;
    bStop = False;
    for i in range( nLen ):
#        debugLog( "findNumber: i: " + strText[i] );
        if( strText[i].isdigit() or strText[i] == '.' ):
            if( nBegin == -1 ):
                nBegin = i;
            if( i+1 == nLen ):
                # la chaine se termine par un chiffre, il faut l'analyser maintenant
                bStop = True;
                i += 1; # car on veut utiliser ce dernier charactere aussi
        else:
            if( nBegin != -1 ):
                bStop = True;
        if( bStop ):
            # print( "trying: '%s'" % strText[nBegin:i] );
            try:
                n = int( strText[nBegin:i] );
            except:                
                try:
                    n = float( strText[nBegin:i] );
                except:
                    nBegin = i;
                    continue; # burk number
            # print( "findNumber(temp): in '%s': %s" %( strText, str( n ) ) );
            if( n > nMinValue ):
                if( not bFindLast ):
                    return n;
                nValueToRet = n; # memorise for later use
            # if( n > nMinValue ) - end
            bStop = False;
            nBegin = -1;
    return nValueToRet; 
# findNumber - end

def findAfter( strText, strTextToFind ):
    "find the text after some text"
    "return '' if not found"
    nFind = strText.find( strTextToFind );
    if( nFind == -1 ):
        return "";
    return strText[nFind+len( strTextToFind ):];
# findAfter - end

def findBetween( strText, strTextBefore = None, strTextAfter = None ):
    "find the text between to text"
    "if 'before text' is not found, return from the beginning"
    "if 'after text' is not found, return til the end"
    "TODO: use substr ! "
    if( strTextBefore == None ):
        nBegin = 0;        
    else:
        nBegin = strText.find( strTextBefore );    
        if( nBegin == -1 ):
            nBegin = 0;
        else:
            nBegin += len( strTextBefore );

    if( strTextAfter == None ):
        nEnd = len( strText );
    else:
        nEnd = strText.find( strTextAfter,  nBegin );
        if( nEnd == -1 ):
            nEnd = len( strText );
    return strText[nBegin:nEnd];
# findAfter - end
    
def transformAsciiAccentToUtf8( s ):
    "change ascii (french?) accents to utf-8"
    strOutput = "";
    nLen = len( s );
    # We remark that only taken the ascii char bigger than E0 and outputting  0xC3 0xA0+(offset compared to E0) is working
    for i in range( 0, nLen ):
        print( "transformAsciiAccentToUtf8: %d %c 0x%x" % ( i, s[i], ord( s[i] ) ) );
        if( ord( s[i] ) >= 0xE0 ): # This works fine, for accent, but not for every strange character, eg: the movie "IRREVERSIBLE", with the last E, mirrored (some: "0xD0 0xAF 0xC6 0x8E")
            strOutput = strOutput + chr(0xC3) + chr( 0xA0+ord( s[i] )-0xE0 );
        else:
            if( ord( s[i] ) > 127 and ord( s[i] ) != 0xC3 and ord( s[i-1] ) != 0xC3 ): # looks like rotten characters, skipping it (but the eacute)
                pass;
            else:
                strOutput = strOutput + s[i];
    return strOutput;
# transformAsciiAccentToUtf8 - end

def isVersionFresher( strPrev, strNext ):
    "return True if strNext contains a fresher version number than strPrev (not equal)"
    "version are something like 1.0, 0.9, 1.8.16, 1.100.1888, ..."
    "1.0 is equal to 1."
    aPrev = strPrev.split( '.' );
    aNext = strNext.split( '.' );
    
    # change 1. by 1.0    
    if( aPrev[-1] == '' ):
        aPrev[-1] = '0';
    # change 1. by 1.0    
    if( aNext[-1] == '' ):
        aNext[-1] = '0';
    
    #~ print( "aPrev: %s" % str( aPrev ) );
    #~ print( "aNext: %s" % str( aNext ) );
    for idx in range( len( aNext ) ):
        if( len( aPrev ) <= idx ):
            return True;
        if( aPrev[idx] != aNext[idx] ):
            return int(aNext[idx]) > int( aPrev[idx] );
    return False; # equal => False
    
# isVersionFresher - end

def dictionnaryToString( aDico ):
  "return a beautiful and sorted string describing a dictionnaries for debugging or printing..."
  s = "# dictionnary has %d element(s):\n" % ( len( aDico ) );
  for k, v in sorted( aDico.iteritems() ):
    s += "  '%s': %s,\n" % ( str(k), str(v) );
  return s;
# dictionnaryToString - end

def autoTest():
    strNumber = "<br><strong>My IP Country Latitude</strong>: (46) <br><b>My IP Address City</b>:&nbsp;&nbsp; <font color='#980000'>Pa";
    nVal = findNumber( strNumber );
    print( "nVal: %s" % str( nVal ) );
    strNumber = "blablabla 3.59";
    nVal = findNumber( strNumber );
    print( "nVal: %s" % str( nVal ) );
    assert( nVal == 3.59 );
    
    strText = "Hello Alexandre";
    strOut = findAfter( strText, "Hello " );
    print( "findAfter: '%s'" % strOut );
    assert( strOut == "Alexandre" );
    strOut = findAfter( strText, "introuvable" );
    assert( strOut == "" );    
    
    strText = "Hello Alexandre, comment ca va?";
    strOut = findBetween( strText, "Hello ",  ", comment ca va?" );
    print( "findBetween: '%s'" % strOut );
    assert( strOut == "Alexandre" );
    strOut = findBetween( strText, "introuvable1",  "introuvable2" );
    print( "findBetween: '%s'" % strOut );
    strOut = findBetween( strText );
    print( "findBetween: '%s'" % strOut );    
    assert( strOut == strText );
    
    assert( isVersionFresher( "1.0", "1.1" ) );
    assert( not isVersionFresher( "1.0", "1.0" ) );
    assert( not isVersionFresher( "1.", "1.0" ) );
    assert( not isVersionFresher( "1.1", "1.0" ) );
    assert( isVersionFresher( "1.1", "1.1.5.6.7" ) );
    assert( isVersionFresher( "1.1", "2" ) );
    assert( not isVersionFresher( "1.1", "0" ) );
    assert( not isVersionFresher( "1.1", "" ) );
    
# autoTest - end

#autoTest();