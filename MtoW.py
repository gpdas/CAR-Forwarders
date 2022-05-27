#####################################################################
# Author:       Andy Perrett (18684092@students.lincoln.ac.uk)      #
# Version:      1                                                   #
# Date:         19/05/2022                                          #
# Description:  MQTT forwarder to Websocket and visa-versa as part  #
#               of Call-A-Robot and Smart Trolley Device project.   #
#               This is the main module.                            #
# Module:       MtoW.py                                             #
#####################################################################

# Standard imports

# My imports
from MQTTForward import MQTTforwarder
from Config import *

########
# main #
########
def main():

    # Setup Daemon
    m = MQTTforwarder(MQTT_HOST, MQTT_PORT, MQTT_USER, MQTT_PASSWORD, MQTT_TOPICS, WS_HOST)
    m.run()

# Call main properly
if __name__ == "__main__":

    main()





