# -*- coding: utf-8 -*-

###########################################################
# Aldebaran Behavior Complementary Development Kit
# Arraytools tools
# Aldebaran Robotics (c) 2010 All Rights Reserved - This file is confidential.
###########################################################

"Array tools"

# renammed from array to arraytools, to be more explicit.

print( "importing abcdk.arraytools" );

import random

import typetools

def arrayCreate( nNewSize, value = 0 ):
    "create an array of size nNewSize by inserting some value (default 0)"
    newArray = [];
    for i in range( nNewSize ):
        if( not typetools.isArray( value ) ):
            newArray.append( value );
        else:
            #don't want to have a pointer on the list contains in value, but a fresh new array !
            newArray.append( [] );
            newArray[len( newArray) -1].extend( value ); # TODO: .last() ???
    return newArray;
# arrayCreate - end

def arraySum( anArray ):
    "compute the sum of an array"
    "assume all element of the array could be added each others"
    sum = 0;
    for val in anArray:
        sum += val;
    return sum;
# arraySum - end


def chooseOneElem( aList ):
    "Pick randomly an element in a list "
    "each list contains elements, and optionnal probability ratio (default is 1)"
    "exemple of valid list:"
    "     'hello' (a non list with only one element)"
    "     ['hello', 'goodbye']"
    "     ['sometimes', ['often',10] ] often will appears 10x more often than sometimes (statistically)"
    
    # simple case
    if( not typetools.isArray( aList ) ):
        return aList;
        
    # generate statistic repartition
    listProba = [];
    nSum = 0;
    for elem in aList:
        if( typetools.isArray( elem ) and len( elem ) > 1 ):
            nVal = elem[1];        
        else:
            nVal = 1; # default value        
        listProba.append( nVal );
        nSum += nVal;
    nChoosen = random.randint( 0, nSum - 1 );
#    logToChoregraphe( "nChoosen: %d / total: %d / total different: %d (list:%s)" % ( nChoosen, nSum, len( aList ) , aList ) );
    nSum = 0;
    nIdx = 0;
    for val in listProba:
        nSum += val;
        if( nSum > nChoosen ):
            elem = aList[nIdx];
            if( typetools.isArray( elem ) ):
                return elem[0];
            return elem;
        nIdx += 1;
        
    return "not found or error";
# chooseOneElem - end

def constructFromNamedArray(obj, aNamedArray ):
    "construct a python object from an array of couple [attr_name,attr_value]"
    "reverse of stringtools.dictionnaryToString ???"
    for attr_name, attr_value in aNamedArray:
        try:
            attr = getattr( obj, attr_name );
            if( attr != None ):
                # eval( "obj." + attr_name + " = '" + attr_value + "'" );
                setattr( obj, attr_name, attr_value );
        except BaseException, err:
            print( "WRN: constructFromNamedArray: ??? (err:%s)" % ( str( err ) ) );
            pass
  # for
#   print( dump( obj ) );
    return obj;
# constructFromNamedArray - end

def autoTest():
    a = arrayCreate( 8, 2 );
    s = arraySum( a );
    assert( s == 16 );
    print( "autoTest: ok" );
# autoTest - end

autoTest();