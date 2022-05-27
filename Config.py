#####################################################################
# Author:       Andy Perrett (18684092@students.lincoln.ac.uk)      #
# Version:      1                                                   #
# Date:         19/05/2022                                          #
# Description:  MQTT forwarder to Websocket and visa-versa as part  #
#               of Call-A-Robot and Smart Trolley Device project.   #
#               These are the configurable variables                #
# Module:       Config.py                                           #
#####################################################################

MQTT_USER = 'andy'
MQTT_PASSWORD = '!qswd3288!S'
MQTT_HOST = 'mqtt.lar.lincoln.ac.uk'
MQTT_PORT = 8097

# Topics as a list
MQTT_TOPICS = ['trolley/gps', 'trolley/battery', 'trolley/method', 'trolley/registration', 'trolley/status']

WS_HOST = 'wss://lcas.lincoln.ac.uk/car/ws' #'wss://demo.piesocket.com/v3/channel_1?api_key=VCXCEuvhGcBDP7XhiJJUDvR1e1D3eiVjgZ9VRiaV&notify_self'#'wss://lcas.lincoln.ac.uk/car/ws'