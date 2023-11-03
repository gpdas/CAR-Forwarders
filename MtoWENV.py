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
import os

# My imports
from MQTTForward import MQTTforwarder

########
# main #
########
def main():

    # Define fields
    MQTT_HOST = os.getenv('CAR_MQTT_IP')
    MQTT_PORT = os.getenv('CAR_MQTT_PORT')
    MQTT_USER = os.getenv('CAR_MQTT_USER')
    MQTT_PASSWORD = os.getenv('CAR_MQTT_PASSWORD')
    MQTT_TOPICS = ['trolley/gps',
                   'trolley/battery',
                   'trolley/method',
                   'trolley/register',
                   'trolley/status']
    WS_HOST = os.getenv('WEBSOCKET_URL')

    # Setup Daemon
    m = MQTTforwarder(MQTT_HOST, MQTT_PORT, MQTT_USER, MQTT_PASSWORD, MQTT_TOPICS, WS_HOST)
    m.run()

# Call main properly
if __name__ == "__main__":
    main()





