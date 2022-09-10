#####################################################################
# Author:       Andy Perrett (18684092@students.lincoln.ac.uk)      #
# Version:      1                                                   #
# Date:         19/05/2022                                          #
# Description:  MQTT forwarder to Websocket and visa-versa as part  #
#               of Call-A-Robot and Smart Trolley Device project.   #
#               This is the main module.                            #
# Module:       WtoM.py                                             #
#####################################################################

# Standard imports

# My imports
from WSForward import WSforwarder
from Config import *
import time

########
# main #
########
def main():

    # Setup Daemon
    
    w = WSforwarder(WS_HOST)
    w.run()
    
# Call main properly
if __name__ == "__main__":
    main()





