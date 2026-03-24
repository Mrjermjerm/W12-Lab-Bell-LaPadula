########################################################################
# COMPONENT:
#    CONTROL
# Author:
#    Br. Helfrich, Kyle Mueller, <your name here if you made a change>
# Summary: 
#    This class stores the notion of Bell-LaPadula
########################################################################



# Reminders 
# Permitted:  READ_DOWN & WRITE_UP
# Restricted: READ_UP & WRITE_DOWN

from enum import Enum, auto


class Control(Enum):
    Public = auto()
    Confidential = auto()
    Privileged = auto()
    Secret = auto()


def canRead(userControl, assetControl):
    return userControl.value >= assetControl.value
    

def canWrite(userControl, assetControl):
    return userControl.value <= assetControl.value

