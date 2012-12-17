# -*- coding: utf-8 -*-

###########################################################
# Aldebaran Behavior Complementary Development Kit
# Numeric tools
# Aldebaran Robotics (c) 2010 All Rights Reserved - This file is confidential.
###########################################################

"Numeric tools"

print( "importing abcdk.numeric" );

def limitRange( rVal, rMin, rMax ):
    "ensure that a value is in the range rMin, rMax"
    "WARNING: if rMin is less than rMax, there could be some strange behaviour"
    if( rVal < rMin ):
        rVal = rMin;
    elif( rVal > rMax ):
        rVal = rMax;
    return rVal;
# limitRange - end

def autotest():
    assert( limitRange( 0,0,0) == 0 );
    assert( limitRange( 10,0,5) == 5 );
    assert( limitRange( -5,0.,5) == 0. );
    assert( limitRange( 500,1000,10) == 1000 ); # sounds like a bug, but it's a known limitation :)
# autotest - end
    
autotest();