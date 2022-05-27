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
from time import sleep

# My imports
from WSForward import WSforwarder
from Config import *

########
# main #
########
def main():

    # Setup Daemon
    
    while True:
        try:
            w = WSforwarder(WS_HOST)
            w.run()
        except Exception as e:
            print(e)

# Call main properly
if __name__ == "__main__":
    main()





