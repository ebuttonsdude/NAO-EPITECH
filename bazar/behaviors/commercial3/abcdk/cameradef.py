# -*- coding: utf-8 -*-

###########################################################
# Aldebaran Behavior Complementary Development Kit
# Camera definition
# @author The usage team - Living Labs
# Aldebaran Robotics (c) 2010 All Rights Reserved - This file is confidential.
###########################################################

"""Camera definition: some constants useful to use camera modules"""

print( "importing abcdk.cameradef" );

# Image Format
VGA = 2;                # 640*480
QVGA =1;               # 320*240
QQVGA = 0;            # 160*120

# Standard Id
BrightnessID       = 0;
ContrastID         = 1;
SaturationID       = 2;
SID       = 2;
HueID              = 3;
RedChromaID        = 4;
BlueChromaID       = 5;
GainID             = 6;
HFlipID            = 7;
VFlipID            = 8;
LensXID            = 9;
LensYID            = 10;
AutoExpositionID   = 11;
AutoWhiteBalanceID = 12;
AutoGainID         = 13;
FormatID           = 14;
FrameRateID        = 15;
BufferSizeID       = 16;
ExposureID         = 17;
SelectID           = 18;
SetDefaultParamsID = 19;
ColorSpaceID       = 20;
ExposureCorrectionID = 21;
CameraAecAlgorithmID     = 22;
CameraFastSwitchID       = 23;
CameraSharpnessID        = 24; 